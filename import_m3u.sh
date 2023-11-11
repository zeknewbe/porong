#!/bin/bash

# Variables
SOURCE_REPO="jsosao/m3u"
SOURCE_FILE="mylist.m3u8"
SOURCE_BRANCH="main"
DEST_REPO="git@github.com:zeknewbe/porong.git"
DEST_PATH="mylist.m3u8"   # Path where you want the file to be in the destination repo

# Setup Git configuration
GIT_EMAIL="visionintegral@gmail.com"
GIT_NAME="zeknewbe"

# Clone destination repo
echo "Cloning destination repository..."
if git clone "$DEST_REPO" dest-repo; then
    cd dest-repo || exit 1
else
    echo "Failed to clone destination repository."
    exit 1
fi

# Add source repo as a remote and fetch the file
echo "Adding source repository as remote..."
git remote add source_repo "https://github.com/$SOURCE_REPO.git"
git fetch source_repo $SOURCE_BRANCH

# Checkout the specific file from source repo
echo "Checking out file from source repository..."
if git checkout source_repo/$SOURCE_BRANCH -- "$SOURCE_FILE"; then
    if mv "$SOURCE_FILE" "$DEST_PATH"; then
        echo "File moved to destination path."
    else
        echo "Failed to move file to destination path."
        exit 1
    fi
else
    echo "Failed to checkout file from source repository."
    exit 1
fi

# Commit and push the changes
echo "Setting up Git configuration..."
git config user.email "$GIT_EMAIL"
git config user.name "$GIT_NAME"

echo "Committing changes..."
git add "$DEST_PATH"
git commit -m "Imported $SOURCE_FILE from $SOURCE_REPO"

echo "Pushing changes to the repository..."
if git push origin main; then
    echo "File imported successfully!"
else
    echo "Failed to push changes to destination repository."
    exit 1
fi

# Cleanup by removing the added remote
git remote remove source_repo
