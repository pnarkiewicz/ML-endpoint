import requests


def get_ulr(speal_length="", speal_width="", petal_length="", petal_width=""):
    return f"http://localhost:8000/predict/?speal_length={speal_length}&speal_width={speal_width}&petal_length={petal_length}&petal_width={petal_width}"


def get_invalid_ulr(speal_length="", speal_width="", petal_length="", petal_width=""):
    return f"http://localhost:8000/predict/?speal_length={speal_length}&speal_width={speal_width}&petal_length={petal_length}"


def send_request(speal_length="", speal_width="", petal_length="", petal_width=""):

    url = get_ulr(speal_length, speal_width, petal_length, petal_width)

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()

    return response


def send_invalid_request(speal_length="", speal_width="", petal_length=""):

    url = get_invalid_ulr(speal_length, speal_width, petal_length)

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()

    return response


def test_predict():

    assert send_request(1000, 30, 102, 1)["prediction"] == "versicolor"
    assert send_request(1, 30, 102, 1)["prediction"] == "virginica"
    assert send_request(1, -1, 102, 1)["prediction"] == "virginica"
    assert (
        send_request(1, -1, "TE", 1)["detail"][0]["msg"] == "value is not a valid float"
    )
    assert (
        send_invalid_request(1, -1, 102)["detail"]
        == "Please specify the following parameters: ['petal_width']"
    )


def test_get_requests():

    url = "http://localhost:8000/get_requests"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload).json()

    assert len(response) >= 0

    if len(response) > 0:
        assert response[0]["index"] == 0
        assert response[-1]["index"] == len(response) - 1

        for key in [
            "index",
            "date",
            "speal_length",
            "petal_length",
            "speal_width",
            "speal_length",
            "message",
        ]:
            assert key in response[-1]
