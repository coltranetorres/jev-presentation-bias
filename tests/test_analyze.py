import numpy as np
import pandas as pd

from jev_bias import analyze


def test_bootstrap_ci_contains_mean_on_known_data():
    x = np.array([0.0, 1.0] * 50)
    lo, hi = analyze.bootstrap_ci(x)
    assert lo < 0.5 < hi and hi - lo < 0.3


def abs_df():
    rows = []
    for q in ("a", "b", "c", "d"):
        rows += [(q, "correct", "plain", 0.8), (q, "correct", "long", 0.9),
                 (q, "wrong", "plain", 0.3), (q, "wrong", "long", 0.6)]
    return pd.DataFrame(rows, columns=["qid", "side", "style", "p_correct"])


def test_absolute_summary_zero_shift_for_plain():
    s = analyze.absolute_summary(abs_df())
    plain = s[(s["style"] == "plain") & (s["side"] == "wrong")].iloc[0]
    assert plain["shift"] == 0
    long_wrong = s[(s["style"] == "long") & (s["side"] == "wrong")].iloc[0]
    assert abs(long_wrong["shift"] - 0.3) < 1e-9 and long_wrong["flip_rate"] == 1.0  # 0.3 -> 0.6 crosses 0.5
    assert long_wrong["n"] == 4


def pair_df():
    rows = []
    for q in ("a", "b"):
        for order in ("correct_first", "wrong_first"):
            rows.append((q, "plain", "plain", order, True, 0.9))
            rows.append((q, "plain", "long", order, order == "correct_first", 0.5))
    return pd.DataFrame(rows, columns=["qid", "correct_style", "wrong_style", "order", "picked_correct", "p_correct_side"])


def test_pairwise_summary_reports_orders_separately():
    s = analyze.pairwise_summary(pair_df())
    cond = s[(s["wrong_style"] == "long")]
    assert set(cond["order"]) == {"correct_first", "wrong_first", "both"}
    assert cond[cond["order"] == "correct_first"].iloc[0]["accuracy"] == 1.0
    assert cond[cond["order"] == "wrong_first"].iloc[0]["accuracy"] == 0.0


def test_pairwise_summary_handles_empty_cell_without_crash():
    s = analyze.pairwise_summary(pair_df().iloc[0:0])
    assert len(s) == 0
