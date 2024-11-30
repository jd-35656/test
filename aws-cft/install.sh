#!/bin/bash

# Step 1: Get the current Git repository URL from the remote
REPO_DIR=$(pwd)

# Step 2: Clone the current repository into the new directory
# We assume that the script is being run from the repository's root directory
# and we want to clone the same repository into a new folder.
git clone "$REPO_DIR" "${REPO_DIR}_clone"

# Step 3: Navigate to the newly cloned directory
cd "${REPO_DIR}_clone" || exit

# Step 4: Initialize the Git repository (if needed)
git init

# Step 5: Make the first commit if files are already present in the folder
git add .
git commit -m "Initial commit with all files"

echo "New project initialized successfully in ${REPO_DIR}_clone."
