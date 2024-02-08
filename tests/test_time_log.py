import time

from quantcast_cli.time_log import time_log


def test_time_log(capsys):
    txt = "Hi Test"
    with time_log(txt):
        a = 1 + 2
        time.sleep(0.1)
    captured = capsys.readouterr()
    assert captured.out.startswith(f"{txt}: ")
    assert captured.out.endswith(f"secs\n")
    assert a == 3
