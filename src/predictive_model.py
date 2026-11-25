
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_predict,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# Features used by the predictive model
CATEGORICAL_FEATURES = [
    "production_line",
    "shift",
    "product",
]

NUMERIC_FEATURES = [
    "production_quantity",
    "seal_temperature",
]

TARGET = "loss_quantity"
WASTE_THRESHOLD = 200


def prepare_training_data(df):

    required = [
        *CATEGORICAL_FEATURES,
        *NUMERIC_FEATURES,
        TARGET,
    ]

    missing = [
        col for col in required
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing required mapped columns: "
            + ", ".join(missing)
        )

    data = df[required].copy()

    # Convert numerical columns
    for col in NUMERIC_FEATURES + [TARGET]:
        data[col] = pd.to_numeric(
            data[col], errors="coerce"
        )

    # Remove records without a known target
    data = data.dropna(subset=[TARGET])

    # Remove invalid production records
    data = data[
        (data["production_quantity"] > 0)
        & (data[TARGET] >= 0)
    ]

    # Binary classification target
    y = (
        data[TARGET] >= WASTE_THRESHOLD
    ).astype(int)

    X = data[
        CATEGORICAL_FEATURES + NUMERIC_FEATURES
    ].copy()

    # Treat empty categorical values as missing
    for col in CATEGORICAL_FEATURES:
        X[col] = X[col].replace(
            r"^\s*$", pd.NA, regex=True
        )

    return X, y


def build_model():

    categorical_pipeline = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ])

    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    preprocessor = ColumnTransformer([
        (
            "categorical",
            categorical_pipeline,
            CATEGORICAL_FEATURES
        ),
        (
            "numerical",
            numeric_pipeline,
            NUMERIC_FEATURES
        )
    ])

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier",
            MLPClassifier(
                hidden_layer_sizes=(32,),
                activation="relu",
                solver="adam",
                learning_rate_init=0.001,
                max_iter=1000,
                random_state=42
            )
        )
    ])

    return model


def train_model(df):

    X, y = prepare_training_data(df)

    class_counts = y.value_counts()

    if len(class_counts) != 2:
        raise ValueError(
            "Training data must contain both "
            "high-risk and low-risk batches."
        )

    minority_count = int(class_counts.min())

    if minority_count < 3:
        raise ValueError(
            "At least 3 examples from each risk "
            "class are required for initial training."
        )

    folds = min(5, minority_count)

    model = build_model()

    cv = StratifiedKFold(
        n_splits=folds,
        shuffle=True,
        random_state=42
    )

    # Evaluate using out-of-fold predictions
    cv_predictions = cross_val_predict(
        model,
        X,
        y,
        cv=cv,
        method="predict"
    )

    # Train final model using all uploaded records
    model.fit(X, y)

    metrics = {
        "records": len(X),
        "high_risk_records": int((y == 1).sum()),
        "low_risk_records": int((y == 0).sum()),
        "accuracy": accuracy_score(
            y, cv_predictions
        ),
        "balanced_accuracy": balanced_accuracy_score(
            y, cv_predictions
        ),
        "precision": precision_score(
            y, cv_predictions, zero_division=0
        ),
        "recall": recall_score(
            y, cv_predictions, zero_division=0
        ),
        "f1": f1_score(
            y, cv_predictions, zero_division=0
        ),
        "confusion_matrix": confusion_matrix(
            y, cv_predictions, labels=[0, 1]
        ),
        "classification_report": classification_report(
            y,
            cv_predictions,
            labels=[0, 1],
            target_names=["Low Risk", "High Risk"],
            zero_division=0
        )
    }

    return model, metrics


def predict_batch(
    model,
    line,
    shift,
    product,
    production,
    temperature
):

    batch = pd.DataFrame([{
        "production_line": line,
        "shift": shift,
        "product": product,
        "production_quantity": production,
        "seal_temperature": temperature
    }])

    prediction = int(model.predict(batch)[0])

    probabilities = model.predict_proba(batch)[0]

    high_risk_index = list(
        model.classes_
    ).index(1)

    risk_score = float(
        probabilities[high_risk_index] * 100
    )

    return {
        "prediction": prediction,
        "risk_score": risk_score,
        "risk_label": (
            "HIGH RISK"
            if prediction == 1
            else "LOW RISK"
        )
    }
