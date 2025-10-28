import argparse
import os
import sys
from pathlib import Path

from staticjinja import Site
from dotenv import load_dotenv

def get_context() -> dict[str, str]:
    context = {}
    prefix = "SJP_"
    for key in os.environ.keys():
        if key.startswith(prefix):
            context[key.removeprefix(prefix).lower()] = os.environ[key]
    return context


def validate_source_directory(path: Path):
    if not path.exists():
        print(f"Source directory {path} does not exist", file=sys.stderr)
        return False

    if not path.is_dir():
        print(f"Source directory {path} is not a directory", file=sys.stderr)
        return False

    try:
        all_html_files = list(path.glob("*.html"))
        if not all_html_files:
            print(f"Source directory {path} is empty", file=sys.stderr)
            return False

        unreadable_files = []
        for file in all_html_files:
            if not os.access(file, os.R_OK):
                unreadable_files.append(file)

        if unreadable_files:
            print(f"Permission denied: cannot read files:", file=sys.stderr)
            for file in unreadable_files:
                print(f"  {file}", file=sys.stderr)
            return False

    except PermissionError:
        print(f"Permission denied: cannot list files in {path}", file=sys.stderr)
        return False

    return True

def validate_output_directory(path: Path):
    if path.exists() and not path.is_dir():
        print(f"Output path {path} is not a directory", file=sys.stderr)
        return False

    try:
        path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"Permission denied: cannot create output directory {path}", file=sys.stderr)
        return False

    try:
        test_file = path / ".test_write"
        test_file.touch()
        test_file.unlink()
    except PermissionError:
        print(f"Permission denied: cannot write to output directory {path}", file=sys.stderr)
        return False

    return True


def main() -> None:
    load_dotenv(override=True)

    parser = argparse.ArgumentParser(
        description="Render HTML pages from Jinja templates",
    )
    parser.add_argument(
        "-w",
        "--watch",
        help="Render the site, and re-render on changes to <srcpath>",
        action="store_true",
    )
    parser.add_argument(
        "--srcpath",
        help="The directory to look in for templates (defaults to './templates)'",
        default=Path(".") / "templates",
        type=Path,
    )
    parser.add_argument(
        "--outpath",
        help="The directory to place rendered files in (defaults to './build')",
        default=Path(".") / "build",
        type=Path,
    )

    args = parser.parse_args()

    src_path = args.srcpath
    output_path = args.outpath
    static_path = Path(src_path) / "assets"

    if not validate_source_directory(src_path):
        return

    if not validate_output_directory(output_path):
        return

    site = Site.make_site(
        searchpath=src_path,
        outpath=output_path,
        staticpaths=[
            str(static_path),
        ],
        contexts=[(".*.html", get_context)],
    )

    site.render(use_reloader=args.watch)


if __name__ == '__main__':
    main()
