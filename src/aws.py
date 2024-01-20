from typing import List, Optional

import boto3
from botocore.client import Config

from src.constans import AWS_REGION_WEST, AWS_SERVICE_SES


class Aws:
    @staticmethod
    def get_client(service: str):
        return boto3.client(
            service,
            region_name=AWS_REGION_WEST,
            config=Config(signature_version="s3v4"),
        )

    def send_email(
        self, email_from: str, emails_to: List[str], data: str
    ) -> Optional[str]:
        client = self.get_client(AWS_SERVICE_SES)
        try:
            resp = client.send_raw_email(
                Source=email_from, Destinations=emails_to, RawMessage={"Data": data}
            )
            return resp["MessageId"]
        except Exception as e:
            print(e)
            return None
