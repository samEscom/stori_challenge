import re
from json import dumps, loads
from typing import Dict, Optional

from src.constans import ACCESS_KEY, EMAIL_PATTERN, POST_METHOD


class Params:
    def __init__(self, event: Dict):
        self.event = event
        self.email = str()
        self.file_name = str()
        self.headers = dict()
        self.http = dict()

        self.__set_params_body()
        self.__set_headers()
        self.__set_http()

    def __set_params_body(self) -> None:
        body = loads(self.event.get("body"))

        self.email = body.get("email")
        self.file_name = body.get("fileName")

    def __set_headers(self) -> None:
        self.headers = self.event["headers"]

    def __set_http(self) -> None:
        self.http = self.event.get("requestContext").get("http")

    def have_issues(self) -> Optional[Dict]:

        if self.file_name is None or self.email is None:
            return {
                "statusCode": 500,
                "body": dumps(
                    {
                        "message": "email or file name could not be empty",
                    }
                ),
            }

        if not re.match(EMAIL_PATTERN, self.email):
            return {
                "statusCode": 500,
                "body": dumps({"message": "invalid email"}),
            }

        if self.http.get("method") != POST_METHOD:
            return {
                "statusCode": 501,
                "body": dumps({"message": "method not allowed"}),
            }

        if self.headers.get("x-api-key") != ACCESS_KEY:
            return {
                "statusCode": 502,
                "body": dumps({"message": "user not allowed"}),
            }

        return None
