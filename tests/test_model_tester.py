import os

import pandas as pd
from scripts.model_tester import NewScraper

current_dir = os.path.dirname(__file__)


def test_TwitterScraper():
    output_dir = os.path.join(current_dir, "..", "output")

    # test max_result
    NewScraper("vaksin covid", max_result=10).scrape("vaksin_covid")
    filename = os.path.join(output_dir, "scrape-vaksin_covid.csv")
    dataset = pd.read_csv(filename)
    assert len(dataset) == 10
    os.remove(filename)
