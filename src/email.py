from os import path
from typing import Dict

from jinja2 import Environment, FileSystemLoader


class Email:
    def __init__(self):
        self.template = Environment(
            loader=FileSystemLoader(
                path.join(path.dirname(__file__), "templates"), encoding="utf8"
            )
        )

    def create_template(self, params: Dict) -> str:
        template = self.template.get_template(
            "resume.htm",
        )
        return template.render(params=params)

    def send(self, email_str: str, message: str) -> int:

        __, _ = email_str, message

        return 0
