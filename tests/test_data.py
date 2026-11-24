import pandas as pd
import pytest

from jev_bias.data import load_items


@pytest.fixture
def csv_path(tmp_path):
    rows = [{"Question": f"q{i}", "Best Answer": f"c{i}", "Best Incorrect Answer": f"w{i}"} for i in range(20)]
    rows.append({"Question": "qe", "Best Answer": "", "Best Incorrect Answer": "w"})
    rows.append({"Question": "qn", "Best Answer": "c", "Best Incorrect Answer": None})
    p = tmp_path / "t.csv"
    pd.DataFrame(rows).to_csv(p, index=False)
    return str(p)


def test_load_items_is_deterministic(csv_path):
    assert load_items(5, seed=1, path=csv_path) == load_items(5, seed=1, path=csv_path)


def test_load_items_skips_empty_answers(csv_path):
    qs = {i.question for i in load_items(100, path=csv_path)}
    assert "qe" not in qs and "qn" not in qs and len(qs) == 20


def test_load_items_respects_n(csv_path):
    items = load_items(7, path=csv_path)
    assert len(items) == 7
    assert items[0].correct and items[0].wrong and items[0].qid
