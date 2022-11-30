from pathlib import Path

import pandas as pd
from src.scraper import TwitterScraper

main_dir = Path(__file__).parents[1]


def test_TwitterScraper():
    output_dir = main_dir / "output"

    # test max_result
    TwitterScraper("minyak").scrape(
        export="minyak",
        max_result=10,
        denied_users=(main_dir / "data" / "denied-users.json").as_posix(),
    )
    filename = output_dir / "scrape-minyak.csv"
    dataset = pd.read_csv(filename.as_posix())
    assert len(dataset) == 10
    filename.unlink(missing_ok=True)

    # test since and until
    since, until = "2022-07-18", "2022-07-19"
    TwitterScraper("ayam bakar", since=since, until=until).scrape(export="ayam", verbose=False)
    filename = output_dir / "scrape-ayam.csv"
    dataset = pd.read_csv(filename.as_posix())
    dataset["date"] = pd.to_datetime(dataset["date"])
    assert (dataset["date"] >= since).all() and (dataset["date"] < until).all()
    filename.unlink(missing_ok=True)
