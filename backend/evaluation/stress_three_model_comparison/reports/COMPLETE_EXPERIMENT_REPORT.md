# Stress dataset: three-model comparison

Task: binary text classification (0 = Not Stressed, 1 = Stressed).
Selection criterion: validation Macro-F1; test set was not used for selection.

Selected production model: **microsoft/deberta-v3-base** (deberta_v3_base).
Validation Macro-F1: **0.8437**.

## Results

| model_key               | base_model                |   validation_accuracy |   validation_macro_f1 |   validation_weighted_f1 |   test_accuracy |   test_macro_f1 |   test_weighted_f1 |
|:------------------------|:--------------------------|----------------------:|----------------------:|-------------------------:|----------------:|----------------:|-------------------:|
| deberta_v3_base         | microsoft/deberta-v3-base |              0.844523 |              0.843662 |                 0.844277 |        0.81958  |        0.818545 |           0.818986 |
| roberta_base            | roberta-base              |              0.837456 |              0.833615 |                 0.834955 |        0.781818 |        0.775815 |           0.776995 |
| distilbert_base_uncased | distilbert-base-uncased   |              0.805654 |              0.805031 |                 0.805615 |        0.772028 |        0.770996 |           0.77149  |

## Important limitations

This is a benchmark on the supplied dataset, not clinical validation.
Do not use predictions to diagnose or replace professional care.