from jev_bias import absolute
from jev_bias.data import Item

ITEMS = [Item("q1", "Q?", "c", "w")]
VARIANTS = {
    "q1": {
        "correct": {"plain": "c-plain", "long": "c-long"},
        "wrong": {"plain": "w-plain"},
        "excluded": [["wrong", "long"]],
    }
}


def fake_jev(state, questions, cache_dir=""):
    return {"is_correct": {"type": "noul", "noul": 0.9 if "c-" in state[1] else 0.2}}


def test_run_absolute_one_row_per_variant(monkeypatch, tmp_path):
    monkeypatch.setattr(absolute, "call_jev", fake_jev)
    df = absolute.run_absolute(VARIANTS, ITEMS, out_path=str(tmp_path / "a.csv"))
    assert len(df) == 3
    assert list(df.columns) == ["qid", "side", "style", "p_correct"]
    row = df[(df.side == "correct") & (df.style == "long")].iloc[0]
    assert row.p_correct == 0.9


def test_run_absolute_skips_excluded(monkeypatch, tmp_path):
    monkeypatch.setattr(absolute, "call_jev", fake_jev)
    df = absolute.run_absolute(VARIANTS, ITEMS, out_path=str(tmp_path / "a.csv"))
    assert not ((df.side == "wrong") & (df.style == "long")).any()
