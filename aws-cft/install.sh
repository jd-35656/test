#!/bin/bash

# Step 1: Check if the user has provided a project name
if [ -z "$1" ]; then
  echo "Error: No project name provided."
  echo "Usage: $0 <Project-Name>"
  exit 1
fi

# Get the project name from the first argument
PROJECT_NAME="$1"

# Step 2: Clone the repository into the new directory (the provided project name)
echo "Cloning repository into '$PROJECT_NAME'..."
REPO_DIR=$(pwd)

git clone "$REPO_DIR" "$PROJECT_NAME"

# Step 3: Navigate into the new directory
cd "$PROJECT_NAME" || exit

# Step 4: Reinitialize Git (optional, if you want a fresh git history)
git init

# Step 5: Make the first commit if files are already present in the folder
git add .
git commit -m "Initial commit with all files"

# Step 6: Print success message
echo "New project initialized successfully in '$PROJECT_NAME'."
