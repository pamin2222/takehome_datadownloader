import os
import pytest
import uuid


@pytest.fixture(scope='session')
def url_file(test_urls):
    url_file_name = str(uuid.uuid4())

    with open(url_file_name, 'w') as f:
        for url in test_urls:
            url = url[0]
            f.write(url + '\n')

    yield os.path.abspath(url_file_name)

    os.remove(url_file_name)


@pytest.fixture(scope='session')
def test_urls(http_url, ftp_url):
    return [http_url, ftp_url]


@pytest.fixture(scope='session')
def http_url():
    return (
        'http://speedtest.ftp.otenet.gr/files/test100k.db'
    )


@pytest.fixture(scope='session')
def ftp_url():
    return (
        'ftp://speedtest.tele2.net/1MB.zip',
    )
