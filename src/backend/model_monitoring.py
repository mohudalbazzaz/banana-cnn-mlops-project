import numpy as np
import mlflow
import random

from src.backend.train_model import load_model
from src.backend.blob_storage import extract_imgs_from_db

BANANA_PRODUCTION_IMAGES = "banana-production-images"


def monitor_model() -> None:
    """
    Loads labelled test images from a storage bucket, performs inference
    using a pre-loaded model, and logs each prediction to MLflow.
    """
    model = load_model()

    image_classifications = extract_imgs_from_db(BANANA_PRODUCTION_IMAGES)

    X = []
    y = []

    for classification, images in image_classifications.items():

        X.extend(images)
        y.extend(len(images) * [classification])

    mlflow.set_experiment("Banana Monitoring")

    with mlflow.start_run():

        correct_predictions = 0

        for img, true_label in random.sample(list(zip(X, y)), 50):

            img = np.expand_dims(img, axis=0)

            prediction_probs = model.predict(img)

            class_names = ["overripe", "ripe", "unripe"]
            predicted_class = class_names[np.argmax(prediction_probs)]
            predicted_class = f"production-{predicted_class}"

            correct_predictions += int(predicted_class == true_label)

        accuracy = correct_predictions / 50

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("num_samples", 50)


if __name__ == "__main__":
    monitor_model()
