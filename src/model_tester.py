import csv
import json
import logging
import os
from subprocess import PIPE, Popen
from typing import Optional, Sequence, Union

from src.model import Model
from src.preprocessing import preprocessing
from src.scraper import TwitterScraper
from src.utils import get_name, kill_proc_tree

# Setup logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)


class ModelScraper(TwitterScraper):
    """Model scrapper.

    Args:
        model (str): Model path.
        query (str): Search query. Defaults to "vaksin (corona OR covid)".
        lang (str): Language. Defaults to "id".
        since (Optional[str]): Since [string isoformated datetime]. Defaults to None.
        until (Optional[str]): Until [string isoformated datetime]. Defaults to None.
    """

    def __init__(
        self,
        model: str,
        query: str = "vaksin (corona OR covid)",
        lang: str = "id",
        since: Optional[str] = None,
        until: Optional[str] = None,
    ) -> None:
        super().__init__(query, lang, since, until)
        self.model = Model(model)

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
            writer.writerow(filters + ["p_emotions"])

        logging.info("Scraping...")
        snscrape = Popen(command, stdout=PIPE, shell=True)
        assert snscrape.stdout is not None, "None stdout"

        index = 1
        for out in snscrape.stdout:
            temp = self._flatten(json.loads(out))

            if denied_users is not None:  # filter username
                if temp["user.username"] in denied_users:  # pragma: no cover
                    continue

            prediction = self.model.predict(preprocessing(temp["content"]))

            if verbose:  # logging output
                content = repr(
                    f"{temp['content'][:67]}..." if len(temp["content"]) > 69 else temp["content"]
                )
                print(
                    f"{index} - {temp['date']} - {temp['user.username']} - "
                    + f"{content} - {prediction[0][0]}"
                )

            if export:  # write row
                row = [temp[x] for x in filters] + [prediction[0][0]]
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
