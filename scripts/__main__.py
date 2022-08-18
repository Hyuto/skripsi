from typing import Optional

import typer

main = typer.Typer()


@main.command("scrape", help="Scrapping twitter berdasarkan query yang diberikan")
def scrape(
    query: str = typer.Argument(..., help="Query pencarian tweet"),
    lang: str = typer.Option("id", help="Bahasa"),
    max_results: Optional[int] = typer.Option(None, help="Banyak tweet maksimal yang discrape"),
    since: Optional[str] = typer.Option(None, help="Since (batasan awal tanggal tweet)"),
    until: Optional[str] = typer.Option(None, help="Until (batasan akhir tanggal tweet)"),
    export: Optional[str] = typer.Option(None, help="Nama file untuk export tweet hasil scrape"),
    verbose: bool = typer.Option(True, help="Logging setiap tweet yang discrape"),
) -> None:
    from scripts.scraper import TwitterScraper

    scraper = TwitterScraper(query, lang, max_results, since, until)
    scraper.scrape(export=export, verbose=verbose)


@main.command("model-test", help="Testing model dengan tweet baru")
def model_test(
    query: str = typer.Argument("vaksin covid", help="Query pencarian tweet"),
    lang: str = typer.Option("id", help="Bahasa"),
    max_results: Optional[int] = typer.Option(None, help="Banyak tweet maksimal yang discrape"),
    since: Optional[str] = typer.Option(None, help="Since (batasan awal tanggal tweet)"),
    until: Optional[str] = typer.Option(None, help="Until (batasan akhir tanggal tweet)"),
    export: Optional[str] = typer.Option(None, help="Nama file untuk export tweet hasil scrape"),
    verbose: bool = typer.Option(True, help="Logging setiap tweet yang discrape"),
) -> None:
    from scripts.model_tester import ModelScraper

    scraper = ModelScraper(query, lang, max_results, since, until)
    scraper.scrape(export=export, verbose=verbose)


main()
