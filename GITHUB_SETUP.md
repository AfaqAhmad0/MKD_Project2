# Push this project to GitHub

Your code is cloned from Gitea and ready to push to your GitHub.

## Option A: GitHub CLI (recommended)

If you have [GitHub CLI](https://cli.github.com/) installed and logged in (`gh auth login`):

```powershell
cd "C:\Users\Mine\Pictures\MKD_DS\Project 2"
gh repo create ds_task_scp --private --source=. --remote=github --push
```

- Use `--public` instead of `--private` if you want a public repo.
- This creates a new repo `ds_task_scp` under your GitHub user, adds it as remote `github`, and pushes.

To keep the existing Gitea repo as `origin` and add GitHub as a second remote:

```powershell
gh repo create ds_task_scp --private --source=. --remote=github --push
# Your remotes will be: origin (Gitea), github (GitHub)
```

## Option B: Create repo on GitHub manually, then push

1. On GitHub: **New repository** → name it (e.g. `ds_task_scp`) → **Create repository** (do not add README or .gitignore).

2. Add GitHub as a remote and push:

```powershell
cd "C:\Users\Mine\Pictures\MKD_DS\Project 2"
git remote add github https://github.com/YOUR_USERNAME/ds_task_scp.git
git push -u github main
```

Replace `YOUR_USERNAME` with your GitHub username. If you want GitHub to be the main remote and keep Gitea as backup:

```powershell
git remote rename origin gitea
git remote add origin https://github.com/YOUR_USERNAME/ds_task_scp.git
git push -u origin main
```

## Commit and push the new app code

The new `app/`, `requirements.txt`, and `.env.example` need to be committed before pushing:

```powershell
cd "C:\Users\Mine\Pictures\MKD_DS\Project 2"
git add app/ requirements.txt .env.example .gitignore
git commit -m "Add FastAPI app skeleton and project setup"
git push origin main
# or: git push github main  (if you added github remote)
```
