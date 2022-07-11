import argparse
import csv
import json
import logging
import os
from datetime import datetime
from subprocess import PIPE, Popen
from typing import Sequence

from .scraper import TwitterScraper
from .utils import get_name

# Setup logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)


class NewScraper(TwitterScraper):
    def scrape(self, export: bool, filter: Sequence[str] = ["date", "content", "url"]) -> None:
        command = self._get_command()

        if export:
            path = os.path.join("..", "output")
            logging.info(f"Exporting to '{path}' directory")
            os.makedirs(path, exist_ok=True)
            name = get_name(os.path.join(path, f"test-{datetime.now().strftime('%d-%b-%Y')}.csv"))
            f = open(name, "w", encoding="utf-8")
            writer = csv.writer(f)
            writer.writerow(filter)

        logging.info("Scraping...")
        with Popen(command, stdout=PIPE, shell=True) as p:
            assert p.stdout is not None, "None stdout"
            for out in p.stdout:
                temp = json.loads(out)
                content = (
                    f"{temp['content'][:77]}..." if len(temp["content"]) > 80 else temp["content"]
                )
                print(f"{temp['date']} - {content}")

                if export:
                    writer.writerow([temp[x] for x in filter])

        if export:
            logging.info(f"Successfully Exported to {name}")
            f.close()

        logging.info("Done!")


def main() -> None:
    parser = argparse.ArgumentParser(description="Testing model dengan tweet baru")
    parser.add_argument("-q", "--query", help="Search query", type=str, default="vaksin covid")
    parser.add_argument("-n", "--max-results", help="Max number of tweet to scrape", type=int)
    parser.add_argument("-L", "--lang", help="Language", type=str, default="id")
    parser.add_argument("-S", "--since", help="Since", type=str)
    parser.add_argument("-U", "--until", help="Until", type=str)
    parser.add_argument("-e", "--export", help="Export to csv", action="store_true")

    args = parser.parse_args()
    logging.info("Starting script with params:")
    for arg, value in vars(args).items():
        print(f"   * {arg.title()}  : {value}")

    scraper = NewScraper(args.query, args.lang, args.max_results, args.since, args.until)
    scraper.scrape(args.export)


if __name__ == "__main__":
    main()
