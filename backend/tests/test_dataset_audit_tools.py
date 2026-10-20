from pathlib import Path

from scripts.audit_datasets import _near_duplicates, _norm, inspect_csv


def test_normalization_detects_case_punctuation_and_spacing_variants():
    assert _norm("Hello,   WORLD!") == _norm("hello world")


def test_near_duplicate_cap_reports_exact_skipped_pairs():
    left = {"path": "left.csv", "texts": ["a calm supportive response", "a calm helpful response"], "text_column": "text"}
    right = {"path": "right.csv", "texts": ["a calm supportive response", "a calm helpful response"], "text_column": "text"}
    result = _near_duplicates(left, right, threshold=0.3, pair_cap=1)
    assert result["comparisons_performed"] == 1
    assert result["status"] == "partial_pair_cap"
    assert result["skipped_comparisons"]
    assert all("cap" in item["reason"] for item in result["skipped_comparisons"])


def test_near_duplicate_method_is_explicit():
    left = {"path": "left.csv", "texts": ["some text"], "text_column": "text"}
    right = {"path": "right.csv", "texts": ["some other text"], "text_column": "text"}
    result = _near_duplicates(left, right, threshold=0.95, pair_cap=100)
    assert "MinHash LSH" in result["method"]
    assert result["possible_comparisons"] == 1


def test_stress_training_uses_seeded_train_only_validation_split():
    source = (Path(__file__).parents[1] / "app" / "ai" / "stress_detection" / "train.py").read_text(encoding="utf-8")
    assert "random_state=SEED" in source
    assert "data_seed=SEED" in source
    assert 'data_files={"train": str(DATASET_PATH / "clean_train.csv")}' in source
    assert '"clean_test.csv"' not in source


def test_csv_inspection_streams_and_reports_duplicate_source_rows(tmp_path):
    source = tmp_path / "tiny.csv"
    source.write_text("text,label\nSame text,0\nsame TEXT!,1\nunique,0\n", encoding="utf-8")
    audited = inspect_csv(source)
    assert audited["row_count"] == 3
    assert audited["exact_duplicate_texts_within_file"] == 1
    assert audited["exact_duplicate_text_groups_within_file"][0]["source_rows_1based_including_header"] == [2, 3]
