# guhcampos

Build tools for guhcampos.github.io - a Hugo-based personal website.

## Features

- **Hugo Build Management**: Streamlined Hugo site building with rich output
- **Development Server**: Easy Hugo development server management
- **Build Statistics**: Track build performance and output metrics
- **Rich CLI**: Beautiful command-line interface with progress indicators

## Installation

This package is part of the guhcampos.github.io repository and uses `uv` for dependency management.

```bash
# Install dependencies
uv sync

# Install the package in development mode
uv pip install -e .
```

## Usage

### Building the Hugo Site

```bash
# Basic build
build

# Build with options
build --clean --minify --verbose

# Build with drafts and future content
build --draft --future
```

### Development Server

```bash
# Start development server
build serve

# Custom port and binding
build serve --port 8080 --bind 0.0.0.0

# Include drafts
build serve --draft
```

### Command Options

#### Build Command
- `--hugo-dir`: Hugo site directory (default: `hugo`)
- `--output-dir`: Output directory (default: `hugo/public`)
- `--clean`: Clean output directory before building
- `--draft`: Include draft content
- `--future`: Include future-dated content
- `--minify`: Minify the output
- `--verbose`: Enable verbose output

#### Serve Command
- `--hugo-dir`: Hugo site directory (default: `hugo`)
- `--port`: Port to serve on (default: 1313)
- `--bind`: Address to bind to (default: 127.0.0.1)
- `--draft`: Include draft content
- `--future`: Include future-dated content

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=guhcampos

# Run specific test file
uv run pytest tests/test_core.py
```

### Code Quality

```bash
# Format code
uv run black src/ tests/

# Sort imports
uv run isort src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

## Project Structure

```
src/guhcampos/
├── __init__.py      # Package initialization
├── cli.py          # Click-based command-line interface
├── core.py         # Core build utilities and Hugo integration
└── README.md       # This file
```

## Dependencies

- **click**: Command-line interface creation
- **rich**: Rich text and beautiful formatting in the terminal
- **pathspec**: Path pattern matching
- **watchdog**: File system monitoring (for future features)

## License

MIT License - see the main repository LICENSE file.
