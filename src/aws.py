from typing import Any, Dict, List, Union

import boto3
from botocore.client import Config

from src.constans import (
    AWS_REGION_EAST,
    AWS_SERVICE_DYNAMO,
    AWS_SERVICE_S3,
    AWS_SERVICE_SES,
    BUCKET_NAME,
    TABLE_NAME,
)


class Aws:
    @staticmethod
    def get_client(service: str):
        return boto3.client(
            service,
            region_name=AWS_REGION_EAST,
            config=Config(signature_version="s3v4"),
        )

    def send_email(self, email_from: str, emails_to: List[str], data: str) -> str:
        try:
            client = self.get_client(AWS_SERVICE_SES)
            resp = client.send_raw_email(
                Source=email_from, Destinations=emails_to, RawMessage={"Data": data}
            )
            return resp["MessageId"]
        except Exception:
            raise

    def save_data(self, summary: Dict) -> Union[int, str]:
        try:
            dynamodb = self.get_client(AWS_SERVICE_DYNAMO)
            response = dynamodb.put_item(TableName=TABLE_NAME, Item=summary)
            return response["ResponseMetadata"]["HTTPStatusCode"] == 200

        except Exception:
            raise

    def get_csv_file(self, file_name: str) -> Any:
        try:
            s3 = self.get_client(AWS_SERVICE_S3)
            response = s3.get_object(Bucket=BUCKET_NAME, Key=file_name)

            return response["Body"].read()

        except Exception:
            raise
