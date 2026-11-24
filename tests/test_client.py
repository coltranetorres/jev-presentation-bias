import pytest

from jev_bias import client


class FakeResp:
    def __init__(self, status=200, payload=None):
        self.status_code = status
        self._payload = payload or {}

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"http {self.status_code}")


@pytest.fixture(autouse=True)
def _fast(monkeypatch):
    monkeypatch.setattr(client.time, "sleep", lambda s: None)
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")


QUESTIONS = {"q": {"type": "noul", "instructions": "x", "criteria": {"true": "t", "false": "f"}}}


def test_call_jev_caches_second_call(monkeypatch, tmp_path):
    calls = []

    def post(*a, **k):
        calls.append(1)
        return FakeResp(200, {"answers": {"q": {"noul": 0.9}}})

    monkeypatch.setattr(client.requests, "post", post)
    a = client.call_jev(["s"], QUESTIONS, cache_dir=str(tmp_path))
    b = client.call_jev(["s"], QUESTIONS, cache_dir=str(tmp_path))
    assert a == b == {"q": {"noul": 0.9}}
    assert len(calls) == 1


def test_call_jev_retries_on_429_then_succeeds(monkeypatch, tmp_path):
    seq = [FakeResp(429), FakeResp(200, {"answers": {"q": {"noul": 0.1}}})]
    monkeypatch.setattr(client.requests, "post", lambda *a, **k: seq.pop(0))
    assert client.call_jev(["s"], QUESTIONS, cache_dir=str(tmp_path)) == {"q": {"noul": 0.1}}


def test_call_jev_raises_and_does_not_cache_on_persistent_error(monkeypatch, tmp_path):
    monkeypatch.setattr(client.requests, "post", lambda *a, **k: FakeResp(500))
    with pytest.raises(RuntimeError):
        client.call_jev(["s"], QUESTIONS, cache_dir=str(tmp_path))
    assert list(tmp_path.iterdir()) == []


def test_call_jev_raises_on_malformed_body(monkeypatch, tmp_path):
    monkeypatch.setattr(client.requests, "post", lambda *a, **k: FakeResp(200, {"oops": 1}))
    with pytest.raises(RuntimeError):
        client.call_jev(["s"], QUESTIONS, cache_dir=str(tmp_path))
    assert list(tmp_path.iterdir()) == []


def test_chat_caches_second_call(monkeypatch, tmp_path):
    calls = []

    def post(*a, **k):
        calls.append(1)
        return FakeResp(200, {"choices": [{"message": {"content": "hi"}}]})

    monkeypatch.setattr(client.requests, "post", post)
    assert client.chat("p", "m", cache_dir=str(tmp_path)) == "hi"
    assert client.chat("p", "m", cache_dir=str(tmp_path)) == "hi"
    assert len(calls) == 1


def test_call_jev_does_not_cache_invalid_choice(monkeypatch, tmp_path):
    qs = {"better": {"type": "choice", "instructions": "x", "criteria": {"A": "a", "B": "b"}}}
    bad = {"answers": {"better": {"type": "choice", "choice": "C", "probabilities": {"C": 1}}}}
    monkeypatch.setattr(client.requests, "post", lambda *a, **k: FakeResp(200, bad))
    with pytest.raises(RuntimeError):
        client.call_jev(["s"], qs, cache_dir=str(tmp_path))
    assert list(tmp_path.iterdir()) == []


def test_call_jev_does_not_cache_noul_missing_value(monkeypatch, tmp_path):
    bad = {"answers": {"q": {"type": "noul"}}}
    monkeypatch.setattr(client.requests, "post", lambda *a, **k: FakeResp(200, bad))
    with pytest.raises(RuntimeError):
        client.call_jev(["s"], QUESTIONS, cache_dir=str(tmp_path))
    assert list(tmp_path.iterdir()) == []
