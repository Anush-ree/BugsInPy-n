import os
from collections import defaultdict

def find_bugsinpy_test_duplicates():
    projects_dir = "projects"
    
    if not os.path.exists(projects_dir):
        print(f"Error: Could not find '{projects_dir}'.")
        return

    test_clusters = defaultdict(list)
    print(f"Scanning BugsInPy '{projects_dir}' directory for overlapping failing tests...")
    
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
                
            # Check for run_test.sh first, fallback to test.sh
            test_script_path = os.path.join(bug_path, "run_test.sh")
            if not os.path.exists(test_script_path):
                test_script_path = os.path.join(bug_path, "test.sh")
                if not os.path.exists(test_script_path):
                    continue
                
            with open(test_script_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            tests = []
            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                tokens = line.split()
                test_targets = []
                for token in tokens:
                    if token in ('pytest', 'nosetests', 'python', 'python3', '-m', 'unittest', 'tox', 'run', 'coverage'):
                        continue
                    if token.startswith('-'):
                        continue
                    
                    test_targets.append(token.strip("'\""))
                
                if test_targets:
                    tests.append(" ".join(test_targets))
                else:
                    tests.append(line)
            
            if tests:
                failing_tests = tuple(sorted(set(tests)))
                full_bug_name = f"{project_name}-{bug_id}"
                test_clusters[failing_tests].append(full_bug_name)

    identical_test_bugs = {tests: bugs for tests, bugs in test_clusters.items() if len(bugs) > 1}
    
    print(f"\nFound {len(identical_test_bugs)} clusters of identical bugs based on test overlap:")
    print("-" * 50)
    for tests, bugs in identical_test_bugs.items():
        print(f"Bugs: {bugs}")
        print(f"Shared Failing Tests: {tests}\n")

if __name__ == "__main__":
    find_bugsinpy_test_duplicates()