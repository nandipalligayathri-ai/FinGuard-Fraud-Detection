def test_review_status_values():
    allowed = {"PENDING", "UNDER_REVIEW", "CLEARED", "CLOSED"}
    assert "PENDING" in allowed
    assert "CONFIRMED_FRAUD" not in allowed
