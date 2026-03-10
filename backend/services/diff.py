import json
from decimal import Decimal
from datetime import datetime, date


def _serialize(val):
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, (datetime, date)):
        return val.isoformat()
    if val is None:
        return None
    return val


def _row_key(row: list) -> str:
    return json.dumps([_serialize(v) for v in row], sort_keys=False)


def compute_diff(expected: dict, actual: dict) -> dict:
    if expected.get("error") or actual.get("error"):
        return {
            "match_pct": 0,
            "matching_rows": [],
            "missing_rows": expected.get("rows", []),
            "extra_rows": actual.get("rows", []),
            "expected_columns": expected.get("columns", []),
            "actual_columns": actual.get("columns", []),
            "order_correct": False,
            "column_order_match": False,
        }

    exp_rows = expected.get("rows", [])
    act_rows = actual.get("rows", [])
    exp_cols = expected.get("columns", [])
    act_cols = actual.get("columns", [])

    # Column order check
    column_order_match = exp_cols == act_cols

    # Row membership check
    exp_set = {}
    for r in exp_rows:
        key = _row_key(r)
        exp_set[key] = exp_set.get(key, 0) + 1

    matching = []
    extra = []
    exp_copy = dict(exp_set)
    for r in act_rows:
        key = _row_key(r)
        if exp_copy.get(key, 0) > 0:
            matching.append(r)
            exp_copy[key] -= 1
        else:
            extra.append(r)

    act_set = {}
    for r in act_rows:
        key = _row_key(r)
        act_set[key] = act_set.get(key, 0) + 1

    missing = []
    act_copy = dict(act_set)
    for r in exp_rows:
        key = _row_key(r)
        if act_copy.get(key, 0) > 0:
            act_copy[key] -= 1
        else:
            missing.append(r)

    # Row ordering check: compare serialized order of matching rows
    order_correct = True
    if len(matching) == len(exp_rows) and len(extra) == 0:
        exp_keys = [_row_key(r) for r in exp_rows]
        act_keys = [_row_key(r) for r in act_rows]
        order_correct = exp_keys == act_keys

    if len(exp_rows) == 0 and len(act_rows) == 0:
        match_pct = 100.0
    else:
        total = max(len(exp_rows), 1)
        match_pct = round(len(matching) / total * 100, 1)

    return {
        "match_pct": match_pct,
        "matching_rows": matching,
        "missing_rows": missing,
        "extra_rows": extra,
        "expected_columns": exp_cols,
        "actual_columns": act_cols,
        "order_correct": order_correct,
        "column_order_match": column_order_match,
    }
