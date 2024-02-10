from datetime import datetime

import pytest
from typer.testing import CliRunner

from quantcast_cli.cookietop import app
from quantcast_cli.utils import temp_csv_file

runner = CliRunner()


@pytest.fixture
def cookie_log():
    return (
        "cookie,timestamp\n"
        "cookie1,2018-12-09T17:00:00+00:00\n"
        "cookie1,2018-12-09T12:30:00+00:00\n"
        "cookie3,2018-12-09T12:00:00+00:00\n"
        "cookie2,2018-12-08T14:00:00+00:00\n"
        "cookie2,2018-12-07T15:00:00+00:00\n"
        "cookie1,2018-12-07T14:00:00+00:00\n"
    )


def test_cookietop_with_most_active_cookie(cookie_log):
    with temp_csv_file(cookie_log) as file:
        result = runner.invoke(app, ["-f", file.name, "-d", "2018-12-09"])
        assert result.exit_code == 0
        assert "cookie1" in result.output


def test_cookietop_with_no_activity_on_date(cookie_log):
    with temp_csv_file(cookie_log) as file:
        result = runner.invoke(app, ["-f", file.name, "-d", "2018-12-06"])
        assert result.exit_code == 0
        assert not result.output.strip()


def test_cookietop_with_invalid_date_format(cookie_log):
    with temp_csv_file(cookie_log) as file:
        wrong_date = "2018/12/09"
        result = runner.invoke(app, ["-f", file.name, "-d", wrong_date])
        assert result.exit_code == 2  # Typer exits with 2 when input is invalid


def test_cookietop_with_future_date(cookie_log):
    with temp_csv_file(cookie_log) as file:
        future_date = datetime.now().strftime("%Y-%m-%d")
        result = runner.invoke(app, ["-f", file.name, "-d", future_date])
        assert result.exit_code == 0
        assert not result.output.strip()


def test_cookietop_with_empty_file(tmp_path):
    with temp_csv_file("") as file:
        result = runner.invoke(app, ["-f", file.name, "-d", "2018-12-09"])
        assert result.exit_code == 0
        assert not result.output.strip()


def test_cookietop_with_non_existent_file():
    result = runner.invoke(app, ["-f", "random_7612_file.name"])
    assert result.exit_code == 1
    assert "file does not exists" in result.output.strip()
