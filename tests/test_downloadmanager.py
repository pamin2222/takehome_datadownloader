import pytest
from datadownloader.downloadmanager import DownloaderFactory
from datadownloader.ftp_downloader import FtpDownloader
from datadownloader.sftp_downloader import SftpDownloader
from datadownloader.http_downloader import HttpDownloader


def test_downloader_factory_unsupport_url():
    with pytest.raises(NotImplementedError):
        DownloaderFactory.get_downloader('hello://world')


@pytest.mark.parametrize('input_url, expected', [
    ('ftp://speedtest.com/file1.txt', FtpDownloader),
    ('http://user:password@speedtest.com/dir/file2.txt', HttpDownloader),
    ('sftp://user:password@speedtest.com:8820/dir/file3.txt', SftpDownloader),
])
def test_downloader_factory(input_url, expected):
    return_downloader = DownloaderFactory.get_downloader(input_url)
    assert return_downloader == expected
