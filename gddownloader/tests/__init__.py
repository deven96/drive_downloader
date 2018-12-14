"""
    Test suite using doctest

>>> share_link = r"https://drive.google.com/open?id=1Rp4Pu257IlfuoFX3sEarm8Mgl75vi1U5"
>>> gdwnloader = GDownloader(share_link)
>>> print(gdwnloader.download_link)
https://drive.google.com/uc?export=download&id=1Rp4Pu257IlfuoFX3sEarm8Mgl75vi1U5

>>> csv_path = "example.csv"
>>> csvdwnloader = CsvGDownloader(csv_path)
>>> print(round(csvdwnloader.total_size, 0))
7.0

>>> args = {"shareable_link": r"https://drive.google.com/open?id=1Rp4Pu257IlfuoFX3sEarm8Mgl75vi1U5", "csv_path": None, "full_path": None}
>>> cli.main(args); # doctest: +ELLIPSIS
Downloaded to location ...
Size of download 2.47MB
"""


if __name__=="__main__":
    import doctest
    import sys, os
    sys.path.insert(0, os.getcwd())
    from core import GDownloader, CsvGDownloader
    from core import cli
    doctest.testmod(verbose=True)