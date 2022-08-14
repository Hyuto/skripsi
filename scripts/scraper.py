"""Script untuk generate command dan memanggil `snscrape` yang digunakan untuk scraping suatu topik
   di twitter"""

import argparse
import csv
import json
import logging
import os
from subprocess import PIPE, Popen
from typing import Optional, Sequence

from scripts.utils import get_name

# Setup logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)


class TwitterScraper:
    """Scrapping twitter berdasarkan query yang diberikan.

    Examples:
        Scraping spesifik topik

        >>> scraper = TwitterScraper(query="minyak")
        >>> scraper.scrape()
        [ INFO ] Scraping...
        1 - 2022-08-01T16:39:41+00:00 - @gerundghast im broke. harga minyak no joke rn
        2 - 2022-08-01T16:39:17+00:00 - @beaulitude Minyak mahal jadi gimana kalo direbus? https://t.co/MnmgY4iNPs
        3 - 2022-08-01T16:39:13+00:00 - @Damsllette ak blm nemu enakny dmna 😭😭 biasa pke minyak angin doang
        ...
    """

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
        """Mengenerate command yang akan diberikan pada `snscrape`

        Returns:
            str: command
        """
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

    def scrape(
        self,
        export: Optional[str] = None,
        filter: Sequence[str] = ["date", "content", "url"],
        verbose: bool = True,
    ) -> None:
        """Running scraping dengan `snscrape`

        Args:
            export (Optional[str]): Nama file tempat table diexport pada direktori `output`.
                Jika `None` maka table hasil scraping tidak akan diexport. Defaults to None.
            filter (Sequence[str]): Filter kolom yang akan diexport. Kolom yang tersedia yaitu.
                Defaults to ["date", "content", "url"].
            verbose (bool): Tampilkan tweet yang di scrape di terminal. Defaults to True.
        """
        command = self._get_command()

        if export is not None:
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

            index = 1
            for out in p.stdout:
                temp = json.loads(out)
                if verbose:
                    content = repr(
                        f"{temp['content'][:77]}..."
                        if len(temp["content"]) > 80
                        else temp["content"]
                    )
                    print(f"{index} - {temp['date']} - {content}")

                if export:
                    writer.writerow([temp[x] for x in filter])
                index += 1

        if export:
            logging.info(f"Successfully Exported to {filename}")
            f.close()

        logging.info("Done!")
