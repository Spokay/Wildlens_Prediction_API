import pathlib

import keras
import tensorflow as tf

from app.config import WILDLENS_FOOTPRINT_BINARY_CLASSIFIER_MODEL_PATH, \
    WILDLENS_FOOTPRINT_MULTICLASS_CLASSIFIER_MODEL_PATH

gpus = tf.config.list_physical_devices('GPU')
if gpus:
  # Restrict TensorFlow to only use the first GPU
  try:
    tf.config.set_visible_devices(gpus[0], 'GPU')
    logical_gpus = tf.config.list_logical_devices('GPU')
    tf.config.experimental.set_memory_growth(gpus[0], True)
  except RuntimeError as e:
    # Visible devices must be set before GPUs have been initialized
    print(e)


# Model which predicts whether an image contains a footprint or not
project_root = pathlib.Path(__file__).resolve().parent

binary_classifier_path = project_root / WILDLENS_FOOTPRINT_BINARY_CLASSIFIER_MODEL_PATH

binary_classifier_model = keras.models.load_model(filepath=binary_classifier_path)

# Model which classifies a footprint image into classes of species

multiclass_classifier_path = project_root / WILDLENS_FOOTPRINT_MULTICLASS_CLASSIFIER_MODEL_PATH
multiclass_classifier_model = keras.models.load_model(WILDLENS_FOOTPRINT_MULTICLASS_CLASSIFIER_MODEL_PATH)