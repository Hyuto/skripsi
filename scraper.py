import argparse, os
import logging, json
from subprocess import Popen, PIPE
from datetime import datetime

# Setup logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)


class TwitterScraper:
    crawler = "snscrape"
    scraper = "twitter-search"

    def __init__(self, query, lang="id", max_result=None, since=None, until=None, json=True):
        self.query = query
        self.lang = lang
        self.max_result = max_result
        self.since = since
        self.until = until
        self.json = json

    def _get_command(self):
        global_options = []
        if self.json:
            global_options.append("--jsonl")
        if self.since:
            global_options.append(f"--since {self.since}")
        if self.max_result:
            global_options.append(f"--max-results {self.max_result}")
        global_options = " ".join(global_options)

        scrapper_options = [self.query, f"lang:{self.lang}"]
        if self.until:
            scrapper_options.append(f"until:{self.until}")
        scrapper_options = " ".join(scrapper_options)

        return f'{self.crawler} {global_options} {self.scraper} "{scrapper_options}"'

    def scrape(self):
        command = self._get_command()
        data = []
        with Popen(command, stdout=PIPE) as p:
            index = 1
            for b in p.stdout:
                temp = json.loads(b)
                content = (
                    f"{temp['content'][:77]}..." if len(temp["content"]) > 80 else temp["content"]
                )
                print(f"{index} - {temp['date']} - {content}")

                index += 1
                data.append(temp)
        return data


def main():
    parser = argparse.ArgumentParser(description="Scrapping Twitter Data")
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

    scraper = TwitterScraper(args.query, args.lang, args.max_results, args.since, args.until)
    scraper.scrape()


if __name__ == "__main__":
    main()
