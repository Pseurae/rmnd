# rmnd
> A Minimal CLI Todo List.  

By **@Adhith Chand Thiruvath**

rmnd (called remind) is a todo list made with Python using Click, Typer, Rich and pickle.  

rmnd is made as my (Adhith Chand Thiruvath's) final year CS investigatory project submission.

## Commands

```console
$ python rmnd.py --help

Usage: rmnd.py [OPTIONS] COMMAND [ARGS]...

  Remind - A Minimal CLI Todo List

Options:
  --store-path PATH     Use another file to save.  [default: store.rmnd]
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  add          Append a task to the list.
  callme       Change Username.
  clear        Delete all tasks from the list.
  delete       Delete a task from the list.
  done         Display all done tasks.
  mark         (Section) Marking tasks.
  move         Change task order.
  pending      Display all pending tasks.
  remove-done  Delete all finished tasks.
  rename       Rename a task.
  tasks        Display all tasks in the list.

Made by Adhith

$ python rmnd.py mark --help
Usage: rmnd.py mark [OPTIONS] COMMAND [ARGS]...

  (Section) Marking tasks.

Options:
  --help  Show this message and exit.

Commands:
  all-done     Mark all tasks as finished.
  all-pending  Mark all tasks as unfinished.
  done         Mark a task as finished.
  pending      Mark a task as unfinished.

Made by Adhith
```
