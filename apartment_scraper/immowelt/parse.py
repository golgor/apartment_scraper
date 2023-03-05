from typing import Any


class FieldParser:
    def __init__(self, response: dict[str, Any]):
        self.response = response

    @property
    def price(self) -> float:
        try:
            if price_range := self.response["primaryPrice"]:
                return float(price_range["amountMin"])
            raise ValueError
        except Exception:
            print(
                "Failed to parse the field 'PRICE' for "
                f"id={self.response['id']}, "
                f"url={self.url}"
            )
            return 0

    @property
    def area(self) -> float:
        try:
            if primary_area := self.response["primaryArea"]:
                return primary_area["sizeMin"]
            raise ValueError
        except Exception:
            print(
                "Failed to parse the field 'Area' for "
                f"id={self.response['id']}, "
                f"url={self.url}"
            )
            return 0

    @property
    def url(self) -> str:
        return f"https://www.immowelt.at/expose/{self.response['onlineId']}"

    @property
    def postcode(self) -> str:
        return self.response.get("place", "")

    @property
    def rooms(self) -> int:
        return self.response.get("roomsMin", 0)

    @property
    def id(self) -> str:
        return self.response["id"]


def parse_immowelt_response(raw_data: list[dict[str, Any]]):
    raise NotImplementedError
    # estates: list[dict[str, Any]] = list(
    #     filter(lambda x: x["itemType"] == "ESTATE", raw_data)
    # )
    # apartment_list: list[Apartment] = []

    # for estate in estates:
    #     # try:
    #     parser = FieldParser(estate)
    #     apartment_list.append(
    #         Apartment(
    #             id=parser.id,
    #             price=parser.price,
    #             area=parser.area,
    #             url=parser.url,
    #             post_code=parser.postcode,
    #             rooms=parser.rooms,
    #             floor=0,
    #         )
    #     )
    # return apartment_list
