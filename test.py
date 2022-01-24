import argparse, os
import logging, json
from scraper import TwitterScraper
from subprocess import Popen, PIPE
from datetime import datetime

# Setup logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)


def get_name(path):
    filename, extension = os.path.splitext(path)

    if not os.path.isfile(path):
        return path
    else:
        index = 1
        while True:
            new_name = f"{filename} ({index}){extension}"

            if not os.path.isfile(new_name):
                return new_name
            else:
                index += 1


class NewScraper(TwitterScraper):
    def scrape(self, export):
        command = self._get_command()
        with Popen(command, stdout=PIPE) as p:
            for out in p.stdout:
                temp = json.loads(out)
                content = (
                    f"{temp['content'][:77]}..." if len(temp["content"]) > 80 else temp["content"]
                )
                print(f"{temp['date']} - {content}")

        if export:
            logging.info("Exporting to './output' directory")
            path = "./output"
            if not os.path.isdir(path):
                os.mkdir(path)
            name = get_name(os.path.join(path, f"crawl-{datetime.now().strftime('%d-%b-%Y')}.csv"))

        logging.info("Done!")


def main():
    parser = argparse.ArgumentParser(description="Testing model dengan tweet baru")
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

    scraper = NewScraper(args.query, args.lang, args.max_results, args.since, args.until)
    scraper.scrape(args.export)


if __name__ == "__main__":
    main()
