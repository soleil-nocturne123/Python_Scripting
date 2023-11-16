#!/usr/bin/python3

# AUTHOR: PHAN HOAI HUONG NGUYEN (SYLVIA NGUYEN)
# PURPOSE: SCRIPT TO REPORT DISK SPACE USED BY EACH DIRECTORY AND EXPORT TO A CSV FILE

# PACKAGE
import sys # Interact with the interpreter
import os # Interact with the operating system
import pandas as pd # Helpful for data manipulation

# SUPPORT FUNCTION - GET DISK SPACE USED BY A DIRECTORY
def disk_used(dir, level): # Level determines the detailed of report, default -1 -- Report all files; 0 -- Report current directory as a whole; 1 -- Report by each directory in the current directory; etc. 
    used_space = 0
    curr_lv = -1 # Only used in directory case

    # Detailed of Report
    if(level == -1):
        global File
        global Usage
    else:
        global Directory
        global Usage

    # Get Disk Space Usage
    for entry in os.scandir(dir): # Scan every directory
        try:
            if(entry.is_dir(follow_symlinks=False)): # Don't follow symlinks and check directories\
                # Add to Report
                curr_lv += 1
                if(level != -1):
                    if(curr_lv == level):
                        Directory.append(entry.path)
                        used_space += disk_used(entry.path, level) # Get disk space used for this directory
                        Usage.append(used_space)
                        used_space = 0
                        curr_lv = -1
                    else:
                        used_space += disk_used(entry.path, level) # Get disk space used for this directory
                else:
                    used_space += disk_used(entry.path, level) # Get disk space used for this directory  
            else:
                used_space += entry.stat(follow_symlinks=False).st_size # Disk space used by this file
                # Add to Report
                if(level == -1):
                    File.append(entry.path)
                    Usage.append(entry.stat(follow_symlinks=False).st_size)
        except Exception as e:
            print("Exception: ", e)
    return(used_space)

# MAIN PROGRAM
if __name__ == "__main__": # This script runs as a standalone program -- cannot be executed from another script
    path = sys.argv[1] if len(sys.argv) >= 2 else "/home" # Default path is \home
    level = int(sys.argv[2]) if len(sys.argv) >= 3 else -1 # Default is report all files

    # Prepare for report
    if(level == -1):
        File = []
        Usage = []
    else:
        Directory = []
        Usage = []

    # Get disk space used
    disk_used(path, level)

    # Create report
    usage_dict = {"File" : File, "Usage" : Usage} if (level == -1) else {"Directory" : Directory, "Usage" : Usage}
    df = pd.DataFrame(usage_dict)
    df.to_csv("Disk_Usage.csv")
