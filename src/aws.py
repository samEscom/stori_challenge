from typing import Dict, List, Union

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError, NoCredentialsError

from src.constans import AWS_REGION_EAST, AWS_SERVICE_SES


class Aws:
    @staticmethod
    def get_client(service: str):
        return boto3.client(
            service,
            region_name=AWS_REGION_EAST,
            config=Config(signature_version="s3v4"),
        )

    def send_email(self, email_from: str, emails_to: List[str], data: str) -> str:
        client = self.get_client(AWS_SERVICE_SES)
        try:
            resp = client.send_raw_email(
                Source=email_from, Destinations=emails_to, RawMessage={"Data": data}
            )
            return resp["MessageId"]
        except Exception as e:
            return str(e)

    def save_data(self, summary: Dict) -> Union[int, str]:
        dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION_EAST)

        try:
            table = dynamodb.Table("summaries")
            response = table.put_item(Item=summary)

            return response["ResponseMetadata"]["HTTPStatusCode"]

        except ClientError as err:
            return str(err.response["Error"]["Code"], err.response["Error"]["Message"])

        except NoCredentialsError as err:
            return str(err)
