from base64 import b64decode
from typing import Dict

from src.summary import Summary


def main(event, context) -> Dict:
    email = event["email"]
    file_csv = b64decode(event["body-json"]).decode("utf-8")

    summary = Summary(file_csv)

    summary.execute()
    email_id = summary.send_email(email)

    return {
        "emailId": email_id,
        "summary_data": summary.data.shape[0],
    }
