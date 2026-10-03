# distrACT
Students often get distracted by social media notifications or feel overwhelmed when balancing back-to-back workshops and school assignments
# Git & GitHub Workflow for Distract!

This guide explains how every team member should set up the repository, work on their assigned features, and submit code without overwriting someone else's work.

## 1. Prerequisites

Before starting, install:

* [Git](https://git-scm.com/downloads)
* [Python](https://www.python.org/downloads/)
* [Visual Studio Code](https://code.visualstudio.com/) (recommended)

You also need access to the Distract! GitHub repository.

## 2. Clone the Repository

**You only need to clone the repository once on your computer.**

1. Open the Distract! repository on GitHub.
2. Click the green **Code** button.
3. Copy the HTTPS repository URL.
4. Open a terminal and navigate to the folder where you want to save the project.

```bash
git clone <REPOSITORY_URL>
cd distract
```

Replace `<REPOSITORY_URL>` with the actual URL copied from GitHub. Replace `distract` with the actual local folder name if it differs.

Open the project in VS Code:

```bash
code .
```

If the `code` command is unavailable, open VS Code and select **File → Open Folder**.

### Check your Git configuration

Set your name and email if you haven't configured Git before:

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Check the current branch and repository status:

```bash
git branch
git status
git remote -v
```

## 3. Understand the Branching Strategy

* `main`: The stable branch containing the team's approved code.
* Feature branches: Each teammate creates a separate branch for their assigned task.

**Never work directly on `main`.** Create your own branch before editing project files.

Example branch names:

```text
feature/authentication
feature/google-calendar
feature/activity-management
feature/dashboard-ui
bugfix/calendar-overlap
```

Use a short, descriptive name that explains your task.

## 4. Create Your Own Branch

Before starting a new task, update your local `main` branch:

```bash
git switch main
git pull origin main
```

Create and switch to your feature branch:

```bash
git switch -c feature/your-feature-name
```

Example:

```bash
git switch -c feature/dashboard-ui
```

Confirm your current branch:

```bash
git branch
```

The branch marked with `*` is your current branch.

If your feature branch already exists, switch to it instead of creating it again:

```bash
git switch feature/your-feature-name
```

## 5. Get the Latest Code

Before beginning work, update your local copy of `main`:

```bash
git switch main
git pull origin main
```

Then return to your feature branch:

```bash
git switch feature/your-feature-name
```

If your feature branch is behind `main`, and you have committed your current work, you can incorporate the latest approved changes with:

```bash
git fetch origin
git merge origin/main
```

Resolve any merge conflicts, test the application, and commit the merge if Git requires it.

**Important:** If you have uncommitted changes, save or commit them before switching branches or merging updates.

## 6. Make Changes to Your Assigned Files

Open the project in VS Code and work only on your assigned feature.

Before editing, check your branch:

```bash
git branch
git status
```

After editing, review which files changed:

```bash
git status
git diff
```

Review the actual changes before staging them:

```bash
git diff -- path/to/file
```

## 7. Stage and Commit Your Changes

A commit saves a snapshot of your work in your local Git history.

### Step 1: Stage your changes

Stage a specific file:

```bash
git add app.py
```

Stage multiple specific files:

```bash
git add app.py google_calendar.py
```

Stage all changes in the current repository:

```bash
git add .
```

Before using `git add .`, make sure you are not including `.env`, Google credentials, tokens, virtual environments, or other unwanted files.

### Step 2: Commit your changes

```bash
git commit -m "Describe your changes"
```

Examples:

```bash
git commit -m "Add user signup and login"
git commit -m "Create activity management endpoints"
git commit -m "Build dashboard layout"
git commit -m "Integrate Google Calendar events"
```

Commit messages should explain what the commit does.

## 8. Push Your Branch to GitHub

The first time you push a new branch:

```bash
git push -u origin feature/your-feature-name
```

Example:

```bash
git push -u origin feature/dashboard-ui
```

After the upstream is configured, future pushes are simpler:

```bash
git push
```

Pushing uploads your commits to GitHub. **It does not automatically merge your work into `main`.**

## 9. Open a Pull Request (PR)

After pushing your feature branch:

1. Open the Distract! repository on GitHub.
2. Click **Compare & pull request**, if GitHub displays it.
3. Set the base branch to `main`.
4. Set the compare branch to your feature branch.
5. Add a title and description explaining your changes.
6. Mention how you tested your work.
7. Submit the pull request.
8. Ask a teammate to review it.
9. Resolve feedback and push any requested fixes to the same branch.
10. Merge only after review and approval according to the team's rules.

Example pull request description:

```text
Feature: Dashboard UI

Changes:
- Added dashboard layout using Bootstrap.
- Added activity cards.
- Connected the dashboard to the events endpoint.

Testing:
- Verified the page loads locally.
- Checked the layout at different screen sizes.

Notes:
- Requires the backend events endpoint to be available.
```

After your pull request is merged, update your local `main`:

```bash
git switch main
git pull origin main
```

## 10. Complete Daily Git Workflow

Use this routine each time you start and finish a work session.

### When starting work

```bash
git status
git switch main
git pull origin main
git switch feature/your-feature-name
git merge origin/main
```

If you have not fetched the latest remote changes yet, run this before the merge:

```bash
git fetch origin
```

### After making changes

```bash
git status
git diff
git add path/to/your-file
git commit -m "Describe your changes"
git push
```

Replace `path/to/your-file` with the files you actually changed.

If you have multiple changed files, stage each intended file or use `git add .` after reviewing the changes.

## 11. Handle Merge Conflicts

A merge conflict occurs when Git cannot automatically combine changes to the same part of a file.

1. Run:

```bash
git status
```

2. Open the files listed as conflicted in VS Code.
3. Look for conflict markers:

```text
<<<<<<< HEAD
Your current branch's changes
=======
Incoming branch's changes
>>>>>>> origin/main
```

4. Decide which code should remain. You may need to combine both versions.
5. Remove all conflict markers and save the file.
6. Test the application.
7. Stage the resolved files and finish the merge:

```bash
git add path/to/resolved-file
git commit -m "Resolve merge conflict"
```

If Git completes the merge automatically after staging, follow the instructions it gives you. Do not start another merge while the current one is unresolved.

**Important:** Do not blindly select "Accept Current" or "Accept Incoming." Review both changes, especially when merging shared files such as `app.py` or `models.py`.

If you accidentally start a merge and want to abandon it before completing it, use:

```bash
git merge --abort
```

## 12. If Someone Else Adds a New File

After a teammate merges a new file into `main`, retrieve it:

```bash
git switch main
git pull origin main
```

Then incorporate it into your feature branch:

```bash
git switch feature/your-feature-name
git fetch origin
git merge origin/main
```

The file will be available in your branch unless your own changes conflict with it.

## 13. Set Up the Python Environment

From the repository root, create a virtual environment.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project's dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If a local `.env` file is required, copy `.env.example` to `.env` and fill in the required values. Never commit the real `.env` file.

Run the application using the command specified in the project README. For the initial Flask app, this may be:

```bash
python app.py
```

## 14. Useful Git Commands

| Command                     | Purpose                                                  |
| --------------------------- | -------------------------------------------------------- |
| `git status`                | Check changed, staged, and untracked files               |
| `git branch`                | List local branches                                      |
| `git switch main`           | Switch to `main`                                         |
| `git switch -c branch-name` | Create and switch to a branch                            |
| `git fetch origin`          | Download remote branch updates without merging           |
| `git pull origin main`      | Fetch and integrate updates from remote `main`           |
| `git add file.py`           | Stage a specific file                                    |
| `git add .`                 | Stage changes under the current directory                |
| `git diff`                  | Review unstaged changes                                  |
| `git diff --staged`         | Review staged changes                                    |
| `git commit -m "message"`   | Save staged changes locally                              |
| `git push`                  | Upload commits to the current branch                     |
| `git log --oneline`         | View recent commits                                      |
| `git stash`                 | Temporarily save tracked uncommitted changes             |
| `git stash pop`             | Restore stashed changes                                  |
| `git merge origin/main`     | Merge the fetched remote `main` into your current branch |
| `git merge --abort`         | Cancel an in-progress merge                              |

## 15. Team Rules

1. Never commit directly to `main`.
2. Always work on your own feature branch.
3. Pull the latest `main` before starting new work.
4. Commit small, logical changes with descriptive messages.
5. Push your branch regularly so your work is backed up.
6. Open a pull request before merging into `main`.
7. Coordinate changes to shared files, especially `app.py`, `models.py`, and `requirements.txt`.
8. Never commit `.env`, passwords, Google OAuth credentials, or access tokens.
9. Test your changes before opening a pull request.
10. Communicate with teammates when your feature depends on their files or endpoints.

Following this workflow helps everyone work independently while keeping the Distract! project organized and reducing accidental overwrites and merge conflicts.

## Project Structure

```text
distract/
├── app.py
├── auth.py
├── activity.py
├── google_calendar.py
├── overlap.py
├── models.py
├── config.py
├── requirements.txt
├── .env                  # Never commit
├── .gitignore
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   └── add_activity.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── dashboard.js
```
