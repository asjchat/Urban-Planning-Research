# push_to_github.ps1
# Helper script to initialize, commit, create repo via gh (if available) and push.
# Run this in PowerShell from the repository root.

param(
    [string]$RepoName = "Urban-Planning-Population-Projection-Research",
    [string]$Description = "Urban planning population projection research",
    [switch]$Private
)

function Write-Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Write-Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Write-Err($m){ Write-Host "[ERROR] $m" -ForegroundColor Red }

# Check prerequisites
$git = Get-Command git -ErrorAction SilentlyContinue
$gh = Get-Command gh -ErrorAction SilentlyContinue

if (-not $git) {
    Write-Err "Git is not installed or not on PATH. Install Git for Windows: https://git-scm.com/download/win"
    exit 1
}

# Initialize and commit if no .git
if (-not (Test-Path -Path .git -PathType Container)) {
    Write-Info "Initializing git repository and making initial commit..."
    git init | Out-Null
    git add .
    git commit -m "Initial commit" | Out-Null
} else {
    Write-Info ".git directory already present. Skipping init."
}

# Ensure branch name main
try {
    git branch -M main 2>$null
} catch {
    # ignore
}

if ($gh) {
    Write-Info "GitHub CLI detected. Attempting to create repo and push using 'gh'..."
    $vis = if ($Private) { "--private" } else { "--public" }
    # create with --source and push; pass -y to skip prompts
    gh repo create "$RepoName" $vis --description "$Description" --source . --remote origin --push --confirm
    if ($LASTEXITCODE -eq 0) {
        Write-Info "Repository created and pushed. Use 'gh repo view --web' to open in browser."
    } else {
        Write-Warn "'gh' command failed. Check your authentication (run 'gh auth login') or create the repo manually on github.com."
    }
} else {
    Write-Warn "GitHub CLI ('gh') not found. Please create a repository on github.com or install 'gh' (https://cli.github.com/)."
    Write-Host "
Manual push steps (replace YOUR_GITHUB_USERNAME):
    git remote add origin https://github.com/YOUR_GITHUB_USERNAME/$RepoName.git
    git push -u origin main
"
}
