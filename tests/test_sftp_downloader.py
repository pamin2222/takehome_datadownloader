import pytest
import os
from datadownloader.sftp_downloader import SftpDownloader


@pytest.mark.parametrize('input_url, expected', [
    ('sftp://user:password@speedtest.com/dir/file1.txt', 'file1.txt'),
    ('sftp://user:password@speedtest.com:8820/dir/file2.txt', 'file2.txt'),
])
def test_get_file_name(tmpdir, input_url, expected):
    downloader = SftpDownloader(input_url, str(tmpdir))
    assert downloader.get_file_name() == expected


def test_download_sftp_file_complete(mocker, tmpdir):
    ftp_test_url = 'sftp://pamin:Pamin@example.net/sftp_test.zip'
    downloader = SftpDownloader(ftp_test_url, str(tmpdir))
    mocker.patch('datadownloader.sftp_downloader.SftpDownloader.start_download').side_effect = lambda: open(
        os.path.join(str(tmpdir), 'sftp_test.zip'), 'wb')
    downloader.start_download()
    assert os.path.exists(downloader.downloaded_file)


def test_download_sftp_file_fail(mocker, tmpdir):
    ftp_test_url = 'sftp://pamin:Pamin@example.net/sftp_test_fail.zip'
    downloader = SftpDownloader(ftp_test_url, str(tmpdir))
    mocker.patch(
        'datadownloader.sftp_downloader.SftpDownloader.start_download').side_effect = lambda: downloader.cancel()
    downloader.start_download()
    assert not os.path.exists(downloader.downloaded_file)
