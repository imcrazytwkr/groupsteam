from http.client import HTTPResponse
from urllib import request
from gzip import GzipFile
from io import BytesIO
from typing import Any
import json


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"


def fetch_json(url: str) -> Any:
    req = request.Request(
        url,
        data=None,
        headers={
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": USER_AGENT,
        },
    )

    with request.urlopen(req) as response:
        payload = read_body(response)

    return payload


# @api: private
def read_body(response: HTTPResponse) -> Any:
    encoding = response.info().get("Content-Encoding")

    if encoding == "gzip" or encoding == "deflate":
        buffer = BytesIO(response.read())
        return json.load(GzipFile(fileobj=buffer, mode="rb"))

    return json.load(response)


__all__ = ["fetch_json"]

assert __name__ != "__main__", "Do no evil"
