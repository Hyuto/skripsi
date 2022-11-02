import os

import pandas as pd
from src.model_tester import ModelScraper

current_dir = os.path.dirname(__file__)


def test_ModelScraper():
    output_dir = os.path.join(current_dir, "..", "output")
    model_dir = os.path.join(current_dir, "..", "models", "model.onnx")

    # test max_result
    ModelScraper(model_dir, "vaksin covid").scrape(export="vaksin_covid", max_result=10)
    filename = os.path.join(output_dir, "scrape-vaksin_covid.csv")
    dataset = pd.read_csv(filename)
    assert len(dataset) == 10
    os.remove(filename)
