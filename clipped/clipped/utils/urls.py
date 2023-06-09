from urllib.parse import urlparse


def validate_url(url: str) -> bool:
    if not url.startswith(("http://", "https://")):
        return False
    parsed = urlparse(url)
    if not parsed.hostname:
        return False
    return True


URL_FORMAT = "{protocol}://{domain}{path}"
