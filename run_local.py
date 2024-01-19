from base64 import b64encode

from src.app import main

if __name__ == "__main__":
    file_upload = open("example.csv")
    file_encoded = b64encode(bytes(file_upload.read(), "utf-8"))
    file_upload.close()

    event = {"email": "sa5m.escom@gmail.com", "body-json": file_encoded}

    resp = main(event, None)
    print(resp)
