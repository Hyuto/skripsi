import argparse, os
import twint, logging
from datetime import datetime

# Setup logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO)


def crawl(search, n, export):
    logging.info("Starting script with params:")
    logging.info(f"   * Query  : {search}")
    logging.info(f"   * Export : {export}")

    c = twint.Config()
    c.Search = search
    c.Filter_retweets = True
    c.Limit = n
    c.Lang = "id"
    c.Store_pandas = True

    logging.info("Crawling Tweets\n")
    twint.run.Search(c)

    if export:
        logging.info("Exporting to './output' directory")
        path = "./output"
        if not os.path.isdir(path):
            os.mkdir(path)
        df = twint.storage.panda.Tweets_df
        df.to_csv(
            os.path.join(path, f"crawl-{datetime.now().strftime('%d-%b-%Y')}.csv"),
            index=False,
        )

    logging.info("Done!")


def main():
    parser = argparse.ArgumentParser(description="Testing model dengan tweet baru")
    parser.add_argument("-q", "--query", help="Search query", type=str, default="vaksin covid")
    parser.add_argument("-e", "--export", help="Export to csv", action="store_true")
    parser.add_argument("-n", "--number", help="n tweet to crawl", type=int, default=100)

    args = parser.parse_args()
    data = crawl(args.query, args.number, args.export)


if __name__ == "__main__":
    main()
