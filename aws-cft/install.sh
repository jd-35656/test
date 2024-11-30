#!/bin/bash

# Step 1: Prompt for the new project name (or use the current directory as the default)
echo "Enter the new project name (default is the current directory name):"
read -p "Project Name: " PROJECT_NAME

# If no input is provided, default to the current directory name
if [ -z "$PROJECT_NAME" ]; then
  PROJECT_NAME=$(basename "$PWD")
fi

# Step 2: Ask if the user wants to clone the repository (confirmation prompt)
echo "You are about to clone the repository into a new directory called '$PROJECT_NAME'."
read -p "Do you want to proceed? (y/n): " CONFIRMATION

# If the user confirms, proceed, otherwise exit
if [[ "$CONFIRMATION" != "y" && "$CONFIRMATION" != "Y" ]]; then
  echo "Operation canceled."
  exit 1
fi

# Step 3: Get the current Git repository URL from the remote (if you're inside a Git repository)
REPO_DIR=$(pwd)

# Step 4: Clone the repository into the new directory
echo "Cloning repository into '$PROJECT_NAME'..."
git clone "$REPO_DIR" "$PROJECT_NAME"

# Step 5: Navigate into the new directory
cd "$PROJECT_NAME" || exit

# Step 6: Reinitialize Git (optional, if you want a fresh git history)
git init

# Step 7: Make the first commit if files are already present in the folder
git add .
git commit -m "Initial commit with all files"

# Step 8: Print success message
echo "New project initialized successfully in '$PROJECT_NAME'."
