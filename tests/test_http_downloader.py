from datadownloader.http_downloader import HttpDownloader
import pytest
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
from threading import Thread
import requests
import re


@pytest.mark.parametrize('input_url, expected', [
    ('http://speedtest.ftp.otenet.gr/files/test100k.db', 'test100k.db'),
    ('http://speedtest.ftp.otenet.gr/files/test1Mb.db', 'test1Mb.db'),
    ('https://www.abc.com/file4.txt', 'file4.txt'),
])
def test_get_file_name(tmpdir, input_url, expected):
    downloader = HttpDownloader(input_url, str(tmpdir))
    assert downloader.get_file_name() == expected


class MockServerRequestHandler(BaseHTTPRequestHandler):
    COMPLETE_PATTERN = re.compile(r'_complete')

    def do_GET(self):
        if re.search(self.COMPLETE_PATTERN, self.path):
            self.send_response(requests.codes.ok)

            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            response_content = b'\x00\x00\x00\x00\x00\x00\x00\x00'
            self.wfile.write(response_content)
            return
        else:
            self.send_response(requests.codes.not_found)

            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

            response_content = b''
            self.wfile.write(response_content)
            return

    @staticmethod
    def get_free_port():
        s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        address, port = s.getsockname()
        s.close()
        return port

    @staticmethod
    def start_mock_server(port):
        mock_server = HTTPServer(('localhost', port), MockServerRequestHandler)
        mock_server_thread = Thread(target=mock_server.serve_forever)
        mock_server_thread.setDaemon(True)
        mock_server_thread.start()


class TestWithMockHttpServer(object):
    @classmethod
    def setup_class(self):
        self.mock_server_port = MockServerRequestHandler.get_free_port()
        MockServerRequestHandler.start_mock_server(self.mock_server_port)

    def test_http_download_complete(self, tmpdir, monkeypatch):
        mock_file_url = 'http://localhost:{port}/test_complete.txt'.format(port=self.mock_server_port)
        http_downloader = HttpDownloader(mock_file_url, str(tmpdir))

        monkeypatch.setattr(http_downloader, 'url', mock_file_url)
        http_downloader.start_download()

        assert os.path.exists(http_downloader.downloaded_file)
        assert open(http_downloader.downloaded_file).read() == b'\x00\x00\x00\x00\x00\x00\x00\x00'.decode('utf-8')

    def test_http_download_return_none(self, tmpdir, monkeypatch):
        mock_file_url = 'http://localhost:{port}/test_none.txt'.format(port=self.mock_server_port)
        http_downloader = HttpDownloader(mock_file_url, str(tmpdir))

        monkeypatch.setattr(http_downloader, 'url', mock_file_url)
        http_downloader.start_download()

        assert not os.path.exists(http_downloader.downloaded_file)
