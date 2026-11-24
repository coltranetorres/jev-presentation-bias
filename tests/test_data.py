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


def test_load_mmlu_pro_pairs_correct_option_with_a_distractor(tmp_path):
    from jev_bias.data import load_mmlu_pro

    rows = [
        {"question_id": i, "question": f"q{i}", "options": ["o0", "o1", "o2", "o3"],
         "answer": "B", "answer_index": 1, "category": cat}
        for i, cat in enumerate(["law", "law", "math", "history", "physics"])
    ]
    p = tmp_path / "m.parquet"
    pd.DataFrame(rows).to_parquet(p)
    items = load_mmlu_pro(10, seed=0, path=str(p))
    assert {i.question for i in items} == {"q0", "q1", "q3"}  # math/physics excluded
    for it in items:
        assert it.correct == "o1" and it.wrong in {"o0", "o2", "o3"} and it.qid.startswith("m")
    assert load_mmlu_pro(10, seed=0, path=str(p)) == items


def _mmlu_parquet(tmp_path):
    rows = [{"question_id": 1, "question": "q1", "options": ["o0", "o1", "o2", "o3"],
             "answer": "B", "answer_index": 1, "category": "law"}]
    p = tmp_path / "m.parquet"
    pd.DataFrame(rows).to_parquet(p)
    return str(p)


def test_load_mmlu_pro_uses_model_chosen_distractor(monkeypatch, tmp_path):
    from jev_bias import data

    monkeypatch.setattr(data, "chat", lambda prompt, model, **k: "D")
    (it,) = data.load_mmlu_pro(5, path=_mmlu_parquet(tmp_path), distractor_model="m")
    assert it.correct == "o1" and it.wrong == "o3"


def test_load_mmlu_pro_falls_back_to_random_on_bad_model_pick(monkeypatch, tmp_path):
    from jev_bias import data

    for bad in ("B", "Z", "no idea"):  # the correct letter, out of range, unparseable
        monkeypatch.setattr(data, "chat", lambda prompt, model, _b=bad, **k: _b)
        (it,) = data.load_mmlu_pro(5, path=_mmlu_parquet(tmp_path), distractor_model="m")
        assert it.wrong in {"o0", "o2", "o3"}
