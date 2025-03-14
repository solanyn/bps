import re
import s3fs
from urllib.parse import urlparse
from urllib.request import urlopen
from prefect import flow, task
from prefect.blocks.system import Secret
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
    urls = [url for url in urls]
    s3 = s3fs.S3FileSystem(
        key=Secret.load("minio-key").get(),
        secret=Secret.load("minio-secret").get(),
        endpoint_url="http://minio.default.svc.cluster.local:9000",
    )
    for url in urls:
        uri = f"s3://bps/{urlparse(url).path}"
        if s3.exists(uri):
            continue

        with urlopen(url) as fd:
            with s3.open(uri, "wb") as f:
                f.write(fd.read())


@flow
def collect() -> None:
    urls = get_links()
    download_links(urls)


if __name__ == "__main__":
    collect()
