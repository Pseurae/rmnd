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

store: Store = None
tasklist: Tasks = None
console = Console()

IndexArg = typer.Argument(..., min=1)


def _retrieve_tasklist(store):
    """
    Returns the list of stored tasks or creates a list if one doesn't exist.
    """

    tl = store.get("tasks")

    if tl is None:
        store.set("tasks", [])
        return _retrieve_tasklist(store)

    return tl


def _check_username(store):
    """
    Returns True is username exists in the store.
    Prompts the user to enter a username and returns False if username doesn't exist.
    """

    if store.get("username"):
        return True

    username = typer.prompt("Enter Username")
    store.set("username", username)
    return False


def initialize_store(fname):
    """
    Initializes the pickle store and tasklist.
    """

    global store, tasklist

    store = Store(fname)
    store.load()

    tasklist = Tasks(_retrieve_tasklist(store), store.save)


def is_empty_string(s):
    """
    Check whether string is empty.
    Whitespace is also counted as empty.
    """
    return not s or s.isspace()


def draw_tasks_progress_bar():
    """
    Draws a progress bar for the tasklist.
    """

    tasks_count = tasklist.count_tasks()
    done_count = tasklist.count_tasks("done")

    progress = Progress(BarColumn(), MofNCompleteColumn(), console=console)

    with progress:
        task = progress.add_task("Progress", total=tasks_count)
        progress.update(task, advance=done_count)


"""
Start of Typer Commands.
"""


@remind.command(help="Append a task to the list.", rich_help_panel="Define")
def add(name: str):
    if is_empty_string(name):
        raise typer.BadParameter("Task name cannot be an empty string!")

    task = Task(name)

    if tasklist.is_duplicate(task):
        raise RMNDException("Task already exists!")

    tasklist.add(task)
    console.print(f'Task "{name}" has been added.')
    tasks_check()


@remind.command(help="Delete a task from the list.", rich_help_panel="Define")
def delete(task_id: int = IndexArg):
    if not tasklist.has_task(task_id - 1):
        raise RMNDException(f"Task #{task_id} does not exist!")

    typer.confirm(f"Are you sure that you want to delete Task #{task_id}?", abort=True)

    tasklist.remove(task_id - 1)
    console.print(f"Task #{task_id} has been deleted.")
    tasks_check()


@remind.command(help="Rename a task.", rich_help_panel="Modify")
def rename(task_id: int = IndexArg, name: str = typer.Argument(...)):
    if not tasklist.has_task(task_id - 1):
        raise RMNDException(f"Task #{task_id} does not exist!")

    tasklist.change(task_id - 1, name)
    console.print(f"Task #{task_id} has been renamed to {name}.")
    tasks_check()


@remind.command(help="Change task order.", rich_help_panel="Modify")
def move(old_id: int = IndexArg, new_id: int = IndexArg):
    if not tasklist.has_task(old_id - 1):
        raise RMNDException(f"Task #{old_id} does not exist!")

    if not tasklist.has_task(new_id - 1):
        raise RMNDException(f"Task #{new_id} does not exist!")

    tasklist.swap(old_id - 1, new_id - 1)
    console.print(f"Task #{old_id} has been moved to {new_id}.")
    tasks_check()


@remind.command(help="Delete all tasks from the list.", rich_help_panel="Define")
def clear():
    typer.confirm(f"Are you sure that you want to clear your tasklist?", abort=True)

    tasklist.clear()
    console.print("Tasklist has been cleared.")


@remind.command(help="Delete all finished tasks.", rich_help_panel="Define")
def remove_done():
    typer.confirm(
        f"Are you sure that you want to remove all completed tasks?", abort=True
    )

    tasklist.remove_done()
    console.print(f"All completed tasks have been removed.")
    tasks_check()


