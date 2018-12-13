"""
 Custom scipt to run command line tool that downloads a file from google drive script given
    the shareable link

"""

import argparse
import progressbar as pb
import os
import re
import sys
import time
import urllib
from multiprocessing.dummy import Pool
from urllib.request import urlretrieve, urlopen


class GDownloader():
    """
        Download Handler
    """
    def __init__(self, share_link, path=None):
        self.share_link = share_link
        if str(path).startswith("~"):
            sys.exit("Please do not use tilde(~) to denote home location")
        else:
            self.path = path
        #get site info
        meta = urlopen(self.download_link).info()
        alt_svc = dict(meta)["Alt-Svc"]
        ma = re.findall(r"ma=\d+", alt_svc)[0]
        #extract int
        self.total_size = int(ma.replace("ma=", ""))
        self.filename = None
        self.headers = None
        #progress bar
        self.pbar = pb.ProgressBar(maxval=self.total_size)

    @property
    def download_link(self):
        """
            Preps a shareable link and turns it into a downloadable one
            e.g https://drive.google.com/open?id=1Rp4Pu257IlfuoFX3sEarm8Mgl75vi1U5
            turns to https://drive.google.com/uc?export=download&id=1Rp4Pu257IlfuoFX3sEarm8Mgl75vi1U5
        """
        drive_share = "https://drive.google.com/open?id="
        replace = "https://drive.google.com/open?"
        drive_download = "https://drive.google.com/uc?export=download&"
        if not self.share_link.startswith(drive_share):
            sys.exit("Link given is not a valid google drive download link")
        else:
            return self.share_link.replace(replace, drive_download)
    
    def reporthook(self, count, block_size, total_size):
        """
            monitor progress of download
        """
        downloaded = count * block_size
        if downloaded < self.total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()


    def download(self):
        """
            Downloads the file using urllib
        """
        if self.path:
            self.pbar.start()
            self.filename, self.headers = urlretrieve(url=self.download_link,
                                            filename=self.path, 
                                            reporthook=self.reporthook)
        else:
            self.pbar.start()
            self.filename, self.headers = urlretrieve(url=self.download_link, 
                                            reporthook=self.reporthook)



if __name__ == "__main__":
    #setup command line arguments
    parser = argparse.ArgumentParser(description='Google Drive Resource Downloader')
    parser.add_argument('-sl','--shareable-link', help='Shareable link of resource', required=True)
    parser.add_argument('-path','--full-path', help='Full path plus name(with extension) to be given \
                        to the resource on download e.g /home/user/Documents/resource.zip', default=None)
    args = vars(parser.parse_args())
    downloader = GDownloader(args['shareable_link'], args["full_path"])
    downloader.download()
    print(f"Downloaded to location {downloader.filename}")
