import os
from urllib.parse import urlparse
import paramiko
from datadownloader.abstract_downloader import AbstractDownloader
import shutil


class SftpDownloader(AbstractDownloader):

    def __init__(self, url, downloaded_dir):
        super().__init__(url, downloaded_dir)
        self._total_file_length = 0
        self._file_downloaded_length = 0
        self._transport = None
        self._sftp = None

    def _connect(self):
        parsed_url = urlparse(self.url)
        hostname = parsed_url.hostname
        port = parsed_url.port or 0
        username = parsed_url.username
        password = parsed_url.password

        try:
            self._transport = paramiko.Transport((hostname, port))
            self._transport.connect(username=username, password=password)
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        except:
            print("sftp login error for {0}".format(self.url))
            self.cancel()

    def get_file_name(self):
        parsed_url = urlparse(self.url)
        return os.path.basename(parsed_url.path)

    def start_download(self):
        try:
            super().start_download()
            parsed_url = urlparse(self.url)
            path = parsed_url.path

            self._connect()
            info = self._sftp.stat(path)
            self._total_file_length = info.st_size

            with open(self.downloaded_file, 'wb') as f:
                with self._sftp.open(path, mode="r", bufsize=1024) as remote_file:
                    self._file_downloaded_length = self._total_file_length * 0.10  # indicate the downloading is started
                    shutil.copyfileobj(remote_file, f)
                self._file_downloaded_length = self._total_file_length

        except Exception as e:
            print(e)
            self.cancel()

    def get_progress(self):
        return self._file_downloaded_length, self._total_file_length

    def cancel(self):
        try:
            self.delete_downloaded_file()
            self._sftp.close()
        except:
            pass
