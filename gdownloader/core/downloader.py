"""
 Defined Classes that handle single and multi download scenarios

"""
import os
import re
import sys
import urllib
from urllib.request import urlopen, urlretrieve

import pandas as pd
import progressbar as pb


class GDownloader:
    """
        Download Handler
    """
    def __init__(self, share_link, path=None):
        self.share_link = share_link
        if str(path).startswith("~"):
            raise Exception("Please do not use tilde(~) to denote home location")
        else:
            self.path = path
        #get site info
        meta = urlopen(self.download_link).info()
        alt_svc = dict(meta)["Alt-Svc"]
        ma = re.findall(r"ma=\d+", alt_svc)[0]
        #extract int
        self.total_size = int(ma.replace("ma=", "")) / (1024 * 1024)
        self.filename = "Unassigned"
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
            raise Exception("Link given is not a valid google drive download link")
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


class CsvGDownloader:
    """
        Handles multiple downloads using csv
    """
    def __init__(self, csv_path):
        self.csv_path = csv_path 
        self.size_list = []
        if not str(self.csv_path).endswith('.csv'):
            raise Exception("Not a valid (.csv) file")
        self.df = pd.read_csv(csv_path, header=None).fillna("None")
        self.main_pb = pb.ProgressBar(maxval=self.total_size)

    @property
    def gdownloader_list(self):
        downloader_list = []
        for i in range(0, len(self.df)):
            path = self.df.iloc[i][1]
            shareable_link = self.df.iloc[i][0]
            downloader = None
            if path == "None":
                downloader = GDownloader(shareable_link)
            else:
                downloader = GDownloader(shareable_link, path)
            downloader_list.append(downloader)
        return downloader_list

    @property
    def total_size(self):
        """
            Combined size of all files to be downloaded
        """
        size = 0
        for i in self.gdownloader_list:
            size += i.total_size
        return size

    def __listfromgdownloader(self, attr):
        """
            Generates any attribute list from gdownloader (private)

            attr[str]: name of attribute to get
        """
        output = []
        for i in self.gdownloader_list:
            output.append(getattr(i, attr))
        return output
    
    @property
    def filenames(self):
        """
            List of the final filenames as stored on download
        """
        return self.__listfromgdownloader("filename")

    @property
    def sizes(self):
        """
            List of the individual sizes 
        """
        return self.__listfromgdownloader("total_size")   


    def download(self):
        """
            Downloads the files from csv using urllib
        """      
        self.main_pb.start()
        for i in self.gdownloader_list:
            i.download()
            self.main_pb.update(i.total_size)
        main_pb.finish()
        print(f"Total Download Finished, total_size was {round(self.total_size, 2)}MB")

