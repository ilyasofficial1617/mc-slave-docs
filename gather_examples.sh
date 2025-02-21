#!/bin/bash

# Read each line from the github_repo_references.txt file
while IFS= read -r repo_url; do
    # Extract the repository name from the URL
    repo_name=$(basename "$repo_url" .git)
    
    # Clone the repository into its own directory within examples
    git clone "$repo_url" "examples/$repo_name"
done < examples/github_repo_references.txt
