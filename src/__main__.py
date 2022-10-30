import glob
import logging
import os
import shutil
from typing import List, Optional

import typer

# Setup logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)

# Setup typer
main = typer.Typer(add_completion=False)


@main.command("scrape", help="Scrapping twitter berdasarkan query yang diberikan")
def scrape(
    query: str = typer.Argument(..., help="Query pencarian tweet"),
    lang: str = typer.Option("id", help="Bahasa"),
    max_results: Optional[int] = typer.Option(None, help="Banyak tweet maksimal yang discrape"),
    since: Optional[str] = typer.Option(
        None, help="Since (batasan awal tanggal tweet) [isoformated date string]"
    ),
    until: Optional[str] = typer.Option(
        None, help="Until (batasan akhir tanggal tweet) [isoformated date string]"
    ),
    export: Optional[str] = typer.Option(None, help="Nama file untuk export tweet hasil scrape"),
    add_features: Optional[str] = typer.Option(
        None, help='Menambahkan feature yang akan diexport dalam file csv [string separated by ","]'
    ),
    denied_users: Optional[str] = typer.Option(
        os.path.join(os.path.dirname(__file__), "..", "data", "denied-users.json"),
        help=(
            "List user yang tweetnya diabaikan [pathlike string ke file list user "
            + '(json formated) atau Sequance separated by ","]'
        ),
    ),
    verbose: bool = typer.Option(True, help="Logging setiap tweet yang discrape"),
) -> None:
    add_features = add_features.split(",") if add_features else []  # type: ignore
    if denied_users:
        if not os.path.exists(denied_users):
            denied_users = denied_users.split(",")  # type: ignore

    logging.info("Starting scrape commands with args:")
    args = locals()
    for k, v in args.items():
        print(f"  * {k} : {v}")

    from src.scraper import TwitterScraper

    scraper = TwitterScraper(query, lang, since, until)
    scraper.scrape(
        export=export,
        add_features=add_features,  # type: ignore
        denied_users=denied_users,
        max_result=max_results,
        verbose=verbose,
    )


@main.command("model-test", help="Testing model dengan tweet baru")
def model_test(
    query: str = typer.Argument("vaksin covid", help="Query pencarian tweet"),
    lang: str = typer.Option("id", help="Bahasa"),
    max_results: Optional[int] = typer.Option(None, help="Banyak tweet maksimal yang discrape"),
    since: Optional[str] = typer.Option(
        None, help="Since (batasan awal tanggal tweet) [isoformated date string]"
    ),
    until: Optional[str] = typer.Option(
        None, help="Until (batasan akhir tanggal tweet) [isoformated date string]"
    ),
    export: Optional[str] = typer.Option(None, help="Nama file untuk export tweet hasil scrape"),
    add_features: Optional[str] = typer.Option(
        None, help='Menambahkan feature yang akan diexport dalam file csv [string separated by ","]'
    ),
    denied_users: Optional[str] = typer.Option(
        os.path.join(os.path.dirname(__file__), "..", "data", "denied-users.json"),
        help=(
            "List user yang tweetnya diabaikan [pathlike string ke file list user "
            + '(json formated) atau Sequance separated by ","]'
        ),
    ),
    verbose: bool = typer.Option(True, help="Logging setiap tweet yang discrape"),
) -> None:
    add_features = add_features.split(",") if add_features else []  # type: ignore
    if denied_users:
        if not os.path.exists(denied_users):
            denied_users = denied_users.split(",")  # type: ignore

    logging.info("Starting scrape commands with args:")
    args = locals()
    for k, v in args.items():
        print(f"  * {k} : {v}")

    from src.scraper import TwitterScraper

    scraper = TwitterScraper(query, lang, since, until)
    scraper.scrape(
        export=export,
        add_features=add_features,  # type: ignore
        denied_users=denied_users,
        max_result=max_results,
        verbose=verbose,
    )


@main.command("clean", help="Membersihkan project directory")
def clean_up(
    clear: bool = typer.Option(False, help="Menghapus semua folder cache"),
    verbose: bool = typer.Option(True, help="Logging setiap tweet yang discrape"),
) -> None:
    main_dir = os.path.join(os.path.dirname(__file__), "..")
    cache_dir = [".mypy_cache", ".pytest_cache", "./**/__pycache__"]
    additional_dir = ["output", "./**/.ipynb_checkpoints"]
    cache_file = [".coverage"]
    additional_file: List[str] = []

    def delete(folder: bool, iterator: List[str]) -> None:
        # loop through
        for x in iterator:
            glob_dirs = glob.glob(os.path.join(main_dir, x))
            for path in glob_dirs:
                try:
                    if verbose:
                        logging.info(f"Deleting : {path}")
                    if folder:
                        shutil.rmtree(path)
                    else:
                        os.remove(path)
                except:
                    logging.error(f"Error on deleting : {path}")

    directory = cache_dir + additional_dir if clear else cache_dir
    delete(folder=True, iterator=directory)
    files = cache_file + additional_file if clear else cache_file
    delete(folder=False, iterator=files)

    logging.info("Done!")


main()
