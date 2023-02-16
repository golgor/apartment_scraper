import requests
import willhaben
from requester import get_request


def request_willhaben() -> requests.Response:
    wh = willhaben.RequestObject()
    return get_request(wh)


def parse_willhaben():
    pass


def main():
    pass


if __name__ == "__main__":
    main()
