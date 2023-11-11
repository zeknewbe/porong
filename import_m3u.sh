#!/bin/bash

# Variables
SOURCE_REPO="git@github.com:jsosao/m3u/main/mylist.m3u8.git"
DEST_REPO="git@github.com:zeknewbe/porong.git"
FILE_PATH="mylist.m3u8"   # Path to the file you want to import in the source repo
DEST_PATH="mylist.m3u8"     # Path where you want the file to be in the destination repo

# Clone destination repo
git clone $DEST_REPO && cd $(basename $_ .git)

# Add source repo as a remote and fetch its commits
git remote add source_repo $SOURCE_REPO
git fetch source_repo

# Checkout the specific file from source repo
git checkout source_repo/main -- $FILE_PATH

# Ensure the destination directory exists
mkdir -p $(dirname $DEST_PATH)

# Move the file to the desired location in the destination repo
mv $FILE_PATH $DEST_PATH

# Commit and push the changes
git add $DEST_PATH
git commit -m "Imported $FILE_PATH from jsosao/m3u/main/mylist.m3u8"
git push origin main

# Cleanup by removing the added remote
git remote remove source_repo

echo "File imported successfully!"
