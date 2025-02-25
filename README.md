# NSW Bulk Property Sales Workflows

[Flyte](https://flyte.org) workflows for collecting and processing NSW property sales data. It performs the following:

- Finds all HTML `<a>` tags from the [NSW Bulk Property Sales Information](https://valuation.property.nsw.gov.au/embed/propertySalesInformation) page, which provides links to weekly and annual sales reports.
- Downloads and stores linked files on a Minio instance (s3 compatible object storage).
- Extracts and processes data into [Parquet](https://parquet.apache.org) format in s3 storage.
