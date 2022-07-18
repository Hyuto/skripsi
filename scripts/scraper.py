import argparse
import csv
import json
import logging
import os
from datetime import datetime
from subprocess import PIPE, Popen
from typing import Optional, Sequence

from .utils import get_name

# Setup logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)


class TwitterScraper:
    crawler = "snscrape"
    scraper = "twitter-search"

    def __init__(
        self,
        query: str,
        lang: str = "id",
        max_result: Optional[int] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        json: bool = True,
    ) -> None:
        self.query = query
        self.lang = lang
        self.max_result = max_result
        self.since = since
        self.until = until
        self.json = json

    def _get_command(self) -> str:
        global_options = []
        if self.json:
            global_options.append("--jsonl")
        if self.since:
            global_options.append(f"--since {self.since}")
        if self.max_result:
            global_options.append(f"--max-results {self.max_result}")
        new_global_options = " ".join(global_options)

        scrapper_options = [
            self.query,
            f"lang:{self.lang}",
            "exclude:nativeretweets",
            "exclude:retweets",
        ]
        if self.until:
            scrapper_options.append(f"until:{self.until}")
        new_scrapper_options = " ".join(scrapper_options)

        return f'{self.crawler} {new_global_options} {self.scraper} "{new_scrapper_options}"'

    def scrape(self, export: bool, filter: Sequence[str] = ["date", "content", "url"]) -> None:
        command = self._get_command()

        if export:
            path = os.path.join(os.path.dirname(__file__), "..", "output")
            logging.info("Exporting to 'output' directory")
            os.makedirs(path, exist_ok=True)
            name = get_name(os.path.join(path, f"scrape-{datetime.now().strftime('%d-%b-%Y')}.csv"))
            f = open(name, "w", encoding="utf-8")
            writer = csv.writer(f)
            writer.writerow(filter)

        logging.info("Scraping...")
        with Popen(command, stdout=PIPE, shell=True) as p:
            assert p.stdout is not None, "None stdout"

            index = 1
            for out in p.stdout:
                temp = json.loads(out)
                content = (
                    f"{temp['content'][:77]}..." if len(temp["content"]) > 80 else temp["content"]
                )
                print(f"{index} - {temp['date']} - {content}")

                if export:
                    writer.writerow([temp[x] for x in filter])
                index += 1

        if export:
            logging.info(f"Successfully Exported to {name}")
            f.close()

        logging.info("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrapping Twitter Data")
    parser.add_argument("-q", "--query", help="Search query", type=str)
    parser.add_argument("-n", "--max-results", help="Max number of tweet to scrape", type=int)
    parser.add_argument("-L", "--lang", help="Language", type=str, default="id")
    parser.add_argument("-S", "--since", help="Since", type=str)
    parser.add_argument("-U", "--until", help="Until", type=str)
    parser.add_argument("-e", "--export", help="Export to csv", action="store_true")

    args = parser.parse_args()
    logging.info("Starting script with params:")
    for arg, value in vars(args).items():
        print(f"   * {arg}  : {value}")

    scraper = TwitterScraper(args.query, args.lang, args.max_results, args.since, args.until)
    scraper.scrape(args.export)
