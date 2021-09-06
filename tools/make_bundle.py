import tempfile
import os
import subprocess
import click
import datetime
from pathlib import Path
from contextlib import contextmanager
from fnmatch import fnmatch

EXCLUDE_PATTERNS = ["README.md", "pyproject.toml"]


@contextmanager
def workingdir(path):
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)


def head_short_sha():
    return (
        subprocess.run(
            ["git", "rev-parse", "--short=12", "HEAD"],
            capture_output=True,
        )
        .stdout.decode("utf8")
        .rstrip()
    )


def passes_black_check(path):
    result = subprocess.run(["black", "--check", "--quiet", path])
    return result.returncode == 0


def emit_black_results(path):
    subprocess.run(["black", "--diff", "--color", path])


@click.command()
def main():
    # TODO: What if pathnames are not encoded in UTF8?
    git_root = (
        subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
        )
        .stdout.decode("utf8")
        .rstrip()
    )

    dist_dir = Path(git_root) / "dist"
    dist_components_dir = dist_dir / "components"
    os.makedirs(dist_components_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as builddir:
        os.chdir(builddir)
        subprocess.run(["git", "clone", "--quiet", git_root])
        print(f"cloned into {builddir}")
        os.chdir("pytch-demos/demos")
        components = []
        demos_with_error = []
        for entry in os.listdir("."):
            if any(fnmatch(entry, pattern) for pattern in EXCLUDE_PATTERNS):
                print(f"skipping excluded {entry}")
            else:
                if os.path.isfile(entry):
                    print(f"adding file {entry}")
                    subprocess.run(["cp", entry, dist_components_dir])
                    components.append(entry)
                if os.path.isdir(entry):
                    if not passes_black_check(Path(entry) / "dist/code/code.py"):
                        demos_with_error.append(entry)

                    entry_zip = dist_components_dir / f"{entry}.zip"
                    try:
                        os.remove(entry_zip)
                    except FileNotFoundError:
                        pass
                    print(f"adding zip {entry_zip.name}")
                    with workingdir(Path(entry) / "dist"):
                        subprocess.run(["zip", "-qr", entry_zip, "."])
                    components.append(entry_zip.name)

        if demos_with_error:
            print("\nblack is not happy:")
            for demo in demos_with_error:
                print("")
                emit_black_results(Path(demo) / "dist/code/code.py")
            print("\nnot creating bundle zipfile")
        else:
            os.chdir(dist_components_dir)

            now = datetime.datetime.now(datetime.timezone.utc)
            timestamp = now.strftime("%Y%m%dT%H%M%SZ")
            bundle_zip = dist_dir / f"demos-{timestamp}.zip"

            subprocess.run(["zip", "-0", bundle_zip] + components)
            print(f"made {bundle_zip}")


if __name__ == "__main__":
    main()
