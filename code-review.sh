#! /bin/bash

REPONAME="$(basename -s .git `git config --get remote.origin.url`)"
UPSTREAM_ORGANISATION="herts-astrostudents"
if [[ "$(git config --get remote.origin.url)" != "git@"* ]]; then
	PREFIX="https://github.com/"
else
	PREFIX="git@github.com:"
fi
UPSTREAM="$PREFIX$UPSTREAM_ORGANISATION/$REPONAME.git"
CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
TOPLEVEL="$(git rev-parse --show-toplevel)"


require_clean(){
	if ! [[ -z "$(git status --porcelain)" ]]; then
		git status
		echo "please commit changes here before starting next task"
		exit 1
	fi
}


case $1 in
	'first-time-setup' )
		git config push.default simple
		(git remote add upstream "$UPSTREAM" &&
		git checkout master &&
		git fetch upstream && 
		git merge upstream/master &&
		(git branch solutions || echo "solutions branch already exists") &&
		git checkout master &&
		echo "Linked to upstream repository, created solutions branch." &&
		echo "Now use ./code-review.sh start-task to start the latest task" &&
		exit 0) ||
		echo "Failed: have you already done first-time-setup?" && exit 0
		;;
	'view' )
		if [ $# -gt 3 ] || [ $# -lt 2 ]; then
			echo "incorrect usage"
			echo "USAGE: ./code-review.sh view-solution <USERNAME> [<BRANCH>=solutions]"
			exit 1
		elif [[ $# -eq 3 ]]; then
			USERNAME=$2
			BRANCH=$3
		elif [[ $# -eq 2 ]]; then
			USERNAME=$2
			BRANCH="solutions"
		else
			echo "incorrect usage"
			echo "USAGE: ./code-review.sh view-solution <USERNAME> [<BRANCH>=solutions]"
			exit 1
		fi
		require_clean
		echo 'adding repository and checking out'
		git remote add "$USERNAME" "$PREFIX$USERNAME/$REPONAME.git"
		git fetch "$USERNAME" "$BRANCH" || exit 1
		(git checkout -b "$USERNAME-$BRANCH" "$USERNAME/$BRANCH") || (git checkout "$USERNAME-$BRANCH" && git reset --hard FETCH_HEAD && git clean -df)
		exit 0
		;;
	'start-next-task' )
		if [[ $# -ne 2 ]]; then
			echo "incorrect usage"
			echo "USAGE: ./code-review.sh start-task <TASK-NAME>"
			exit 1
		fi
		require_clean &&
		cd "$TOPLEVEL" &&
		git fetch upstream &&
		git checkout master && 
		git merge upstream/master &&
		git checkout -b "$2-solution" &&
		echo "Now on branch $2-solution, do your work here and then run ./code-review.sh finish-task to commit and upload"
		exit 0
		;;
	'finish-task' )
		if [[ $# -ne 2 ]]; then
			echo "incorrect usage"
			echo "USAGE: ./code-review.sh finish-task <TASK-NAME>"
			exit 1
		fi
		read -p "Submit finished task $2? [enter]"
		require_clean &&
		cd "$TOPLEVEL" &&
		git checkout solutions &&
		git merge "$2-solution" -m "finish $2-solution" &&
		git push --set-upstream origin solutions &&
		echo "Now open a pull request on github.com and your're done!"
		exit 0
		;;
	'update-task' )
		if [[ $# -ne 2 ]]; then
			echo "incorrect usage"
			echo "USAGE: ./code-review.sh update-task <TASK-NAME>"
			exit 1
		fi
		read -p "This will pull any changes from the remote repository. Continue? [enter]"
		require_clean &&
		cd "$TOPLEVEL" &&
		(git checkout "$2-solution" && 
		git fetch upstream && 
		git checkout master && 
		git merge upstream/master &&
		git rebase master "$2-solution" &&
		echo "Update succeeded, continue as you were. You may notice some changes from upstream!") || (echo "update failed...")
		git checkout "$CURRENT_BRANCH"
		exit 0
		;;
	'develop' )
		case $2 in
			'create-task' )
				if [[ $# -ne 3 ]]; then
					echo "incorrect usage"
					echo "USAGE: ./code-review.sh develop create-task <TASK-NAME>"
					exit 1
				fi
				require_clean &&
				( git checkout develop || (echo "make a develop branch first" && exit 1) ) &&
				echo "Updating develop branch" &&
				git fetch upstream && 
				git merge upstream/develop && 
				(git checkout -b "task-$3" || exit 1) &&
				( (mkdir "Task $3" && cd "Task $3")  || exit 1) && 
				echo "Now make the task in the Task $3 folder. Use ./code-review.sh develop publish-task $3 to finish & publish it to github"
				exit 0
				;;
			'publish-task' )
				if [[ $# -ne 3 ]]; then
					echo "incorrect usage"
					echo "USAGE: ./code-review.sh develop publish-task <TASK-NAME>"
					exit 1
				fi
				require_clean &&
				cd "$TOPLEVEL" &&
				(git push --set-upstream origin "task-$3" || exit 1) &&
				echo "Now open a pull request against $UPSTREAM on github for task-$3"
				echo "To make further changes to this task do git checkout task-$3"
				exit 0
				;;
		esac

esac

echo "incorrect usage"
echo "USAGE: ./code-review.sh <first-time-setup|view|start-next-task|finish-task|update-task|develop>"
exit 1