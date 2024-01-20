from base64 import b64encode

import boto3

from index import handler

from .mocks.boto3_client import Boto3ClienMock


def mock_boto3client_success(_, **kwargs):
    return Boto3ClienMock(
        _,
        mock_data={
            "send_raw_email": {
                "raise_exception": False,
                "response": {"MessageId": "12345678"},
            },
        },
    )


def test_reminders(monkeypatch):

    file_upload = open("example.csv")
    file_encoded = b64encode(bytes(file_upload.read(), "utf-8"))
    file_upload.close()

    monkeypatch.setattr(boto3, "client", mock_boto3client_success)

    response = handler(
        event={"email": "sa5m.escom@gmail.com", "body-json": file_encoded},
        context=None,
    )

    assert response["emailId"] == "12345678"
    assert response["lenData"] == 4
    assert isinstance(response["resume"], dict)
    assert response["resume"]["totalBalance"] == 39.74
    assert response["resume"]["averageCreditAmount"] == 35.25
    assert response["resume"]["averageDebitAmount"] == -15.38
    assert isinstance(response["resume"]["transactionsByMonths"], list)
