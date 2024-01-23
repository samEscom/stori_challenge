from base64 import b64decode
from typing import Dict

from src.summary import Summary


def main(event, context) -> Dict:
    email = event["email"]
    file_csv = b64decode(event["body-json"]).decode("utf-8")

    summary = Summary(email, file_csv)
    summary.execute()
    email_id = summary.send_email()

    return {
        "emailId": email_id,
        "save": summary.save_flag,
        "lenData": summary.data_frame.shape[0],
        "summaryData": summary.summary_data,
    }
