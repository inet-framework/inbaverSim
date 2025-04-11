#!/usr/bin/env python3
"""
Script to add license headers to all .ned, .cc, and .h files in the project.
The script extracts author name, email, and year from existing file comments.
"""

import os
import re
import glob

def process_file(file_path):
    """Process a single file to add a license header."""
    
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if the file already has a license header
    if "SPDX-License-Identifier: GPL-3.0-or-later" in content:
        print(f"Skipping {file_path} (already has license header)")
        return False
    
    # Extract author information
    author_pattern = r'@author\s*:\s*([^(]+)\(([^)]+)\)'
    author_match = re.search(author_pattern, content)
    if not author_match:
        print(f"Skipping {file_path} (couldn't find author information)")
        return False
    
    author_name = author_match.group(1).strip()
    author_email = author_match.group(2).strip()
    
    # Extract date information
    date_pattern = r'@date\s*:\s*(\d+)-\w+-(\d+)'
    date_match = re.search(date_pattern, content)
    if not date_match:
        print(f"Skipping {file_path} (couldn't find date information)")
        return False
    
    year = date_match.group(2)  # Extract the year
    
    # Create the license header
    license_header = f"""//
// Copyright (C) {year} {author_name} ({author_email})
//
// SPDX-License-Identifier: GPL-3.0-or-later
//

"""
    
    # Add the license header to the beginning of the file
    new_content = license_header + content
    
    # Write the new content back to the file
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print(f"Added license header to {file_path}")
    return True

def main():
    """Find and process all .ned, .cc, and .h files in the project."""
    
    # Find all .ned, .cc, and .h files in the project
    ned_files = glob.glob('src/**/*.ned', recursive=True) + glob.glob('simulations/**/*.ned', recursive=True)
    cc_files = glob.glob('src/**/*.cc', recursive=True)
    h_files = glob.glob('src/**/*.h', recursive=True)
    
    all_files = ned_files + cc_files + h_files
    
    # Process each file
    modified_count = 0
    for file_path in all_files:
        if process_file(file_path):
            modified_count += 1
    
    print(f"\nDone! Added license headers to {modified_count} files.")

if __name__ == "__main__":
    main()
