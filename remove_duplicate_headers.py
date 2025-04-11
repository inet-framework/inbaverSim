#!/usr/bin/env python3
"""
Script to remove comment headers from .cc files if they are the same as 
the comment headers in the corresponding .h files.
"""

import os
import re
import glob

def normalize_comment_header(comment_header):
    """Normalize a comment header by removing trailing whitespace and empty comment lines."""
    # Split the comment header into lines
    lines = comment_header.split('\n')
    
    # Remove trailing whitespace from each line
    lines = [line.rstrip() for line in lines]
    
    # Remove empty comment lines (lines with just '//')
    lines = [line for line in lines if line != '//']
    
    # Join the lines back together
    return '\n'.join(lines)

def extract_comment_header(content):
    """Extract the comment header from a file's content."""
    # Find the license header first
    license_pattern = r'//\s*\n// Copyright \(C\) \d+ .+\n//\s*\n// SPDX-License-Identifier: GPL-3.0-or-later\n//\s*\n'
    license_match = re.search(license_pattern, content)
    
    if not license_match:
        print("No license header found")
        return ""
    
    # Get the content after the license header
    content_after_license = content[license_match.end():]
    
    # Match a block of comments at the beginning of the content after the license header
    comment_pattern = r'^(//[^\n]*\n)+'
    comment_match = re.match(comment_pattern, content_after_license)
    
    if comment_match:
        return comment_match.group(0)
    
    print("No comment header found after license header")
    return ""

def process_file_pair(cc_path):
    """Process a .cc file and its corresponding .h file."""
    # Derive the .h file path from the .cc file path
    h_path = cc_path[:-3] + '.h'
    
    # Check if the .h file exists
    if not os.path.exists(h_path):
        print(f"Skipping {cc_path} (no corresponding .h file)")
        return False
    
    # Read the content of both files
    with open(cc_path, 'r') as f:
        cc_content = f.read()
    
    with open(h_path, 'r') as f:
        h_content = f.read()
    
    # Extract the comment headers
    cc_comment_header = extract_comment_header(cc_content)
    h_comment_header = extract_comment_header(h_content)
    
    # Normalize the comment headers for comparison
    normalized_cc_header = normalize_comment_header(cc_comment_header) if cc_comment_header else ""
    normalized_h_header = normalize_comment_header(h_comment_header) if h_comment_header else ""
    
    # Debug output
    print(f"Comparing headers for {cc_path} and {h_path}")
    print(f"CC header: {normalized_cc_header}")
    print(f"H header: {normalized_h_header}")
    
    # If the normalized comment headers are the same and not empty, remove the comment header from the .cc file
    if normalized_cc_header and normalized_cc_header == normalized_h_header:
        # Find the license header
        license_pattern = r'//\s*\n// Copyright \(C\) \d+ .+\n//\s*\n// SPDX-License-Identifier: GPL-3.0-or-later\n//\s*\n'
        license_match = re.search(license_pattern, cc_content)
        
        if not license_match:
            print(f"No license header found in {cc_path}")
            return False
        
        # Get the content before, during, and after the license header
        license_header = license_match.group(0)
        content_before_license = cc_content[:license_match.start()]
        content_after_license = cc_content[license_match.end():]
        
        # Remove the comment header from the content after the license header
        new_content_after_license = re.sub(r'^' + re.escape(cc_comment_header), '', content_after_license, 1)
        
        # Combine the parts back together
        new_cc_content = content_before_license + license_header + new_content_after_license
        
        # Write the modified content back to the .cc file
        with open(cc_path, 'w') as f:
            f.write(new_cc_content)
        
        print(f"Removed duplicate comment header from {cc_path}")
        return True
    
    print(f"Skipping {cc_path} (comment headers are different or empty)")
    return False

def main():
    """Find and process all .cc files in the project."""
    
    # Find all .cc files in the project
    cc_files = glob.glob('src/**/*.cc', recursive=True)
    
    # Process each file pair
    modified_count = 0
    for cc_path in cc_files:
        if process_file_pair(cc_path):
            modified_count += 1
    
    print(f"\nDone! Removed duplicate comment headers from {modified_count} files.")

if __name__ == "__main__":
    main()
