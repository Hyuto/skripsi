import os

import numpy as np
from src.model import Model

current_dir = os.path.dirname(__file__)


def test_predict():
    model = Model(os.path.join(current_dir, "..", "models", "model.onnx"))

    assert model.predict("test")
    assert model.predict(["test"])
    assert model.predict(np.asarray(["test"]))
    assert model.predict(np.asarray([["test"]]))
    label, probs = model.predict(np.asarray(["test", "test 2"]))
    assert label.shape == (2,) and probs.shape == (2, 7)
