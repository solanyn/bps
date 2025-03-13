import re
import s3fs
import os
from urllib.parse import urlparse, urljoin
from urllib.request import urlopen
from prefect import flow, task
from typing import List
from bs4 import BeautifulSoup
import httpx

NSW_PROPERTY_SALES_INFORMATION_URL = (
    "https://valuation.property.nsw.gov.au/embed/propertySalesInformation"
)


@task
def get_links() -> List[str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    r = httpx.get(NSW_PROPERTY_SALES_INFORMATION_URL, headers=headers)
    soup = BeautifulSoup(r.text, features="html.parser")
    zip_files = [
        link["href"]
        for link in soup.find_all(href=True)
        if re.search(r"\.zip$", link["href"], re.IGNORECASE)
    ]
    return zip_files


@task()
def download_links(urls: List[str]):
    urls = [urlparse(url) for url in urls]
    s3 = s3fs.S3FileSystem(
        key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
        endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    )
    for url in urls:
        uri = f"s3://bps/{url.path}"
        if s3.exists(uri):
            continue

        with urlopen(url) as fd:
            with s3.open(uri, "wb") as f:
                f.write(fd.read())


@flow
def collect() -> None:
    urls = get_links()
    download_links(urls)
