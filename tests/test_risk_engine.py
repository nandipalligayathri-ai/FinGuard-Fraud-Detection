from datetime import datetime
from app.services.risk_engine import RULE_WEIGHTS, AMOUNT_THRESHOLD

def test_rule_weights_are_documented_and_bounded():
    assert sum(RULE_WEIGHTS.values()) == 100
    assert AMOUNT_THRESHOLD > 0

def test_amount_threshold_is_numeric():
    assert isinstance(AMOUNT_THRESHOLD, (int, float))
