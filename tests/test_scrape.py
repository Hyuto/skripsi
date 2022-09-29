import os

import pandas as pd
from scripts.scraper import TwitterScraper

current_dir = os.path.dirname(__file__)


def test_TwitterScraper():
    output_dir = os.path.join(current_dir, "..", "output")

    # test max_result
    TwitterScraper("minyak").scrape(
        export="minyak",
        max_result=10,
        denied_users=os.path.join(os.path.dirname(__file__), "..", "data", "denied-users.json"),
    )
    filename = os.path.join(output_dir, "scrape-minyak.csv")
    dataset = pd.read_csv(filename)
    assert len(dataset) == 10
    os.remove(filename)

    # test since and until
    since, until = "2022-07-18", "2022-07-19"
    TwitterScraper("ayam bakar", since=since, until=until).scrape(
        export="ayam",
        verbose=False,
        denied_users=["faraacademy"],
    )
    filename = os.path.join(output_dir, "scrape-ayam.csv")
    dataset = pd.read_csv(filename)
    dataset["date"] = pd.to_datetime(dataset["date"])
    assert (dataset["date"] >= since).all() and (dataset["date"] < until).all()
    os.remove(filename)
