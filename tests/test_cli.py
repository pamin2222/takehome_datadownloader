from io import StringIO

import pytest

from datadownloader.cli import parse_args, main_cli


def test_parse_args(monkeypatch, url_file, tmpdir):
    monkeypatch.setattr(
        'sys.argv',
        ['datadownloader',
         '-u', url_file,
         '-o', str(tmpdir)])
    args = parse_args()

    assert args.urls.name == url_file
    assert args.output_directory == str(tmpdir)


def test_parse_args_missing_parameters(monkeypatch, url_file):
    args = [['datadownloader', '-o'],
            ['datadownloader', '-u', url_file]]

    for arg in args:
        monkeypatch.setattr('sys.argv', arg)
        with pytest.raises(SystemExit):
            parse_args()


def test_parse_args_invalid_parameters(monkeypatch, url_file, tmpdir):
    args = [
        ['datadownloader', '-u', 'lol', '-o', str(tmpdir)],
        ['datadownloader', '-u', url_file, '-o', '/root'],
        ['datadownloader', '-u', url_file, '-o', 'lol']
    ]

    for arg in args:
        monkeypatch.setattr('sys.argv', arg)
        with pytest.raises(SystemExit):
            parse_args()


@pytest.mark.remote_data
def test_run_from_cli_with_file(monkeypatch, url_file, tmpdir):
    monkeypatch.setattr('sys.argv', ['datadownloader', '-u', url_file, '-o', str(tmpdir)])
    main_cli()


@pytest.mark.remote_data
def test_run_from_cli_with_stdin(monkeypatch, url_file, tmpdir):
    with open(url_file) as f:
        stdin = StringIO(f.read())

    monkeypatch.setattr('sys.stdin', stdin)
    monkeypatch.setattr('sys.argv', ['datadownloader', '-o', str(tmpdir)])
    main_cli()
