from datetime import datetime
from pathlib import Path
from typing import Any

import typer

from .filters import find_most_active_cookies

app = typer.Typer()


@app.command()
def cookietop(
    file: Path = typer.Option(
        Path("cookie_log.csv"), "-f", "--file", help="Cookies file path"
    ),
    date: datetime = typer.Option(
        "2018-12-09",
        "-d",
        "--date",
        formats=["%Y-%m-%d"],
        help="Targeted date in UTC format",
    ),
) -> Any:
    if not file.exists():
        typer.echo(f"file does not exists: {file}")
        raise typer.Exit(1)

    date_str = str(date.date())

    most_active_cookies = find_most_active_cookies(date_str, file)
    for c in most_active_cookies:
        typer.echo(c)
