from datetime import datetime
from io import BytesIO

import boto3
import pytest
from botocore.response import StreamingBody

from index import handler

from .mocks.boto3_client import Boto3ClienMock

file_upload = open("example.csv")
file_s3 = bytes(file_upload.read(), "utf-8")
raw_stream = StreamingBody(BytesIO(file_s3), len(file_s3))
file_upload.close()

mock_data = {
    "send_raw_email": {
        "raise_exception": False,
        "response": {"MessageId": "12345678"},
    },
    "get_object": {
        "raise_exception": False,
        "response": {
            "ResponseMetadata": {
                "RequestId": "6BFC00970E62BC8F",
                "HTTPStatusCode": 200,
                "RetryAttempts": 1,
            },
            "LastModified": str(datetime(2024, 1, 29, 5, 39, 29)),
            "ContentLength": 58,
            "ETag": '"6299528715bad0e3510d1e4c4952ee7e"',
            "ContentType": "binary/octet-stream",
            "Metadata": {},
            "Body": raw_stream,
        },
    },
}


def test_index_success(monkeypatch):
    def mock_boto3client_success(_, **kwargs):
        return Boto3ClienMock(_, mock_data=mock_data)

    monkeypatch.setattr(boto3, "client", mock_boto3client_success)

    response = handler(
        event={"email": "sa5m.escom@gmail.com", "fileName": "example.csv"},
        context=None,
    )

    assert response["emailId"] == "12345678"
    assert response["lenData"] == 4
    assert isinstance(response["summaryData"], dict)
    assert response["summaryData"]["totalBalance"] == 39.74
    assert response["summaryData"]["averageCreditAmount"] == 35.25
    assert response["summaryData"]["averageDebitAmount"] == -15.38
    assert isinstance(response["summaryData"]["transactionsByMonths"], list)


def test_index_error(monkeypatch):
    mock_data["get_object"]["raise_exception"] = True

    def mock_boto3client_success(_, **kwargs):
        return Boto3ClienMock(_, mock_data=mock_data)

    monkeypatch.setattr(boto3, "client", mock_boto3client_success)

    with pytest.raises(RuntimeError) as excinfo:
        handler(
            event={"email": "sa5m.escom@gmail.com", "fileName": "example.csv"},
            context=None,
        )
