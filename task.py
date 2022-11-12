__all__ = ["Task", "Tasks"]

from datetime import datetime

from rich import box
from rich.align import Align
from rich.table import Table

from utils import get_hash


class Task(object):
    _name = None
    _changed = False
    _full_hash = None
    _status = False
    _added_on = None

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


GREEN_TICK = "[bold green]✓[/bold green]"
RED_CIRCLE = "[bold red]○[/bold red]"


class Tasks(object):
    _tasks = None
    _change_cb = None

    def __init__(self, tasks, change_cb=None):
        self._tasks = tasks
        self._change_cb = change_cb

    def add(self, task):
        if self.is_duplicate(task):
            raise Exception("duplicate task.")

        self._tasks.append(task)
        self._change_cb()

    def remove(self, no):
        if not self.has_task(no):
            raise IndexError("task no out of bounds.")

        task = self._tasks[no]
        del self._tasks[no]
        self._change_cb()

        return True

    def swap(self, old, new):
        if not self.has_task(old):
            raise IndexError("task no out of bounds.")

        if not self.has_task(new):
            raise IndexError("task no out of bounds.")

        self._tasks[old], self._tasks[new] = self._tasks[new], self._tasks[old]
        self._change_cb()

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

        self._change_cb()

    def mark_all(self, status):
        for t in self._tasks:
            t.set_status(status)

        self._change_cb()

    def clear(self):
        self._tasks.clear()
        self._change_cb()

    def remove_done(self):
        for t in self._tasks[:]:
            if t.status:
                self._tasks.remove(t)
        self._change_cb()

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

    # filt: "all", "done", "pending"
    def create_table(self, filt="all"):
        match filt:
            case "all":
                return self._create_table()
            case "done":
                return self._create_table(lambda t: t.status)
            case "pending":
                return self._create_table(lambda t: not t.status)
            case _:
                raise Exception("Value of filt must be all, done or pending.")

    def count_tasks(self, filt="all"):
        match filt:
            case "all":
                return len(self._tasks)
            case "done":
                return len([t for t in self._tasks if t.status])
            case "pending":
                return len([t for t in self._tasks if not t.status])
            case _:
                raise Exception("Value of filt must be all, done or pending.")

