## Problem
The `hackparv/jarvis/` and `hackparv/self-operating-computer/` folders were nested git repositories (each had their own `.git` folder) but were not properly configured as submodules. This caused them to appear as empty folders on GitHub.

## Solution
- Removed nested `.git` folders from both directories
- Removed directory entries from Git index (they were tracked as submodules)
- Added all files from both directories to the main repository (51 files, 8965+ lines)
- Created `.gitignore` to exclude `node_modules/`, `venv/`, and other common files

## Changes
- ✅ `hackparv/jarvis/` - Now contains all files and is accessible on GitHub
- ✅ `hackparv/self-operating-computer/` - Now contains all files and is accessible on GitHub
- ✅ Added `.gitignore` for better repository hygiene

## Testing
- Verified all files are properly tracked
- Confirmed `node_modules` and `venv` are excluded via `.gitignore`

After merging, both folders will be fully accessible on GitHub with all their content visible.

