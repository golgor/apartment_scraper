import json
from datetime import datetime
from time import sleep

import willhaben

from apartment_scraper import pkg_path


def main():
    pass


if __name__ == "__main__":
    wh = willhaben.Requester()
    today = datetime.now().strftime("%Y-%m-%d")
    test = []
    for data in wh:
        sleep(1)
        test.extend(data)

    filepath = pkg_path.joinpath("data", f"willhaben_{today}.json")
    with open(filepath, "w") as f:
        f.write(json.dumps(test, indent=2))
        print(f"Successfully saved {len(test)}")
