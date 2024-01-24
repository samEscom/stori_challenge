from src.app import main
from tests.mocks.inputs import event

if __name__ == "__main__":

    resp = main(event, None)
    print(resp)
