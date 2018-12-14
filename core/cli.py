import argparse
from downloader import GDownloader, CsvGDownloader


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
    CsvGDownloader(args['csv_path'])