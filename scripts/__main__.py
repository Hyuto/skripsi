from typing import Optional

import typer

main = typer.Typer()


@main.command("scrape", help="Scrapping Twitter Data")
def scrape(
    query: str = typer.Argument(..., help="Search query"),
    lang: str = typer.Option("id", help="Language"),
    max_results: Optional[int] = typer.Option(None, help="Max number of tweet to scrape"),
    since: Optional[str] = typer.Option(None, help="Since"),
    until: Optional[str] = typer.Option(None, help="Until"),
    export: Optional[str] = typer.Option(None, help="Path to export"),
    verbose: bool = typer.Option(True, help="log all scraped tweets"),
) -> None:
    from scripts.scraper import TwitterScraper

    scraper = TwitterScraper(query, lang, max_results, since, until)
    scraper.scrape(export=export, verbose=verbose)


@main.command("model-test", help="Testing model dengan tweet baru")
def model_test(
    query: str = typer.Argument("vaksin covid", help="Search query"),
    lang: str = typer.Option("id", help="Language"),
    max_results: Optional[int] = typer.Option(None, help="Max number of tweet to scrape"),
    since: Optional[str] = typer.Option(None, help="Since"),
    until: Optional[str] = typer.Option(None, help="Until"),
    export: Optional[str] = typer.Option(None, help="Path to export"),
    verbose: bool = typer.Option(True, help="log all scraped tweets"),
) -> None:
    from scripts.model_tester import TestScraper

    scraper = TestScraper(query, lang, max_results, since, until)
    scraper.scrape(export=export, verbose=verbose)


main()
