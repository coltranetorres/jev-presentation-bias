import pytest

from jev_bias import pairwise
from jev_bias.data import Item

ITEMS = [Item("q1", "Q?", "c", "w")]
STYLES = ["plain", "long"]
VARIANTS = {"q1": {"correct": {"plain": "c-plain", "long": "c-long"},
                   "wrong": {"plain": "w-plain", "long": "w-long"}, "excluded": []}}


def make_jev(pick_text_prefix):
    """Fake Jev: picks whichever slot holds text starting with the given prefix."""
    def fake(state, questions, cache_dir=""):
        a, b = state[1].split(": ", 1)[1], state[2].split(": ", 1)[1]
        pick = "A" if a.startswith(pick_text_prefix) else "B"
        return {"better": {"type": "choice", "choice": pick, "probabilities": {"A": float(pick == "A"), "B": float(pick == "B")}}}
    return fake


def test_both_orders_run_for_every_pair(monkeypatch, tmp_path):
    monkeypatch.setattr(pairwise, "call_jev", make_jev("c-"))
    df = pairwise.run_pairwise(VARIANTS, ITEMS, styles=STYLES, out_path=str(tmp_path / "p.csv"))
    # conditions: plain/plain, long/plain, plain/long  -> 3 conds x 2 orders
    assert len(df) == 6
    assert set(df.order) == {"correct_first", "wrong_first"}


def test_picked_correct_maps_through_order(monkeypatch, tmp_path):
    monkeypatch.setattr(pairwise, "call_jev", make_jev("c-"))
    df = pairwise.run_pairwise(VARIANTS, ITEMS, styles=STYLES, out_path=str(tmp_path / "p.csv"))
    assert df.picked_correct.all()
    monkeypatch.setattr(pairwise, "call_jev", make_jev("w-"))
    df = pairwise.run_pairwise(VARIANTS, ITEMS, styles=STYLES, out_path=str(tmp_path / "p.csv"))
    assert not df.picked_correct.any()


def test_unknown_choice_key_raises(monkeypatch, tmp_path):
    monkeypatch.setattr(pairwise, "call_jev", lambda *a, **k: {"better": {"choice": "C", "probabilities": {"C": 1}}})
    with pytest.raises(ValueError):
        pairwise.run_pairwise(VARIANTS, ITEMS, styles=STYLES, out_path=str(tmp_path / "p.csv"))
