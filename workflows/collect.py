from flytekit import task, workflow, ImageSpec
from typing import List
from bs4 import BeautifulSoup
import httpx

NSW_PROPERTY_SALES_INFORMATION_URL = (
    "https://valuation.property.nsw.gov.au/embed/propertySalesInformation"
)


BPS_IMAGE_SPEC = ImageSpec(
    name="flyte-bps",
    registry="ghcr.io/solanyn",
    packages=["httpx", "s3fs", "beautifulsoup4"],
    python_version="3.11",
)


@task
def get_links() -> List[str]:
    r = httpx.get(NSW_PROPERTY_SALES_INFORMATION_URL)
    soup = BeautifulSoup(r.text, features="html.parser")
    a_tags = [tag.href for tag in soup.find_all(href=True)]
    print(a_tags)
    return a_tags


@workflow
def collect() -> None:
    print(get_links())


if __name__ == "__main__":
    # Execute the workflow by invoking it like a function and passing in
    # the necessary parameters
    print(f"Running wf() {collect()}")
