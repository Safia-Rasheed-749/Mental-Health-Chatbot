import csv
import json

from scripts.create_deduplicated_splits import create
from scripts.evaluate_leakage_adjusted import evaluate
from scripts.train_and_export_probabilities import export_probabilities


def _write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["text", "label"])
        writer.writeheader()
        writer.writerows(rows)


def test_deduplicator_writes_new_files_and_excludes_audited_overlaps(tmp_path):
    train = tmp_path / "train.csv"
    test = tmp_path / "test.csv"
    _write_csv(train, [{"text": "train exact", "label": "0"}, {"text": "train base similar", "label": "1"}])
    _write_csv(test, [{"text": "train exact", "label": "0"}, {"text": "train base similar slightly", "label": "1"}, {"text": "clean", "label": "0"}])
    audit = tmp_path / "audit.json"
    audit.write_text(json.dumps({
        "csv_files": [{"path": str(train)}, {"path": str(test)}],
        "exact_duplicate_texts_across_split_files": [{"left": str(train), "right": str(test), "duplicate_records": [
            {"left_source_rows_1based_including_header": [2], "right_source_rows_1based_including_header": [2]}]}],
        "near_duplicate_split_checks": [{"left": str(test), "right": str(train), "status": "complete", "pairs": [
            {"left_row_1based": 3, "right_row_1based": 3, "jaccard": .98}]}],
    }))
    report = create(audit, [f"train={train}", f"test={test}"], tmp_path / "output")
    info = json.loads(report.read_text())
    assert info["splits"]["test"]["rows_before"] == 3
    assert info["splits"]["test"]["rows_after"] == 1
    assert len(list(csv.DictReader((tmp_path / "output" / "test_deduplicated.csv").open()))) == 1
    assert len(list(csv.DictReader(test.open()))) == 3  # immutable source


def test_leakage_adjusted_eval_reports_brier_bootstrap_and_calibration(tmp_path):
    train, test, prediction = tmp_path / "train.csv", tmp_path / "test.csv", tmp_path / "pred.csv"
    _write_csv(train, [{"text": "duplicate", "label": "0"}])
    _write_csv(test, [{"text": "duplicate", "label": "0"}, {"text": "near variant", "label": "1"}, {"text": "clean", "label": "1"}])
    with prediction.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["y_true", "prob_0", "prob_1"])
        writer.writeheader()
        writer.writerows([{"y_true": "0", "prob_0": .9, "prob_1": .1}, {"y_true": "1", "prob_0": .2, "prob_1": .8}, {"y_true": "1", "prob_0": .1, "prob_1": .9}])
    audit = tmp_path / "audit.json"
    audit.write_text(json.dumps({"near_duplicate_split_checks": [{"left": str(test), "right": str(train), "status": "complete", "pairs": [
        {"left_row_1based": 3, "right_row_1based": 2, "jaccard": .97}]}]}))
    report_path = evaluate(prediction, train, test, audit, tmp_path / "metrics", bootstrap=100)
    result = json.loads(report_path.read_text())
    assert result["sample_count_after"] == 1
    assert result["excluded_count"] == 2
    assert result["multiclass_brier_score"] >= 0
    assert (tmp_path / "metrics" / "calibration_curve.csv").exists()


def test_probability_export_uses_complete_vectors_and_evaluator_column_names(tmp_path):
    target = tmp_path / "predictions.csv"
    export_probabilities(target, ["example A", "example B"], [0, 1], [[.8, .2], [.1, .9]], ["negative", "positive"])
    with target.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["prob_0"] == "0.8000000000"
    assert rows[1]["prob_1"] == "0.9000000000"
    assert rows[0]["y_pred"] == "0"
