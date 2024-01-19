from base64 import b64encode

from index import handler


def test_reminders(monkeypatch):

    file_upload = open("example.csv")
    file_encoded = b64encode(bytes(file_upload.read(), "utf-8"))
    file_upload.close()

    response = handler(
        event={"email": "sa5m.escom@gmail.com", "body-json": file_encoded},
        context=None,
    )

    assert response["emailId"] == 0
