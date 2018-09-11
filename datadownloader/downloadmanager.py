import os
import time
from queue import Queue, Empty
from threading import Thread
from urllib.parse import urlparse
from tqdm import tqdm
from datadownloader.http_downloader import HttpDownloader
from datadownloader.ftp_downloader import FtpDownloader
from datadownloader.sftp_downloader import SftpDownloader
import sys


class DownloaderFactory(object):
    @staticmethod
    def get_downloader(url):
        parsed_url = urlparse(url)
        scheme = parsed_url.scheme
        if scheme == "http":
            return HttpDownloader
        elif scheme == "https":
            return HttpDownloader
        elif scheme == "ftp":
            return FtpDownloader
        elif scheme == "sftp":
            return SftpDownloader
        else:
            raise NotImplementedError('No {0} downloader'.format(scheme))


class DownloadManager(object):
    def __init__(self, urls, output_directory):
        self.output_directory = output_directory

        self._urls = Queue()
        self._download_handlers = []

        # initialize the queue
        for i, url in enumerate(urls):
            self._urls.put((i, url))
            self._download_handlers.append(DownloadHandler(url))

    def process(self):
        try:
            watcher = Thread(target=self.watcher)
            watcher.start()

            for _ in range(5):
                t = Thread(target=self.worker)
                t.start()

            self._urls.join()
            watcher.join()
            self.remove_uncompleted_file()
        except KeyboardInterrupt:
            self.remove_uncompleted_file()
            tqdm.write('')
            sys.exit("Keyboard Interrupt - Cancel downloading tasks")

    def worker(self):
        while True:
            try:
                index, url = self._urls.get_nowait()
            except Empty:
                break

            downloader = self.process_single_url(url)
            if downloader:
                self._download_handlers[index].downloader = downloader
                downloader.start_download()
            self._urls.task_done()

    def process_single_url(self, url):
        try:
            downloader = DownloaderFactory().get_downloader(url)
        except NotImplementedError as e:
            print('{}: skipping {}'.format(e, url))
            return None

        output = os.path.join(self.output_directory)
        download_process = downloader(url, output)
        return download_process

    def watcher(self):
        try:
            while True:
                for download_handler in self._download_handlers:
                    download_handler.update_progress()

                if self._urls.unfinished_tasks == 0:
                    self.remove_uncompleted_file()
                    break
                time.sleep(1)

            tqdm.write('Download Completed!')
        except KeyboardInterrupt:
            self.remove_uncompleted_file()
            tqdm.write('')
            sys.exit("Keyboard Interrupt - Cancel downloading tasks")

    def remove_uncompleted_file(self):
        for download_handler in self._download_handlers:
            download_handler.remove_uncompleted_file()


class DownloadHandler(object):
    def __init__(self, url):
        self.url = url
        self.downloader = None
        self.progress_bar = None

    def update_progress(self):
        if not self.downloader:
            return

        downloaded, total = self.downloader.get_progress()

        if self.progress_bar is None:
            bar_name = os.path.basename(self.downloader.downloaded_file)
            self.progress_bar = tqdm(
                total=total, desc=bar_name, unit='b', unit_scale=True, unit_divisor=1024, disable=False)
        progress = downloaded - self.progress_bar.n
        self.progress_bar.update(progress)

    def remove_uncompleted_file(self):
        if self.downloader == None:
            return
        downloaded, total = self.downloader.get_progress()
        if downloaded != total or downloaded == 0:
            self.downloader.cancel()
