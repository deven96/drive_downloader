"""
 Custom scipt to run command line tool that downloads a file from google drive script given
    the shareable link

"""

import argparse
import os
import re
import sys
import time
import urllib
from multiprocessing.dummy import Pool
from urllib.request import urlopen, urlretrieve

import numpy as np
import pandas as pd
import progressbar as pb


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
        self.total_size = int(ma.replace("ma=", "")) / (1024 * 1024)
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
        downloaded = (count * block_size) / (1024 * 1024)
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
            print(f"Downloaded to location {self.filename}\nSize of download {round(self.total_size, 2)}MB")
        else:
            self.pbar.start()
            self.filename, self.headers = urlretrieve(url=self.download_link, 
                                            reporthook=self.reporthook)
            print(f"Downloaded to location {self.filename}\nSize of download {round(self.total_size, 2)}MB")


def create_csv_downloads(csv_path):
    """ 
        parses a csv of (shareable_link, path)
    """
    downloader_list = list()
    total_size = 0
    if not str(csv_path).endswith('.csv'):
        sys.exit("Not a valid (.csv) file")
    try:
        df = pd.read_csv(csv_path, header=None).fillna("None")
        for i in range(0, len(df)):
            path = df.iloc[i][1]
            shareable_link = df.iloc[i][0]
            downloader = None
            if path == "None":
                downloader = GDownloader(shareable_link)
                total_size += downloader.total_size
                downloader_list.append(downloader)
            else:
                downloader = GDownloader(shareable_link, path)
                total_size += downloader.total_size
                downloader_list.append(downloader)
        main_pb = pb.ProgressBar(maxval=total_size)
        main_pb.start()
        for i in downloader_list:
            i.download()
            main_pb.update(i.total_size)
        main_pb.finish()
        print(f"Total Download Finished, total_size was {round(total_size, 2)}MB")
    except Exception as e:
        sys.exit(e)



if __name__ == "__main__":
    #setup command line arguments
    parser = argparse.ArgumentParser(description='Google Drive Resource Downloader')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-csv', '--csv_path', help='full path to csv file of shareable links and paths')
    group.add_argument('-sl','--shareable-link', help='Shareable link of resource')
    parser.add_argument('-path','--full-path', help='Full path plus name(with extension) to be given \
                        to the resource on download e.g /home/user/Documents/resource.zip', default=None)
    args = vars(parser.parse_args())
    if not args['csv_path'] and args['shareable_link']:
        downloader = GDownloader(args['shareable_link'], args["full_path"])
        downloader.download()
    elif args['csv_path']:
        create_csv_downloads(args['csv_path'])
