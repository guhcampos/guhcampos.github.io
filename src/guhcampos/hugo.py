import subprocess
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

console = Console()


def build_hugo(src: Path, dst: Path):
    cmd = [
        "hugo",
        "--minify",
        "--source",
        str(src),
        "--destination",
        str(dst),
        "--cleanDestinationDir",
    ]
    console.print(f"Command: {' '.join(cmd)}")
    console.print(
        Panel(
            f"[bold]Building Hugo site[/bold]\nCommand: {' '.join(cmd)}",
            title="Build Configuration",
            border_style="blue",
        )
    )

    try:
        subprocess.run(
            cmd,
            cwd=src,
            capture_output=True,
            text=True,
            check=True,
        )

    except subprocess.CalledProcessError as e:
        console.print(
            f"\n[red]Error: Hugo build failed with exit code {e.returncode}[/red]"
        )
        if e.stdout:
            console.print(f"\n[dim]stdout:[/dim]\n{e.stdout}")
        if e.stderr:
            console.print(f"\n[dim]stderr:[/dim]\n{e.stderr}")
        sys.exit(1)
