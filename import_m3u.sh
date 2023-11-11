#!/bin/bash

# Variables
SOURCE_REPO="jsosao/m3u"  # Replace with the GitHub username/repo
SOURCE_FILE="mylist.m3u8" # The path to the file in the source repo
SOURCE_BRANCH="main"      # The branch where the file is located
DEST_REPO="git@github.com:zeknewbe/porong.git"
DEST_PATH="mylist.m3u8"   # Path where you want the file to be in the destination repo

# Clone destination repo
if git clone "$DEST_REPO"; then
    cd "$(basename "$DEST_REPO" .git)" || exit
else
    echo "Failed to clone destination repository."
    exit 1
fi

# Add source repo as a remote and fetch the file
git remote add source_repo "https://github.com/$SOURCE_REPO.git"
git fetch source_repo $SOURCE_BRANCH

# Checkout the specific file from source repo
if git checkout source_repo/$SOURCE_BRANCH -- "$SOURCE_FILE"; then
    mv "$SOURCE_FILE" "$DEST_PATH"  # Move the file to the desired location in the destination repo
    git add "$DEST_PATH"
    git commit -m "Imported $SOURCE_FILE from $SOURCE_REPO"
    if git push origin main; then
        echo "File imported successfully!"
    else
        echo "Failed to push changes to destination repository."
        exit 1
    fi
else
    echo "Failed to checkout file from source repository."
    exit 1
fi

# Cleanup by removing the added remote
git remote remove source_repo
