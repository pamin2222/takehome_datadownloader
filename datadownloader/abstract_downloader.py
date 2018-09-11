import os
from abc import ABC, abstractmethod


class AbstractDownloader(ABC):

    def __init__(self, url, downloaded_dir):
        self.url = url
        self._downloaded_file = None
        self._downloaded_directory = downloaded_dir
        self._error = None

    @abstractmethod
    def get_file_name(self):
        return ''

    @property
    def downloaded_file(self):
        if self._downloaded_file:
            return self._downloaded_file

        filename = self.get_file_name()
        if filename == '':
            raise RuntimeError('Cannot download')

        dup_count = 0
        dup_filename = filename
        while dup_count < 100:
            download_filepath = os.path.join(self._downloaded_directory, dup_filename)
            if self._create_downloaded_file(download_filepath):
                return self._downloaded_file

            dup_count += 1
            dup_filename, extension = os.path.splitext(filename)
            dup_filename = dup_filename + "_" + str(dup_count) + extension

        raise RuntimeError('Cannot download or too much duplicated files')

    def _create_downloaded_file(self, path):
        try:
            with open(path, 'x'):
                self._downloaded_file = path
        except FileExistsError:
            return None
        else:
            return self.downloaded_file

    @abstractmethod
    def start_download(self):
        try:
            os.makedirs(os.path.dirname(self.downloaded_file))
        except:
            pass

    def delete_downloaded_file(self):
        if self.downloaded_file != None and os.path.exists(self.downloaded_file):
            print("delete downloaded file {0}".format(self.downloaded_file))
            os.remove(self.downloaded_file)

    @abstractmethod
    def get_progress(self):
        raise NotImplementedError("Should have implemented this")
