#!/bin/bash

# Prompt for the project name
read -p "Enter the project name: " project_name

# Step 1: Create a new directory with the project name
mkdir "$project_name"
cd "$project_name" || exit

# Step 2: Clone the current repository (assuming the current repo is the origin)
git clone "$(git config --get remote.origin.url)" .

# Step 3: Reinitialize Git (optional: this will reset the repository settings)
rm -rf .git
git init

# Step 4: Add all files to Git
git add .

# Step 5: Commit the files
git commit -m "Initial commit with all files"

# Step 6: Set the remote URL (optional - if you want to push to the original repo)
# git remote add origin <your-remote-repository-url>

# Step 7: Push changes to the remote repository (optional)
# git push -u origin master

echo "New project $project_name initialized successfully."
