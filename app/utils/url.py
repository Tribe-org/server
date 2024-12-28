from urllib.parse import urlencode

def make_url(url):
    def combine_url(pathname, **kwargs):
        # url 끝 슬래시 제거, pathname 시작 슬래시 제거 후 결합
        base_path = f"{url.rstrip('/')}/{pathname.lstrip('/')}"
        query_string = ""

        if kwargs.get("params"):  # params가 존재하는 경우
            query_string = urlencode(kwargs["params"])

        if query_string:
            return f"{base_path}?{query_string}"

        return base_path

    return combine_url
