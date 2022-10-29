import csv
import json
import logging
import os
from subprocess import PIPE, Popen
from typing import Optional, Sequence, Union

from src.scraper import TwitterScraper
from src.utils import get_name, kill_proc_tree

# Setup logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)


class ModelScraper(TwitterScraper):
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
            denied_users = self._denied_users_handler(denied_users)  # pragma: no cover

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
                if temp["user.username"] in denied_users:  # pragma: no cover
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
