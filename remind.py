__all__ = ["remind"]

from pathlib import Path

import typer
from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress

from store import Store
from task import Task, Tasks
from utils import RMNDException

remind = typer.Typer(rich_markup_mode="rich")
mark_sub = typer.Typer(rich_markup_mode="rich")
remind.add_typer(
    mark_sub, name="mark", help="(Section) Marking tasks.", rich_help_panel="Modify"
)

store = None
tasklist = None
console = Console()

IndexArg = typer.Argument(..., min=1)


def _retrieve_tasklist(store):
    tl = store.get("tasks")

    if tl is None:
        store.set("tasks", [])
        return _retrieve_tasklist(store)

    return tl


def _check_username(store):
    if store.get("username"):
        return False

    username = typer.prompt("Enter Username")
    store.set("username", username)
    return True


def initialize_store(fname):
    global store, tasklist

    store = Store(fname)
    store.load()

    tasklist = Tasks(_retrieve_tasklist(store), store.save)


def is_empty_string(s):
    return not s or s.isspace()


def draw_tasks_progress_bar():
    tasks_count = tasklist.count_tasks()
    done_count = tasklist.count_tasks("done")

    progress = Progress(BarColumn(), MofNCompleteColumn())

    with progress:
        task = progress.add_task("Progress", total=tasks_count)
        progress.update(task, advance=done_count)


"""
Start of Typer Commands.
"""


@remind.command(rich_help_panel="Define")
def add(name: str):
    """Append a task to the list."""

    if is_empty_string(name):
        raise typer.BadParameter("Task name cannot be an empty string!")

    task = Task(name)

    if tasklist.is_duplicate(task):
        raise RMNDException("Task already exists!")

    tasklist.add(task)
    console.print(f'Task "{name}" has been added.')
    tasks_check()


@remind.command(rich_help_panel="Define")
def delete(task_id: int = IndexArg):
    """Delete a task from the list."""

    if not tasklist.has_task(task_id - 1):
        raise RMNDException(f"Task #{task_id} does not exist!")

    typer.confirm(
        f"Are you sure that you want to delete Task #{task_id}?", abort=True)

    tasklist.remove(task_id - 1)
    console.print(f"Task #{task_id} has been deleted.")
    tasks_check()


@remind.command(rich_help_panel="Modify")
def rename(task_id: int = IndexArg, name: str = typer.Argument(...)):
    """Rename a task."""

    if not tasklist.has_task(task_id - 1):
        raise RMNDException(f"Task #{task_id} does not exist!")

    tasklist.change(task_id - 1, name)
    console.print(f"Task #{task_id} has been renamed to {name}.")
    tasks_check()


@remind.command(rich_help_panel="Modify")
def move(old_id: int = IndexArg, new_id: int = IndexArg):
    """Change task order."""

    if not tasklist.has_task(old - 1):
        raise RMNDException(f"Task #{old_id} does not exist!")

    if not tasklist.has_task(new - 1):
        return RMNDException(f"Task #{new_id} does not exist!")

    tasklist.swap(old_id - 1, new_id - 1)
    console.print(f"Task #{old_id} has been moved to {new_id}.")
    tasks_check()


@remind.command(rich_help_panel="Define")
def clear():
    """Delete all tasks from the list."""

    typer.confirm(
        f"Are you sure that you want to clear your tasklist?", abort=True)

    tasklist.clear()
    console.print("Tasklist has been cleared.")


@remind.command(rich_help_panel="Define")
def remove_done():
    """Delete all finished tasks."""

    typer.confirm(
        f"Are you sure that you want to remove all completed tasks?", abort=True
    )

    tasklist.remove_done()
    console.print(f"All completed tasks have been removed.")
    tasks_check()


@remind.command(rich_help_panel="Settings")
def callme(name: str):
    """Change Username."""

    if is_empty_string(name):
        raise typer.BadParameter("Username cannot be an empty string!")

    typer.confirm(
        f"Are you sure that you want to change your username to {name}?", abort=True
    )

    store.set("username", name)
    console.print(
        f"Username has been changed to [bold cyan]{name}[/bold cyan].")


@remind.command(rich_help_panel="Display")
def done():
    """Display all done tasks."""

    table = tasklist.create_table("done")

    if table.rows:
        console.print(table)
    else:
        console.print("No done tasks.")


@remind.command(rich_help_panel="Display")
def pending():
    """Display all pending tasks."""

    table = tasklist.create_table("pending")

    if table.rows:
        console.print(table)
    else:
        console.print("No pending tasks.")


@remind.command(rich_help_panel="Display")
def tasks():
    """Display all tasks in the list."""

    table = tasklist.create_table("all")

    if table.rows:
        console.print(table)
    else:
        console.print("No tasks.")


def mark_single(task_id, status):
    if not tasklist.has_task(task_id - 1):
        raise RMNDException(f"Task #{task_id} does not exist!")

    tasklist.change(task_id - 1, status=status)


@mark_sub.command(name="done")
def mark_done(task_id: int = IndexArg):
    """Mark a task as finished."""

    mark_single(task_id, True)
    console.print(f"Task #{task_id} has been marked done.")
    tasks_check()


@mark_sub.command(name="pending")
def mark_pending(task_id: int = IndexArg):
    """Mark a task as unfinished."""

    mark_single(task_id, False)
    console.print(f"Task #{task_id} has been marked pending.")
    tasks_check()


@mark_sub.command(name="all-done")
def mark_all_done():
    """Mark all tasks as finished."""

    typer.confirm(
        "Are you sure that you want to mark all tasks as completed?", abort=True
    )

    tasklist.mark_all(True)
    console.print("All tasks have been marked as done.")
    tasks_check()


@mark_sub.command(name="all-pending")
def mark_all_pending():
    """Mark all tasks as unfinished."""

    typer.confirm(
        "Are you sure that you want to mark all tasks as incomplete?", abort=True
    )

    tasklist.mark_all(False)
    console.print("All tasks have been marked as pending.")
    tasks_check()


def tasks_check():
    """Displays task details after commands."""

    tasks_count = tasklist.count_tasks()
    pending_count = tasklist.count_tasks("pending")

    if not tasks_count:
        console.print(f"No tasks found.")
    else:
        tasks()
        draw_tasks_progress_bar()

        if not pending_count:
            console.print("No pending tasks remaining!")


def welcome():
    """Called when rmnd is ran without a command."""

    username = store.get("username")
    console.print(f"Hello [bold cyan]{username}[/bold cyan].")
    tasks_check()


def first_startup(ctx):
    """Called on first startup."""

    username = store.get("username")
    console.print(f"Welcome [bold cyan]{username}[/bold cyan]!")
    if ctx.invoked_subcommand is None:
        console.print(f"Use '{ctx.info_name} add' to create a task!")
        raise typer.Exit()

@remind.callback(invoke_without_command=True, epilog="Made by Adhith")
def main(
    ctx: typer.Context,
    store_path: Path = typer.Option(
        "store.rmnd", help="Use another file to save."),
):
    """Remind - A Minimal CLI Todo List"""

    initialize_store(store_path.resolve())

    if _check_username(store):
        first_startup(ctx)

    if ctx.invoked_subcommand is None:
        welcome()

    assert store is not None
    assert tasklist is not None
