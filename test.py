import argparse, os
import twint, logging
from datetime import datetime

# Setup logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)


def crawl(search, export):
    logging.info("Starting script with params:")
    logging.info(f"   * Query  : {search}")
    logging.info(f"   * Export : {export}")

    c = twint.Config()
    c.Search = search
    c.Filter_retweets = True
    c.Lang = "id"
    c.Store_csv = True

    if export:
        path = "./output"
        if not os.path.isdir(path):
            os.mkdir(path)
        c.Output = os.path.join(path, f"crawl-{datetime.now().strftime('%d-%b-%Y')}.csv")

    twint.run.Search(c)


def main():
    parser = argparse.ArgumentParser(description="Testing model dengan tweet baru")
    parser.add_argument("-q", "--query", help="Search query", type=str, default="vaksin covid")
    parser.add_argument("-e", "--export", help="Export to csv", action="store_true")

    args = parser.parse_args()
    data = crawl(args.query, args.export)


if __name__ == "__main__":
    main()
