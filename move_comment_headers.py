#!/usr/bin/env python3
"""
Script to move comment headers in .ned files to be positioned between
the package declaration and the module declaration.
"""

import os
import re
import glob

# Files that are already correctly formatted
ALREADY_DONE = ['src/AccessRouter.ned', 'src/CCNInternet.ned']

def process_file(file_path):
    """Process a single .ned file to move the comment header."""
    
    # Skip files that are already done
    if file_path in ALREADY_DONE:
        print(f"Skipping {file_path} (already done)")
        return False
    
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if the file starts with a comment header
    # This regex matches a block of comments at the start of the file
    comment_header_pattern = r'^(//[^\n]*\n)+\s*'
    package_pattern = r'package\s+[^;]+;'
    
    # If the file doesn't start with comments or doesn't have a package declaration,
    # it might not need modification or have a different structure
    if not re.match(comment_header_pattern, content) or not re.search(package_pattern, content):
        print(f"Skipping {file_path} (doesn't match expected pattern)")
        return False
    
    # Extract the comment header
    comment_match = re.match(comment_header_pattern, content)
    comment_header = comment_match.group(0) if comment_match else ""
    
    # Remove the comment header from the content
    remaining_content = content[len(comment_header):].lstrip()
    
    # Extract the package declaration
    package_match = re.match(package_pattern, remaining_content)
    if not package_match:
        print(f"Skipping {file_path} (couldn't find package declaration)")
        return False
    
    package_decl = package_match.group(0)
    
    # Remove the package declaration from the remaining content
    remaining_content = remaining_content[len(package_decl):].lstrip()
    
    # Create the new content with the package declaration first,
    # followed by the comment header, then the rest of the content
    # Ensure comment header ends with exactly one newline and remaining content has no leading whitespace
    comment_header = comment_header.rstrip() + "\n"
    remaining_content = remaining_content.lstrip()
    new_content = f"{package_decl}\n\n{comment_header}{remaining_content}"
    
    # Write the new content back to the file
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print(f"Modified {file_path}")
    return True

def main():
    """Find and process all .ned files in the project."""
    
    # Find all .ned files in the project
    ned_files = glob.glob('src/**/*.ned', recursive=True) + glob.glob('simulations/**/*.ned', recursive=True)
    
    # Process each file
    modified_count = 0
    for file_path in ned_files:
        if process_file(file_path):
            modified_count += 1
    
    print(f"\nDone! Modified {modified_count} files.")

if __name__ == "__main__":
    main()
