# GdDownloader 

Package to download files from google drive given shared link

[![CircleCI](https://circleci.com/gh/deven96/drive_downloader.svg?style=shield)](https://circleci.com/gh/deven96/drive_downloader) [![Coverage Status](https://coveralls.io/repos/github/deven96/drive_downloader/badge.svg?branch=master)](https://coveralls.io/github/deven96/drive_downloader?branch=master)


## Installation

```bash
    pip install gddownloader
```

## Development

```bash
    git clone git@github.com:deven96/drive_downloader.git
```

## Running the tests

```bash
    cd drive_downloader/gddownloader/
```

```bash
    python tests/__init__.py
```

## Usage

Files can be downloaded from google drive providing one has a valid shared link.
One of two ways can be used to download the files : Single or according to an [example csv](gddownloader/example.csv)

```python
    from gddownloader.core import GDownloader, CsvGDownloader

    # Single download
    share_link = r"https://drive.google.com/open?id=1Rp4Pu257IlfuoFX3sEarm8Mgl75vi1U5"
    dwnloader = GDownloader(share_link)
    print(gdwnloader.download_link)
    dwnloader.download()

    # multiple download with csv
    csv_path = "example.csv"
    csvdwnloader = CsvGDownloader(csv_path)
    print(round(csvdwnloader.total_size, 0))
    csvdwnloader.download()
```

