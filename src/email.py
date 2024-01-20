import io
from email.charset import BASE64, Charset
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.text import MIMEText
from os import path
from typing import Dict, Optional

from jinja2 import Environment, FileSystemLoader

from src.aws import Aws
from src.constans import NAME_FILE, SENDER


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

    @staticmethod
    def add_document(csv, filename: str) -> any:
        cs = Charset("utf-8")
        cs.body_encoding = BASE64

        attachment = MIMENonMultipart("text", "csv", charset="utf-8")
        report = {"content": csv.getvalue(), "filename": f"{filename}.csv"}
        attachment.add_header(
            "Content-Disposition", "attachment", filename=report["filename"]
        )
        attachment.set_payload(report["content"], charset=cs)
        return attachment

    def prepare(self, data_frame, message_str, email_to) -> str:
        message = MIMEMultipart()
        message["Subject"] = "Envio de resumen"

        message["From"] = SENDER
        message["To"] = email_to

        part = MIMEText(message_str, "html")
        message.attach(part)

        cs = Charset("utf-8")
        cs.body_encoding = BASE64

        csv_buffer = io.StringIO()
        data_frame.to_csv(csv_buffer, encoding="utf-8")

        filename = NAME_FILE
        attachment = self.add_document(csv_buffer, filename)
        csv_buffer.close()
        message.attach(attachment)
        return message.as_string()

    def send(self, data_frame, email_to_str: str, message: str) -> Optional[str]:

        aws = Aws()
        message_prepare = self.prepare(data_frame, message, email_to_str)
        message_id = aws.send_email(SENDER, [email_to_str], message_prepare)
        return message_id
