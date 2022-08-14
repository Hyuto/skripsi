import argparse
import csv
import json
import logging
import os
from subprocess import PIPE, Popen
from typing import Optional, Sequence

from scripts.scraper import TwitterScraper
from scripts.utils import get_name

# Setup logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)


class ModelScraper(TwitterScraper):
    def scrape(
        self,
        export: Optional[str] = None,
        filter: Sequence[str] = ["date", "content", "url"],
        verbose: bool = True,
    ) -> None:
        command = self._get_command()

        if export:
            logging.info(f"Exporting to 'output' directory")
            path = os.path.join(os.path.dirname(__file__), "..", "output")
            os.makedirs(path, exist_ok=True)
            filename = get_name(os.path.join(path, f"scrape-{export}.csv"))
            f = open(filename, "w", encoding="utf-8")
            writer = csv.writer(f)
            writer.writerow(filter)

        logging.info("Scraping...")
        with Popen(command, stdout=PIPE, shell=True) as p:
            assert p.stdout is not None, "None stdout"
            for out in p.stdout:
                temp = json.loads(out)
                if verbose:
                    content = repr(
                        f"{temp['content'][:77]}..."
                        if len(temp["content"]) > 80
                        else temp["content"]
                    )
                    print(f"{temp['date']} - {content}")

                if export:
                    writer.writerow([temp[x] for x in filter])

        if export:
            logging.info(f"Successfully Exported to {filename}")
            f.close()

        logging.info("Done!")
