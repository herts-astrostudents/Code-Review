# Code-Review
Hertfordshire astronomers code review sessions

The way we're going to this is by having everyone make fork of this repository and work on separate branches. Each task shall have its own folder!

## git configuration
### Setup git and github for a new machine

    git config --global user.name "Firstname Lastname"
    git config --global user.email "mygithubemailaddress@gmail.com"
    git config --global core.editor nano 
    for windows: 
        git config --global core.autocrlf true 
    for all others:
        git config --global core.autocrlf input


### Student privileges
Go to https://education.github.com/discount_requests/new to get free unlimited private repos and all sorts of free stuff!


### Optional extras:
Install the [git-extras package](https://github.com/tj/git-extras) for the `undo/sync/pr` commands (really useful)
Install [bash-git-prompt](https://github.com/magicmonty/bash-git-prompt) to make the terminal tell you whats happening with git 
[GitKraken](https://www.gitkraken.com/) is a really good visualisation and GUI interface to git. It runs on any platform and github gives free premium access to students!


#### Atlassian git resources
[Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials) are really useful to understand exactly what git/github are doing. It has some good documentation and diagrams

[Cheat Sheet](https://www.atlassian.com/git/tutorials/atlassian-git-cheatsheet)


## Task Flow:
Install the `code-review.sh script` in your preferred directory (not the same as the code-review directory!!):

    git clone https://github.com/herts-astrostudents/code-review.sh && cd code-review.sh && chmod +x code-review.sh && ./code-review.sh install

## Doing the tasks
The steps below show you how to do a task that has been put up on github. `<NAME>` is just the name of the branch that you are doing your task on. So if the task has a folder called `Task 6` use `6` or maybe `task-6` as `<NAME>`.

0. First time setup `code-review.sh first-time-setup herts-astrostudents` (run this only once ever)
1. `code-review.sh start-task <NAME>`
2. Do the task, using git to track progress if you want
3. `code-review.sh finish-task <NAME>`
4. "Submit a pull request" to `herts-astrostudents` on github (pull requests are how people submit improvements for inspection on github)

To checkout other people's pull requests during the session, run `git pr <pull request number> upstream` or use `code-review.sh view <USERNAME>` to directly view their solution branch without a pull request.


## Writing a task for the group
For anyone who wants to write a task for the group:
The goal is to have a separate branch for you task and then merge it with the master branch.
Each task should have a `readme.md` to explain what to to and a script to run to test/produce the desired output.
i.e. it should contain `task.py` and `solution.py`.
We are also working exclusively in python and miscellaneous command line applications. No IDL!

1. `code-review.sh develop create-task <NAME>` (this will make a folder called `Task <NAME>`)
2. Write the task in the task folder along with the solution!
3. `code-review.sh develop begin-finalise-task <NAME>`
4. Remove the solution so only the task remains!
5. `code-review.sh develop end-finalise-task <NAME>`
5. `code-review.sh develop publish-task <NAME>`
6. Submit a pull request to `herts-astrostudents` for the branch `task-<NAME>` on github and the maintainer will merge it.
7.  `code-review.sh develop publish-solution <NAME>` to publish your solution like everyone else
8. Submit a pull request to `herts-astrostudents` for the branch `solutions` on github and the maintainer will merge it.
9. Go to the code review session


## Repository Maintenance (admin)
For the admin(s) maintaining this repo:
The goal is to have everyone push their own repo to their own branch on the upstream repo (so everyone can easily access the solutions).

1. Look at pull requests for written tasks 
    * Merge onto the master branch 
1. Look at the solution pull requests. 
    * Create a new branch from the master (named `solution-<PERSON>`) (on github)
    * Direct the pull request to their own personalised solution branch (so make sure that `<person1>` has their solution pull request against `solution-<person1>`)
1. Merge the pull request into the personalised branch (on github)
1. DO NOT PUBLISH SOLUTIONS TO THE DEVELOPMENT OR MASTER BRANCHES, do them on their own branches.

The git tree should have branches:

* *Master* (Do not edit directly. Should only be merged with!)
* *solution-person1* (only for the solutions of person 1)
* *solution-person2* (only for the solutions of person 2)
* etc...

