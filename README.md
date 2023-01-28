# rmnd
> A Minimal CLI Todo List.  

By **@Adhith Chand Thiruvath**

rmnd (called remind) is a todo list made with Python using Click, Typer, Rich and pickle. It has an emphasis on code simplicity and directness.

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

## Screenshots

<img width="503" alt="image1" src="https://user-images.githubusercontent.com/46568705/215254272-24799ccc-a435-4308-9f43-58fba09413cb.png">
<img width="494" alt="image2" src="https://user-images.githubusercontent.com/46568705/215254275-03f3071a-1d8b-41f5-acee-6a9c29bfbc14.png">  
<img width="503" alt="image3" src="https://user-images.githubusercontent.com/46568705/215254276-89762a0b-9e8f-4997-a412-3f56b15004a8.png">
<img width="503" alt="image4" src="https://user-images.githubusercontent.com/46568705/215254278-fbe3d6b1-655c-4ec1-8243-91a72e888423.png">
<img width="503" alt="image5" src="https://user-images.githubusercontent.com/46568705/215254279-9281cd27-1181-4103-9c2a-43fa9e103e74.png">
<img width="570" alt="image6" src="https://user-images.githubusercontent.com/46568705/215254281-f0acf1c7-ec4f-4e74-b6eb-341011b84fca.png">
<img width="567" alt="image7" src="https://user-images.githubusercontent.com/46568705/215254282-68743a36-9283-49eb-ad71-495a00489ca7.png">
<img width="503" alt="image9" src="https://user-images.githubusercontent.com/46568705/215254283-f34c263e-a9cd-4423-8c80-b0ba0d500043.png">
