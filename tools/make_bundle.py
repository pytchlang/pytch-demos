import tempfile
import os
import subprocess
import click
import json
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


def ignore_FileNotFoundError(fun, *args, **kwargs):
    try:
        fun(*args, **kwargs)
    except FileNotFoundError:
        pass


def passes_black_check(path):
    result = subprocess.run(["black", "--check", "--quiet", path])
    return result.returncode == 0


def emit_black_results(path):
    subprocess.run(["black", "--diff", "--color", path])


def maybe_convert_to_code_json(entry):
    """Return True/False according to whether a conversion took place.

    Fudge: If this claims to be at least a version-3 zipfile but has a
    code.py file, convert it to a code.json file.  Use case here is that
    we want to have Python code in a more git-friendly representation in
    this demos repo, but still provide a proper zipfile.  We leave the
    code.py file in place so that black can work with it, but will
    exclude it in the main code explicitly when making the zipfile.
    """

    version_path = Path(entry) / "dist/version.json"
    with version_path.open("rt") as version_file:
        version = json.load(version_file)["pytchZipfileVersion"]
        if version >= 3:
            code_path = Path(entry) / "dist/code/code.py"
            if code_path.is_file():
                code_text = code_path.read_text()
                code_obj = {"kind": "flat", "text": code_text}
                json_path = Path(entry) / "dist/code/code.json"
                with json_path.open("wt") as json_file:
                    json.dump(code_obj, json_file)
                return True
    return False


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
    dist_build_basedir = dist_dir / "builds"

    with tempfile.TemporaryDirectory() as builddir:
        os.chdir(builddir)
        subprocess.run(["git", "clone", "--quiet", git_root])

        os.chdir("pytch-demos")
        build_id = head_short_sha()

        dist_build_content_dir = dist_build_basedir / build_id
        os.makedirs(dist_build_content_dir, exist_ok=True)

        print(f"cloned into {builddir} at {build_id}")
        os.chdir("demos")

        demos_with_error = []
        for entry in os.listdir("."):
            if any(fnmatch(entry, pattern) for pattern in EXCLUDE_PATTERNS):
                print(f"skipping excluded {entry}")
            else:
                if os.path.isfile(entry):
                    print(f"adding file {entry}")
                    subprocess.run(["cp", entry, dist_build_content_dir])
                if os.path.isdir(entry):
                    was_converted = maybe_convert_to_code_json(entry)

                    if not passes_black_check(Path(entry) / "dist/code/code.py"):
                        demos_with_error.append(entry)

                    entry_zip = dist_build_content_dir / f"{entry}.zip"
                    ignore_FileNotFoundError(os.remove, entry_zip)
                    print(f"adding zip {entry_zip.name}")
                    with workingdir(Path(entry) / "dist"):
                        extra_opts = ["-x", "code.py"] if was_converted else []
                        subprocess.run(["zip", "-qr", entry_zip, "."] + extra_opts)

        if demos_with_error:
            print("\nblack is not happy:")
            for demo in demos_with_error:
                print("")
                emit_black_results(Path(demo) / "dist/code/code.py")
            print("\nnot creating bundle zipfile")
        else:
            os.chdir(dist_build_basedir)

            bundle_zip = dist_dir / f"demos-{build_id}.zip"

            subprocess.run(["zip", "-0r", bundle_zip, build_id])
            print(f"made {bundle_zip}")

            unit_test_link_path = dist_build_basedir / "fake-build-id-for-tests"
            ignore_FileNotFoundError(os.remove, unit_test_link_path)
            os.symlink(build_id, unit_test_link_path)


if __name__ == "__main__":
    main()