@remind.command(help="Change username.", rich_help_panel="Settings")
def callme(name: str):
    if is_empty_string(name):
        raise typer.BadParameter("Username cannot be an empty string!")

    typer.confirm(
        f"Are you sure that you want to change your username to {name}?", abort=True
    )

    store.set("username", name)
    console.print(f"Username has been changed to [bold cyan]{name}[/bold cyan].")


@remind.command(help="Display all done tasks.", rich_help_panel="Display")
def done():
    table = tasklist.create_table("done")

    if table.rows:
        console.print(table)
    else:
        console.print("No done tasks.")


@remind.command(help="Display all pending tasks.", rich_help_panel="Display")
def pending():
    table = tasklist.create_table("pending")

    if table.rows:
        console.print(table)
    else:
        console.print("No pending tasks.")


@remind.command(help="Display all tasks in the list.", rich_help_panel="Display")
def tasks():
    table = tasklist.create_table("all")

    if table.rows:
        console.print(table)
    else:
        console.print("No tasks.")


def mark_single(task_id, status):
    """
    Marks a task with the given status.
    Also handles exception if task ID out of bounds.
    """

    if not tasklist.has_task(task_id - 1):
        raise RMNDException(f"Task #{task_id} does not exist!")

    tasklist.change(task_id - 1, status=status)


@mark_sub.command(help="Mark a task as finished.", name="done")
def mark_done(task_id: int = IndexArg):
    mark_single(task_id, True)
    console.print(f"Task #{task_id} has been marked done.")
    tasks_check()


@mark_sub.command(help="Mark a task as unfinished.", name="pending")
def mark_pending(task_id: int = IndexArg):
    mark_single(task_id, False)
    console.print(f"Task #{task_id} has been marked pending.")
    tasks_check()


@mark_sub.command(help="Mark all tasks as finished.", name="all-done")
def mark_all_done():
    typer.confirm(
        "Are you sure that you want to mark all tasks as completed?", abort=True
    )

    tasklist.mark_all(True)
    console.print("All tasks have been marked as done.")
    tasks_check()


@mark_sub.command(help="Mark all tasks as unfinished.", name="all-pending")
def mark_all_pending():
    typer.confirm(
        "Are you sure that you want to mark all tasks as incomplete?", abort=True
    )

    tasklist.mark_all(False)
    console.print("All tasks have been marked as pending.")
    tasks_check()


def tasks_check():
    """
    Post-command callback to display task details after commands are finished.
    """

    tasks_count = tasklist.count_tasks()
    pending_count = tasklist.count_tasks("pending")

    if not tasks_count:
        console.print(f"No tasks found.")
    else:
        tasks()
        draw_tasks_progress_bar()

        if not pending_count:
            console.print("No pending tasks remaining!")


def welcome(ctx):
    """
    Called when rmnd is ran without a command.
    """

    username = store.get("username")
    console.print(f"Hello [bold cyan]{username}[/bold cyan].")
    tasks_check()

    if not tasklist.count_tasks():
        console.print(f"Use '{ctx.info_name} add' to create a task!")


def first_startup(ctx):
    """
    Called on first startup after username prompt.
    """

    username = store.get("username")
    console.print(f"Welcome [bold cyan]{username}[/bold cyan]!")

    if ctx.invoked_subcommand is None:
        console.print(f"Use '{ctx.info_name} add' to create a task!")
        raise typer.Exit()


@remind.callback(
    invoke_without_command=True,
    help="Remind - A Minimal CLI Todo List",
    epilog="Made by Adhith",
)
def main(
    ctx: typer.Context,
    store_path: Path = typer.Option("store.rmnd", help="Use another file to save."),
):
    """
    Callback that initializes the store and tasklist before the respective command function is called.
    Invokes welcome function when no commands are supplied.
    """

    initialize_store(store_path.resolve())

    assert store is not None
    assert tasklist is not None

    if not _check_username(store):
        first_startup(ctx)

    if ctx.invoked_subcommand is None:
        welcome(ctx)
