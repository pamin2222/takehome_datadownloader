import os
from ftplib import FTP
from urllib.parse import urlparse

from datadownloader.abstract_downloader import AbstractDownloader


class FtpDownloader(AbstractDownloader):

    def __init__(self, url, downloaded_dir):
        super().__init__(url, downloaded_dir)
        self._total_file_length = 0
        self._file_downloaded_length = 0
        self._ftp = FTP()

    def _connect(self):
        parsed_url = urlparse(self.url)
        hostname = parsed_url.hostname
        port = parsed_url.port or 0
        username = parsed_url.username
        password = parsed_url.password

        try:
            self._ftp.connect(host=hostname, port=port)
            self._ftp.login(username, password)
        except:
            print("ftp login error for {0}".format(self.url))
            self.cancel()

    def get_file_name(self):
        parsed_url = urlparse(self.url)
        return os.path.basename(parsed_url.path)

    def start_download(self):
        try:
            super().start_download()
            parsed_url = urlparse(self.url)
            path = parsed_url.path
            dirname = os.path.dirname(path)

            self._connect()
            if dirname:
                self._ftp.cwd(dirname)

            self._total_file_length = self._ftp.size(path)
            remote_filename = os.path.basename(path)

            with open(self.downloaded_file, 'wb') as f:
                self._ftp.retrbinary("RETR " + remote_filename,
                                     lambda data: self._write_data_chunk(f, data))
        except Exception as e:
            print(e)
            self.cancel()

    def _write_data_chunk(self, f, data):
        self._file_downloaded_length += len(data)
        f.write(data)

    def get_progress(self):
        return self._file_downloaded_length, self._total_file_length

    def cancel(self):
        try:
            self.delete_downloaded_file()
            if self._ftp.sock:
                self._ftp.abort()
        except:
            pass
