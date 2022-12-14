__all__ = ["Task", "Tasks"]

from datetime import datetime

from rich import box
from rich.align import Align
from rich.table import Table

from utils import get_hash


class Task(object):
    _name: str = None
    _full_hash: str = None
    _status: bool = False
    _added_on: datetime = None

    _changed: bool = False

    @property
    def name(self):
        return self._name

    @property
    def hash(self):
        return self.full_hash[:6]

    @property
    def full_hash(self):
        if self._changed:
            self._full_hash = get_hash(self._name)

        return self._full_hash

    @property
    def status(self):
        return self._status

    @property
    def added_on(self):
        return self._added_on

    def rename(self, name):
        self._name = name
        self._changed = True

    def set_status(self, status):
        self._status = status

    def __init__(self, name):
        self.rename(name)
        self._added_on = datetime.now()

    def __eq__(self, other):
        if type(self) is not type(other):
            return False

        return self.full_hash == other.full_hash

    def __ne__(self, other):
        return not (self == other)

    def __getstate__(self):
        return (self._name, self._added_on, self._status)

    def __setstate__(self, i):
        self.rename(i[0])
        self._added_on = i[1]
        self.set_status(i[2])


GREEN_TICK = "[bold green]✓[/bold green]"
RED_CIRCLE = "[bold red]○[/bold red]"


class Tasks(object):
    _tasks = None
    _changed_cb = None

    def __init__(self, tasks, changed_cb=None):
        self._tasks = tasks
        self._changed_cb = changed_cb

    # Disable setting of _tasks after constructor
    def __setattr__(self, field, value):
        if field == "_tasks" and getattr(self, "_tasks") is not None:
            raise ValueError("Cannot set _tasks after initialization.")

        super().__setattr__(field, value)

    def post_change(self):
        if self._changed_cb is not None:
            self._changed_cb()

    def add(self, task):
        if self.is_duplicate(task):
            raise Exception("duplicate task.")

        self._tasks.append(task)
        self.post_change()

    def remove(self, no):
        if not self.has_task(no):
            raise IndexError("task no out of bounds.")

        task = self._tasks[no]
        del self._tasks[no]
        self.post_change()

        return True

    def swap(self, old, new):
        if not self.has_task(old):
            raise IndexError("task no out of bounds.")

        if not self.has_task(new):
            raise IndexError("task no out of bounds.")

        self._tasks[old], self._tasks[new] = self._tasks[new], self._tasks[old]
        self.post_change()

    def change(self, no, name=None, status=None):
        if name is None and status is None:
            raise Exception("name and status arguments are exhaustive.")

        if not self.has_task(no):
            raise Exception("task no out of bounds.")

        task = self._tasks[no]

        if name is not None:
            task.rename(name)

        if status is not None:
            task.set_status(status)

        self.post_change()

    def mark_all(self, status):
        for t in self._tasks:
            t.set_status(status)

        self.post_change()

    def clear(self):
        self._tasks.clear()
        self.post_change()

    def remove_done(self):
        for t in self._tasks[:]:
            if t.status:
                self._tasks.remove(t)
        self.post_change()

    def is_duplicate(self, val):
        return val in self._tasks

    def has_task(self, no):
        return no < len(self._tasks)

    def get(self, no):
        return self._tasks[no]

    def _create_table(self, fil_fn=None):
        table = Table("No.", "Name", "Hash", "Added On", "Status", box=box.MINIMAL)

        for i, t in enumerate(self._tasks):
            if fil_fn is not None and not fil_fn(t):
                continue

            no = Align(f"{i + 1}", align="right")
            name = Align(t.name, align="left")
            hash = Align(t.hash, align="center")
            added_on = Align(t.added_on.strftime("%c"), align="center")
            status = Align(GREEN_TICK if t.status else RED_CIRCLE, align="center")

            table.add_row(no, name, hash, added_on, status)

        return table

    _filter_funcs = {
        "all": lambda t: True,
        "done": lambda t: t.status,
        "pending": lambda t: not t.status,
    }

    # filt: "all", "done", "pending"
    def create_table(self, filt="all"):
        filter_func = self._filter_funcs.get(filt)
        if filter_func is not None:
            return self._create_table(filter_func)

        raise Exception("Value of filt must be all, done or pending.")

    def count_tasks(self, filt="all"):
        filter_func = self._filter_funcs.get(filt)
        if filter_func is not None:
            return len([t for t in self._tasks if filter_func(t)])

        raise Exception("Value of filt must be all, done or pending.")
