"""Script untuk generate command dan memanggil `snscrape` yang digunakan untuk scraping suatu topik
   di twitter"""

import csv
import json
import logging
import os
from subprocess import PIPE, Popen
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from scripts.utils import datetime_validator, get_name, kill_proc_tree

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
        since: Optional[str] = None,
        until: Optional[str] = None,
    ) -> None:
        self.query = query
        self.lang = lang
        if since:
            datetime_validator(since)
        self.since = since
        if until:
            datetime_validator(until)
        self.until = until

    def _get_command(self) -> str:
        """Mengenerate command yang akan diberikan pada `snscrape`

        Returns:
            str: command
        """
        global_options = ["--jsonl"]
        if self.since:
            global_options.append(f"--since {self.since}")
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

    def _flatten(
        self, nested_d: Dict[str, Any], parent_key: str = "", sep: str = "."
    ) -> Dict[str, Any]:
        items = []  # type: List[Tuple[str, Any]]
        for k, v in nested_d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, Dict):
                items.extend(self._flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def _denied_users_handler(self, denied_users: Union[Sequence[str], str]) -> Sequence[str]:
        if type(denied_users) == str:
            assert os.path.exists(denied_users), "File not exist!!"
            with open(denied_users) as reader:
                users = json.load(reader)  # type: Sequence[str]
            return users
        elif isinstance(denied_users, Sequence):
            return denied_users
        else:  # pragma: no cover
            raise TypeError("Expected pathlike string or Sequence on denied_users!")

    def scrape(
        self,
        add_features: Sequence[str] = [],
        denied_users: Optional[Union[str, Sequence[str]]] = None,
        max_result: Optional[int] = None,
        export: Optional[str] = None,
        verbose: bool = True,
    ) -> None:
        """Running scraping dengan `snscrape`

        Args:
            add_features (Sequence[str]): Menambahkan filter kolom yang akan diexport.
                Defaults to [].
            denied_users (Optional[Union[str, Sequence[str]]]): List user yang tweetnya dapat
                dihiraukan. Dapat berupa pathlike string ke file tempat list user disimpan
                (json format) atau berupa sequence. Defaults to None.
            max_result (Optional[int]): Jumlah maksimal tweet yang di scrape. Defaults to None.
            export (Optional[str]): Nama file tempat table diexport pada direktori `output`.
                Jika `None` maka table hasil scraping tidak akan diexport. Defaults to None.
            verbose (bool): Tampilkan tweet yang di scrape di terminal. Defaults to True.
        """
        command = self._get_command()
        filters = ["date", "url", "user.username", *add_features, "content"]
        if denied_users is not None:
            denied_users = self._denied_users_handler(denied_users)

        if export is not None:
            logging.info(f"Exporting to 'output' directory")
            path = os.path.join(os.path.dirname(__file__), "..", "output")
            os.makedirs(path, exist_ok=True)
            filename = get_name(os.path.join(path, f"scrape-{export}.csv"))
            f = open(filename, "w", encoding="utf-8")
            writer = csv.writer(f)
            writer.writerow(filters)

        logging.info("Scraping...")
        snscrape = Popen(command, stdout=PIPE, shell=True)
        assert snscrape.stdout is not None, "None stdout"

        index = 1
        for out in snscrape.stdout:
            temp = self._flatten(json.loads(out))

            if denied_users is not None:  # filter username
                if temp["user.username"] in denied_users:
                    continue

            if verbose:  # logging output
                content = repr(
                    f"{temp['content'][:67]}..." if len(temp["content"]) > 70 else temp["content"]
                )
                print(f"{index} - {temp['date']} - {temp['user.username']} - {content}")

            if export:  # write row
                row = [temp[x] for x in filters]
                writer.writerow(row)

            if max_result:  # brake and kill subprocess
                if index >= max_result:
                    kill_proc_tree(snscrape.pid)
                    break
            index += 1

        if export:
            logging.info(f"Successfully Exported to {filename}")
            f.close()

        logging.info("Done!")
