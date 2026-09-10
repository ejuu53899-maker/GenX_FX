# Contributing Guide

Welcome to the Workspace Monorepo! This guide will help you contribute to the project.

## Repository Structure

This is a monorepo containing multiple projects:

- **DomainController/** - Domain controller scripts and configurations
- **MQL5-Google-Onedrive/** - MQL5 Google OneDrive integration
- **OS-Twin/** - OS-Twin project
- **OS-Twin-setup/** - OS-Twin setup scripts
- **AgentBrain/** - AgentBrain project

## Getting Started

### Prerequisites

- Git
- PowerShell 5.1+ (for Windows scripts)
- Python 3.11+ (if working on Python projects)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Mouy-leng/Workspace-Monorepo.git
   cd Workspace-Monorepo
   ```

2. Configure git user (if not already set):
   ```bash
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   ```

## Development Workflow

### Branch Strategy

- **main** - Production-ready code
- **develop** - Development branch
- **feature/** - Feature branches
- **fix/** - Bug fix branches

### Making Changes

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes in the appropriate subdirectory

3. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

4. Push to GitHub:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Create a Pull Request on GitHub

### Commit Messages

Follow conventional commit format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks

Example:
```
feat(DomainController): Add new backup script
fix(MQL5): Resolve sync issue
docs: Update README with setup instructions
```

## Project-Specific Guidelines

### DomainController

- PowerShell scripts should follow best practices
- Include error handling in all scripts
- Document script parameters and usage

### MQL5-Google-Onedrive

- Follow MQL5 coding standards
- Include proper error handling
- Document configuration requirements

### OS-Twin

- Follow project-specific guidelines
- Maintain compatibility with existing setup

## Code Review Process

1. All changes require a Pull Request
2. At least one approval required before merging
3. CI checks must pass
4. Code should be tested before submission

## Questions?

If you have questions, please:
1. Check existing documentation
2. Review open issues
3. Create a new issue for discussion

Thank you for contributing! 🎉
