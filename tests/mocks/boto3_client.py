from typing import Dict


class Boto3ClienMock:
    def __init__(self, _, **kwargs) -> None:
        self.mock_data = kwargs["mock_data"]

    def send_raw_email(self, **kwargs) -> Dict:
        data = self.mock_data["send_raw_email"]
        if data.get("raise_exception"):
            raise "Mock AWS Exception"
        return data.get("response", {})

    def get_object(self, **kwargs) -> Dict:
        data = self.mock_data["get_object"]
        if data.get("raise_exception"):
            raise "Mock AWS Exception"
        return data.get("response", {})

    def put_item(self, **kwargs) -> Dict:
        data = self.mock_data["put_item"]
        if data.get("raise_exception"):
            raise "Mock AWS Exception"
        return data.get("response", {})
