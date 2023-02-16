import requests
from requester import get_request
from willhaben.request import WillhabenRequestObject


def request_willhaben() -> requests.Response:
    wh = WillhabenRequestObject()
    return get_request(wh)


def main():
    pass


if __name__ == "__main__":
    main()
