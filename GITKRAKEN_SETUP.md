# GitKraken Setup Guide

GitKraken is a powerful Git GUI client that makes working with this monorepo easier.

## Installation

1. **Download GitKraken**
   - Visit: https://www.gitkraken.com/download
   - Download the Windows version
   - Install the application

2. **Sign Up/Login**
   - Create a free account or use existing account
   - Free accounts support unlimited public repos

## Connecting to This Repository

### Option 1: Clone Repository

1. Open GitKraken
2. Click **File > Clone Repo**
3. Select **GitHub.com**
4. Authenticate with GitHub
5. Find repository: `Mouy-leng/Workspace-Monorepo`
6. Choose local path: `F:\Workspace\Workspace-Monorepo`
7. Click **Clone the repo!**

### Option 2: Open Existing Repository

1. Open GitKraken
2. Click **File > Open Repo**
3. Navigate to: `F:\Workspace\Workspace-Monorepo`
4. Click **Open**

## GitKraken Features for This Monorepo

### Visualizing Branch Structure

GitKraken's graph view shows:
- Main branch (production)
- Develop branch (development)
- Feature branches
- Commit history

### Working with Branches

1. **Create Branch**
   - Right-click on `develop` branch
   - Select **Create branch here**
   - Name: `feature/your-feature-name`

2. **Switch Branches**
   - Double-click any branch to checkout

3. **Merge Branches**
   - Drag branch onto target branch
   - Resolve conflicts if any

### Committing Changes

1. **Stage Files**
   - Check files in the left panel
   - Files move to "Staged Files"

2. **Write Commit Message**
   - Follow conventional commits:
     - `feat:` - New feature
     - `fix:` - Bug fix
     - `docs:` - Documentation
     - `chore:` - Maintenance

3. **Commit**
   - Click **Commit changes to X files**

### Pushing to GitHub

1. Click **Push** button (top toolbar)
2. Select remote: `origin`
3. Select branch to push
4. Click **Submit**

### Pull Requests

1. After pushing, click **Create Pull Request**
2. Fill out PR template
3. Submit for review

## Repository Structure in GitKraken

The monorepo structure is visible in the file tree:
```
Workspace-Monorepo/
├── DomainController/
├── MQL5-Google-Onedrive/
├── OS-Twin/
├── OS-Twin-setup/
├── AgentBrain/
├── .github/
├── scripts/
└── [Documentation files]
```

## Tips for Monorepo Workflow

### Filtering by Directory

1. Use GitKraken's file filter
2. Focus on specific project directory
3. See only relevant changes

### Working with Multiple Projects

1. Create feature branches per project
2. Use branch naming: `feature/project-name/feature-description`
3. Example: `feature/mql5/add-sync-feature`

### Viewing Project History

1. Use GitKraken's graph view
2. Filter commits by author
3. Search commits by message

## Authentication Setup

### GitHub Authentication

1. **File > Preferences > Authentication**
2. Add GitHub account
3. Use Personal Access Token or OAuth

### Personal Access Token

If using token:
1. GitHub Settings > Developer settings > Personal access tokens
2. Generate new token with `repo` scope
3. Add to GitKraken authentication

## Keyboard Shortcuts

- `Ctrl + Shift + N` - New repository
- `Ctrl + O` - Open repository
- `Ctrl + K` - Commit
- `Ctrl + Shift + P` - Push
- `Ctrl + Shift + U` - Pull
- `Ctrl + F` - Search commits

## Troubleshooting

### Repository Not Showing

- Check if `.git` folder exists
- Verify repository path is correct
- Try refreshing GitKraken

### Authentication Issues

- Re-authenticate with GitHub
- Check token permissions
- Verify network connection

### Merge Conflicts

- GitKraken highlights conflicts
- Use built-in merge tool
- Resolve conflicts before committing

## Best Practices

1. **Always Pull Before Push**
   - Click Pull button first
   - Resolve any conflicts
   - Then push your changes

2. **Use Meaningful Commit Messages**
   - Follow conventional commits
   - Reference issue numbers if applicable

3. **Create Feature Branches**
   - Don't commit directly to `main`
   - Use `develop` or feature branches

4. **Review Before Committing**
   - Check staged files
   - Review diffs
   - Ensure no sensitive data

## Resources

- [GitKraken Documentation](https://support.gitkraken.com/)
- [GitKraken Tutorials](https://www.gitkraken.com/learn/git)
- [GitHub Integration Guide](https://support.gitkraken.com/integrations/github/)

## Quick Start Checklist

- [ ] Install GitKraken
- [ ] Open this repository
- [ ] Authenticate with GitHub
- [ ] Create a feature branch
- [ ] Make changes
- [ ] Commit changes
- [ ] Push to GitHub
- [ ] Create Pull Request

---

**Note**: GitKraken is optional. You can continue using command line Git or any other Git client. This guide is for those who prefer a visual interface.
