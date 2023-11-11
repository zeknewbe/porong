#!/bin/bash

# Variables
SOURCE_FILE_URL="https://raw.githubusercontent.com/jsosao/m3u/main/mylist.m3u8"
DEST_REPO="git@github.com:zeknewbe/porong.git"
DEST_PATH="mylist.m3u8"     # Path where you want the file to be in the destination repo

# Clone destination repo
if git clone "$DEST_REPO"; then
    cd "$(basename "$DEST_REPO" .git)" || exit
else
    echo "Failed to clone destination repository."
    exit 1
fi

# Download the file using curl
if ! curl -o "$DEST_PATH" "$SOURCE_FILE_URL"; then
    echo "Failed to download the file."
    exit 1
fi

# Commit and push the changes
git add "$DEST_PATH"
git commit -m "Imported $DEST_PATH from $SOURCE_FILE_URL"
if git push origin main; then
    echo "File imported successfully!"
else
    echo "Failed to push changes to destination repository."
    exit 1
fi
