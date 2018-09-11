import os
import requests
from urllib.parse import urlparse
from datadownloader.abstract_downloader import AbstractDownloader


class HttpDownloader(AbstractDownloader):

    def __init__(self, url, downloaded_dir):
        super().__init__(url, downloaded_dir)
        self._total_file_length = 0
        self._file_downloaded_length = 0
        self._request = None
        self._chunk_size = 1024

    def get_file_name(self):
        parsed_url = urlparse(self.url)
        return os.path.basename(parsed_url.path)

    def start_download(self):
        try:
            super().start_download()
            self._request = requests.get(self.url, stream=True)
            try:
                self._request.raise_for_status()
                self._total_file_length = int(self._request.headers['content-length'])
            except KeyError:
                pass
            except ValueError:
                pass

            with open(self.downloaded_file, "wb") as f:
                for chunk in self._request.iter_content(chunk_size=self._chunk_size):
                    if chunk:  # filter out keep-alive new chunks
                        self._write_data_chunk(f, chunk)
            self._request.close()
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
            self._request.close()
        except:
            pass
