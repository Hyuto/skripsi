import logging
import os
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

    from scripts.scraper import TwitterScraper

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

    from scripts.scraper import TwitterScraper

    scraper = TwitterScraper(query, lang, since, until)
    scraper.scrape(
        export=export,
        add_features=add_features,  # type: ignore
        denied_users=denied_users,
        max_result=max_results,
        verbose=verbose,
    )


main()
