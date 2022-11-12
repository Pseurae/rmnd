import os
import typing
from hashlib import sha1
from pickle import dump, load

from click.exceptions import ClickException


def safe_load(fname):
    if os.path.exists(fname):
        with open(fname, "rb") as f:
            return load(f)

    return None


def safe_write(obj, fname):
    with open(fname, "wb") as f:
        dump(obj, f)


def get_hash(name):
    return sha1(name.encode("utf-8")).hexdigest()


class RMNDException(ClickException):
    def format_message(self):
        return f"{self.message}"
