import subprocess
from pathlib import Path

from rich.console import Console

console = Console()


class HugoBuilder:
    """Hugo site builder with rich output and error handling."""

    def __init__(self, hugo_dir: Path, output_dir: Path):
        self.hugo_dir = hugo_dir
        self.output_dir = output_dir

    def validate_setup(self) -> bool:
        """Validate that Hugo is properly set up."""
        if not self.hugo_dir.exists():
            console.print(f"[red]Error: Hugo directory '{self.hugo_dir}' does not exist[/red]")
            return False

        if not (self.hugo_dir / "hugo.toml").exists():
            console.print(f"[red]Error: No hugo.toml found in '{self.hugo_dir}'[/red]")
            return False

        return True

    def check_hugo_installed(self) -> bool:
        """Check if Hugo is installed and available."""
        try:
            result = subprocess.run(
                ["hugo", "version"],
                capture_output=True,
                text=True,
                check=True,
            )
            console.print(f"[green]Found Hugo: {result.stdout.strip()}[/green]")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            console.print("[red]Error: Hugo is not installed or not in PATH[/red]")
            return False

    def build(
        self,
        draft: bool = False,
        future: bool = False,
        minify: bool = False,
        verbose: bool = False,
    ) -> bool:
        """Build the Hugo site."""
        if not self.validate_setup():
            return False

        if not self.check_hugo_installed():
            return False

        # Prepare Hugo command
        cmd = ["hugo"]

        if not draft:
            cmd.append("--buildDrafts=false")
        if not future:
            cmd.append("--buildFuture=false")
        if minify:
            cmd.append("--minify")
        if verbose:
            cmd.append("--verbose")

        cmd.extend([
            "--source", str(self.hugo_dir),
            "--destination", str(self.output_dir),
        ])

        # Execute build
        try:
            result = subprocess.run(
                cmd,
                cwd=self.hugo_dir,
                capture_output=True,
                text=True,
                check=True,
            )

            if verbose and result.stdout:
                console.print("\n[dim]Build output:[/dim]")
                console.print(result.stdout)

            return True

        except subprocess.CalledProcessError as e:
            console.print(f"\n[red]Error: Hugo build failed with exit code {e.returncode}[/red]")
            if e.stdout:
                console.print(f"\n[dim]stdout:[/dim]\n{e.stdout}")
            if e.stderr:
                console.print(f"\n[dim]stderr:[/dim]\n{e.stderr}")
            return False

    def get_build_stats(self) -> dict | None:
        """Get statistics about the built site."""
        if not self.output_dir.exists():
            return None

        total_files = sum(1 for _ in self.output_dir.rglob("*") if _.is_file())
        total_size = sum(f.stat().st_size for f in self.output_dir.rglob("*") if f.is_file())

        return {
            "files": total_files,
            "size_bytes": total_size,
            "size_mb": total_size / 1024 / 1024,
        }


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def get_hugo_dir() -> Path:
    """Get the Hugo directory path."""
    return get_project_root() / "hugo"


def get_output_dir() -> Path:
    """Get the default output directory path."""
    return get_hugo_dir() / "public"
