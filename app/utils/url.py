from urllib.parse import urlencode


def make_url(url):
    def combine_url(pathname, **kwargs):
        query_string = ""

        if kwargs["params"]:
            query_string = urlencode(kwargs["params"])

        if query_string:
            return f"{url}/{pathname}?{query_string}"

        return f"{url}/{pathname}"

    return combine_url
