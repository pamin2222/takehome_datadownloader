import pytest
import os
from datadownloader.ftp_downloader import FtpDownloader


@pytest.mark.parametrize('input_url, expected', [
    ('ftp://speedtest.com/file1.txt', 'file1.txt'),
    ('ftp://user:password@speedtest.com/dir/file2.txt', 'file2.txt'),
    ('ftp://user:password@speedtest.com:8820/dir/file3.txt', 'file3.txt'),
])
def test_get_file_name(tmpdir, input_url, expected):
    downloader = FtpDownloader(input_url, str(tmpdir))
    assert downloader.get_file_name() == expected


def test_download_ftp_file_complete(mocker, tmpdir):
    ftp_test_url = 'ftp://example.net/ftp_test.zip'
    downloader = FtpDownloader(ftp_test_url, str(tmpdir))
    mocker.patch('datadownloader.ftp_downloader.FtpDownloader.start_download').side_effect = lambda: open(
        os.path.join(str(tmpdir), 'ftp_test.zip'), 'wb')
    downloader.start_download()
    assert os.path.exists(downloader.downloaded_file)


def test_download_ftp_file_fail(mocker, tmpdir):
    ftp_test_url = 'ftp://example.net/ftp_test_fail.zip'
    downloader = FtpDownloader(ftp_test_url, str(tmpdir))
    mocker.patch('datadownloader.ftp_downloader.FtpDownloader.start_download').side_effect = lambda: downloader.cancel()
    downloader.start_download()
    assert not os.path.exists(downloader.downloaded_file)
