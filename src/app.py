from json import dumps
from typing import Dict

from src.params import Params
from src.summary import Summary


def main(event, context) -> Dict:

    params = Params(event)

    issue = params.have_issues()

    if issue is not None:
        return issue

    try:
        summary = Summary(params.email, params.file_name)
        summary.execute()
        email_id = summary.send_email()

        return {
            "statusCode": 200,
            "body": dumps(
                {
                    "emailId": email_id,
                    "save": summary.save_flag,
                    "lenData": summary.data_frame.shape[0],
                    "summaryData": summary.summary_data,
                }
            ),
        }

    except Exception as e:
        return {
            "statusCode": 400,
            "body": dumps(
                {
                    "error": str(e),
                }
            ),
        }
