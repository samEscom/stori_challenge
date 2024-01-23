from typing import Any, Dict, List, Union

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError, NoCredentialsError

from src.constans import AWS_REGION_EAST, AWS_SERVICE_S3, AWS_SERVICE_SES, BUCKET_NAME


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
        except Exception as e:
            return str(e)

    def save_data(self, summary: Dict) -> Union[int, str]:
        try:
            dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION_EAST)
            table = dynamodb.Table("summaries")
            response = table.put_item(Item=summary)

            return response["ResponseMetadata"]["HTTPStatusCode"]

        except ClientError as err:
            return str(err.response["Error"]["Code"], err.response["Error"]["Message"])

        except NoCredentialsError as err:
            return str(err)

    def get_csv_file(self, file_name: str) -> Any:
        try:
            s3 = self.get_client(AWS_SERVICE_S3)
            response = s3.get_object(Bucket=BUCKET_NAME, Key=file_name)

            return response["Body"].read()

        except Exception as e:
            raise RuntimeError(f"[Error] : error leyendo el archivo {str(e)}")
