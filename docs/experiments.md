# Experiments

Reproduce training on synthetic data:

```bash
python -m src.models.train --config configs/train.yaml
```

Artifacts are stored under `models/<version>/` including `model.pkl`, `preprocess.pkl`, `metrics.json`, and `feature_schema.json`. The `models/model_card.md` file summarizes the training configuration and metrics.

To evaluate on a specific dataset, prepare the data as a CSV with feature columns matching `feature_schema.json`, then adapt the training script to load the dataset and run `evaluate()` with the saved model.
