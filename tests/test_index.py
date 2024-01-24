from json import loads

import boto3

from index import handler
from tests.mocks.inputs import event, mock_data

from .mocks.boto3_client import Boto3ClienMock


def test_index_success(monkeypatch):
    def mock_boto3client_success(_, **kwargs):
        return Boto3ClienMock(_, mock_data=mock_data)

    monkeypatch.setattr(boto3, "client", mock_boto3client_success)

    response = handler(
        event=event,
        context=None,
    )

    assert response["statusCode"] == 200

    body = loads(response["body"])

    assert body["emailId"] == "12345678"
    assert body["lenData"] == 4
    assert isinstance(body["summaryData"], dict)
    assert body["summaryData"]["totalBalance"] == 39.74
    assert body["summaryData"]["averageCreditAmount"] == 35.25
    assert body["summaryData"]["averageDebitAmount"] == -15.38
    assert isinstance(body["summaryData"]["transactionsByMonths"], list)


def test_index_error(monkeypatch):
    mock_data["get_object"]["raise_exception"] = True

    def mock_boto3client_success(_, **kwargs):
        return Boto3ClienMock(_, mock_data=mock_data)

    monkeypatch.setattr(boto3, "client", mock_boto3client_success)

    response = handler(event=event, context=None)

    assert response["statusCode"] == 400


def test_index_error_params(monkeypatch):

    event["body"] = '{\n    "email": "sa5m.escom@gmail.com", "fileName": null\n}'

    def mock_boto3client_success(_, **kwargs):
        return Boto3ClienMock(_, mock_data=mock_data)

    monkeypatch.setattr(boto3, "client", mock_boto3client_success)

    response = handler(event=event, context=None)

    assert response["statusCode"] == 500

    event["body"] = '{\n    "email": "sa5m.escom", "fileName": "example.csv"\n}'

    def mock_boto3client_success(_, **kwargs):
        return Boto3ClienMock(_, mock_data=mock_data)

    monkeypatch.setattr(boto3, "client", mock_boto3client_success)

    response = handler(event=event, context=None)

    assert response["statusCode"] == 500


def _test_index_error_save_data(monkeypatch):
    mock_data["get_object"]["raise_exception"] = False
    event[
        "body"
    ] = '{\n"email": "sa5m.escom@gmail.com", "fileName": example_save.csv\n}'
    mock_data["put_item"]["response"] = {}

    def mock_boto3client_success(_, **kwargs):
        return Boto3ClienMock(_, mock_data=mock_data)

    monkeypatch.setattr(boto3, "client", mock_boto3client_success)

    response = handler(event=event, context=None)

    assert response["statusCode"] == 500
