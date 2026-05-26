import os
import re
from collections import defaultdict

def find_bugsinpy_duplicates():
    # This targets the 'projects' folder natively inside your BugsInPy-n directory
    projects_dir = "projects"
    
    if not os.path.exists(projects_dir):
        print(f"Error: Could not find '{projects_dir}'. Make sure your terminal is in the BugsInPy-n root.")
        return

    # Regex to grab the filepath from the standard diff format
    file_regex = re.compile(r"\+\+\+ b/(.*?)\n")
    
    file_clusters = defaultdict(list)
    print(f"Scanning BugsInPy '{projects_dir}' directory for overlapping patches...")
    
    # Walk through the BugsInPy file tree
    for project_name in os.listdir(projects_dir):
        project_path = os.path.join(projects_dir, project_name)
        if not os.path.isdir(project_path):
            continue
            
        bugs_dir = os.path.join(project_path, "bugs")
        if not os.path.exists(bugs_dir):
            continue
            
        for bug_id in os.listdir(bugs_dir):
            bug_path = os.path.join(bugs_dir, bug_id)
            if not os.path.isdir(bug_path):
                continue
                
            # BugsInPy stores the gold patch in this specific text file
            patch_file = os.path.join(bug_path, "bug_patch.txt")
            if not os.path.exists(patch_file):
                continue
                
            with open(patch_file, 'r', encoding='utf-8', errors='ignore') as f:
                patch_content = f.read()
                
            # Extract all modified files, remove duplicates, and freeze into a sorted tuple
            modified_files = tuple(sorted(set(file_regex.findall(patch_content))))
            
            if modified_files:
                # Format as project-id (e.g., pandas-12)
                full_bug_name = f"{project_name}-{bug_id}"
                file_clusters[modified_files].append(full_bug_name)

    # Filter for bugs that modified the exact same files
    identical_file_bugs = {files: bugs for files, bugs in file_clusters.items() if len(bugs) > 1}
    
    print(f"\nFound {len(identical_file_bugs)} clusters of identical file overlap:")
    print("-" * 50)
    for files, bugs in identical_file_bugs.items():
        print(f"Bugs: {bugs}")
        print(f"Shared Files Modified: {files}\n")

if __name__ == "__main__":
    find_bugsinpy_duplicates()