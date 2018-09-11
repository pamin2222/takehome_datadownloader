import os
import sys
import argparse

from datadownloader.downloadmanager import DownloadManager


def valid_directory(dir_val):
    if not os.path.isdir(dir_val):
        raise argparse.ArgumentTypeError("{0} is not a valid directory".format(dir_val))
    return dir_val


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--urls', type=argparse.FileType('r', encoding='UTF-8'), default=sys.stdin,
                        help='File containing urls')
    parser.add_argument('-o', '--output_directory', required=True, type=valid_directory,
                        help='Output directory')

    args = parser.parse_args()
    return args


def main_cli():
    args = parse_args()

    urls = [url.strip() for url in args.urls.readlines()]
    output_directory = args.output_directory

    download_manager = DownloadManager(urls, output_directory)
    download_manager.process()
