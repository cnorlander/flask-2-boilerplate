#!/bin/bash
echo "===================================================================================================================================================="
echo "WARNING: This script can break your project if you have modified the project after cloning it from the repository."
echo "Please be sure to backup the contents of your project directory or backup to external version control. If you have at all modified the boilerplate"
echo "===================================================================================================================================================="



# Get the word to be replaced from a variable
to_replace="boilerplate"
to_replace="${to_replace// /_}"
# Get the replacement boilerplate from user input
read -p "Enter the new project name (lowercase): " new_word

# Find all files with the whitelisted extensions and replace the specified word
while IFS= read -r -d '' file; do
    echo "Working on file: $file"
    sed -i "s/$to_replace/$new_word/g" "$file"
    sed -i "s/${to_replace^}/${new_word^}/g" "$file"
    sed -i "s/${to_replace^^}/${new_word^^}/g" "$file"
done < <(find ../ -type f \( -name '*.html' -o -name '*.css' -o -name '*.js' -o -name '*.py' -o -name '*.yml' -o -name '*.sh' \) ! -name 'rename_project.sh' ! -path '*/.*/*' ! -path '*/venv/*' -print0)

# Find directories with the same name as the specified word and rename them
while IFS= read -r -d '' dir; do
    echo "Renaming directory: $dir"
    parent_dir="$(dirname "$dir")"
    new_dir="${parent_dir}/${new_word}"
    mv "$dir" "$new_dir"
done < <(find ../ -type d -regextype posix-extended -regex ".*/${to_replace}$" ! -path "*/.*/*" ! -path '*/venv/*' -print0)

