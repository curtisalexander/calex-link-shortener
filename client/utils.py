import emoji
import os
import requests
import typer

from urllib.parse import quote_plus, urlencode, urlparse
from typing import Optional


def validate_url(longurl: str) -> None:
    longurl_parsed = urlparse(longurl)

    val_start = f"\nValidating "
    val_middle = typer.style(f"{longurl}", fg=typer.colors.YELLOW, bold=True)
    val_end = " is a valid url..."
    val_msg = val_start + val_middle + val_end
    typer.echo(val_msg)

    longurl_scheme = longurl_parsed.scheme
    longurl_netloc = longurl_parsed.netloc

    if longurl_scheme != "" and longurl_netloc != "":
        print(
            emoji.emojize("  :white_check_mark:  ", use_aliases=True),
            end="",
            flush=True,
        )
        val_val_start = typer.style(f"{longurl}", fg=typer.colors.YELLOW, bold=True)
        val_val_end = f" passes validation!\n"
        val_val_msg = val_val_start + val_val_end
        typer.echo(val_val_msg)
    else:
        print(emoji.emojize("  :x:  ", use_aliases=True), end="", flush=True)
        val_inval_start = typer.style(f"{longurl}", fg=typer.colors.YELLOW, bold=True)
        val_inval_end = f" fails validation!\n"
        val_inval_msg = val_inval_start + val_inval_end
        typer.echo(val_inval_msg)
        raise typer.Exit()


def create_azure_url(env_var: str, path: str, **kwargs) -> str:
    longurl: Optional[str] = kwargs.get("longurl", None)
    azure_url: str = os.getenv(env_var)

    if longurl:
        query_path: str = urlencode({"path": path, "longurl": longurl})
    else:
        query_path: str = urlencode({"path": path})

    azure_full_url: str = f"{azure_url}&{query_path}"

    typer.echo("Submitting GET to...")
    typer.secho(f"  {azure_full_url}\n", fg=typer.colors.BRIGHT_BLUE, bold=True)

    return azure_full_url


def print_response_status(r: requests.models.Response) -> None:
    if r.ok:
        prs_start = f"Hooray, all is well!  Status code: "
        prs_end = typer.style(
            f"{r.status_code}\n", fg=typer.colors.BRIGHT_GREEN, bold=True
        )
        prs_msg = prs_start + prs_end
        typer.echo(prs_msg)
    else:
        prs_start = f"Something went wrong!  Status code: "
        prs_end = typer.style(
            f"{r.status_code}\n", fg=typer.colors.BRIGHT_RED, bold=True
        )
        prs_msg = prs_start + prs_end
        typer.echo(prs_msg)

