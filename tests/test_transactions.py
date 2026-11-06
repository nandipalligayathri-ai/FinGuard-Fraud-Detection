def test_sample_csv_has_required_columns():
    import csv
    with open("../data/sample_transactions.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert {"account_id","transaction_datetime","amount","transaction_type","channel"} <= set(reader.fieldnames)
