from datetime import datetime
from io import BytesIO

from botocore.response import StreamingBody

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
    "put_item": {
        "raise_exception": False,
        "response": {"ResponseMetadata": {"HTTPStatusCode": 200}},
    },
}


event = {
    "version": "2.0",
    "routeKey": "$default",
    "rawPath": "/",
    "rawQueryString": "",
    "headers": {
        "content-length": "70",
        "x-amzn-tls-version": "TLSv1.2",
        "x-forwarded-proto": "https",
        "postman-token": "d9977f07-40e0-4da9-9514-8689edaec9e6",
        "x-forwarded-port": "443",
        "x-forwarded-for": "187.190.198.9",
        "accept": "*/*",
        "x-amzn-tls-cipher-suite": "ECDHE-RSA-AES128-GCM-SHA256",
        "x-amzn-trace-id": "Root=1-65b06869-5c510d14798bd7c02fd2f0f7",
        "host": "5ueyx4dowr4gbfees63usdluiq0tzeqb.lambda-url.us-east-2.on.aws",
        "content-type": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "user-agent": "PostmanRuntime/7.36.1",
        "x-api-key": "A",
    },
    "requestContext": {
        "accountId": "anonymous",
        "apiId": "5ueyx4dowr4gbfees63usdluiq0tzeqb",
        "domainName": "5ueyx4dowr4gbfees63usdluiq0tzeqb.lambda-url.us-east-2.on.aws",
        "domainPrefix": "5ueyx4dowr4gbfees63usdluiq0tzeqb",
        "http": {
            "method": "POST",
            "path": "/",
            "protocol": "HTTP/1.1",
            "sourceIp": "187.190.198.9",
            "userAgent": "PostmanRuntime/7.36.1",
        },
        "requestId": "fa35530e-5c33-418f-a56c-1d06b592c0b4",
        "routeKey": "$default",
        "stage": "$default",
        "time": "24/Jan/2024:01:31:21 +0000",
        "timeEpoch": 1706059881683,
    },
    "body": '{\n    "email": "sa5m.escom@gmail.com",\n    "fileName": "example.csv"\n}',
    "isBase64Encoded": False,
}
