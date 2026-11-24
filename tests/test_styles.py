import json

from jev_bias import styles
from jev_bias.data import Item

ITEMS = [Item("q1", "Q one?", "right fact", "wrong fact"), Item("q2", "Q two?", "r2", "w2")]


def fake_chat_factory(bad_style=None):
    def fake_chat(prompt, model, system=None, cache_dir=""):
        if "SAME or DIFFERENT" in prompt:
            return "DIFFERENT" if "BAD" in prompt else "SAME"
        for style, tmpl in styles.STYLE_PROMPTS.items():
            if prompt.startswith(tmpl.split("{text}")[0]) and style != "plain":
                return "BAD text" if style == bad_style else f"{style} rewrite"
        return "plain answer"

    return fake_chat


def run(monkeypatch, tmp_path, bad_style=None):
    monkeypatch.setattr(styles, "chat", fake_chat_factory(bad_style))
    out = tmp_path / "v.json"
    res = styles.build_variants(ITEMS, "rw", "ck", out_path=str(out))
    return res, out


def test_build_variants_covers_all_styles(monkeypatch, tmp_path):
    res, out = run(monkeypatch, tmp_path)
    assert set(res) == {"q1", "q2"}
    for side in ("correct", "wrong"):
        assert set(res["q1"][side]) == set(styles.STYLES)
    assert res["q1"]["excluded"] == []
    assert json.loads(out.read_text()) == res


def test_different_fact_check_excludes_variant(monkeypatch, tmp_path):
    res, _ = run(monkeypatch, tmp_path, bad_style="long")
    assert "long" not in res["q1"]["correct"]
    assert ["correct", "long"] in res["q1"]["excluded"]
    assert "plain" in res["q1"]["correct"]


def test_exclusions_recorded_not_silently_dropped(monkeypatch, tmp_path):
    res, _ = run(monkeypatch, tmp_path, bad_style="short")
    assert sorted(res["q2"]["excluded"]) == [["correct", "short"], ["wrong", "short"]]


def test_plain_that_drifts_from_source_fact_excludes_side(monkeypatch, tmp_path):
    def fake(prompt, model, system=None, cache_dir=""):
        if "SAME or DIFFERENT" in prompt:
            return "DIFFERENT" if "BAD" in prompt else "SAME"
        if prompt.startswith(styles.STYLE_PROMPTS["plain"].split("{text}")[0]):
            return "BAD plain" if "Fact to assert: right fact" in prompt else "plain answer"
        return "rewrite"

    monkeypatch.setattr(styles, "chat", fake)
    res = styles.build_variants(ITEMS, "rw", "ck", out_path=str(tmp_path / "v.json"))
    assert res["q1"]["correct"] == {}
    assert ["correct", "plain"] in res["q1"]["excluded"]
    assert "plain" in res["q1"]["wrong"]


def test_filtered_model_response_excludes_variant_instead_of_crashing(monkeypatch, tmp_path):
    from jev_bias.client import EmptyChatError

    def fake(prompt, model, system=None, cache_dir=""):
        if "SAME or DIFFERENT" in prompt:
            return "SAME"
        if prompt.startswith(styles.STYLE_PROMPTS["confident"].split("{text}")[0]):
            raise EmptyChatError("content filter")
        return "text"

    monkeypatch.setattr(styles, "chat", fake)
    res = styles.build_variants(ITEMS, "rw", "ck", out_path=str(tmp_path / "v.json"))
    assert ["correct", "confident"] in res["q1"]["excluded"]
    assert "confident" not in res["q1"]["correct"] and "plain" in res["q1"]["correct"]


def test_filtered_check_response_excludes_variant(monkeypatch, tmp_path):
    from jev_bias.client import EmptyChatError

    def fake(prompt, model, system=None, cache_dir=""):
        if "SAME or DIFFERENT" in prompt and "long rewrite" in prompt:
            raise EmptyChatError("content filter")
        if "SAME or DIFFERENT" in prompt:
            return "SAME"
        if prompt.startswith(styles.STYLE_PROMPTS["long"].split("{text}")[0]):
            return "long rewrite"
        return "text"

    monkeypatch.setattr(styles, "chat", fake)
    res = styles.build_variants(ITEMS, "rw", "ck", out_path=str(tmp_path / "v.json"))
    assert ["wrong", "long"] in res["q2"]["excluded"]
