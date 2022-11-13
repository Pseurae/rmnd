__all__ = ["Store"]

from utils import safe_load, safe_write


class Store(object):
    _fields = None
    _default_mappings = {"username": None, "tasks": None}

    def __init__(self, fname):
        self.fname = fname

    def load(self):
        fields = safe_load(self.fname)
        if fields is None:
            fields = self._default_mappings.copy()

        self._fields = fields

    def save(self):
        if self._fields is None:
            return

        safe_write(self._fields, self.fname)

    def get(self, key, default=None):
        return self._fields.get(key, default)

    def set(self, key, value):
        self._fields[key] = value
        self.save()

