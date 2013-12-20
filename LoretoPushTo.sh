#!/bin/bash
PrjName=LnFunctions

REPO=/l/Loreto/GIT-REPO-BARE/$LnFunctions.git
REPO=f602250@esil904:/opt/gitrepo/BARE/PythonProjects/$LnFunctions.git


# cd $PrjName
# git status;rCode=$?
# [[ $rCode != 0 ]] && echo "ERRORE" && exit 1

# git commit -a -m "$1";rCode=$?
# [[ $rCode != 0 ]] && echo "ERRORE" && exit 1

git push --repo=$REPO/$PrjName.git; rCode=$?
[[ $rCode != 0 ]] && echo "ERRORE" && exit 1




