<#
.SYNOPSIS
    Dev Skill: Test → Stage → Commit (TranslatorApp Python Project)

.DESCRIPTION
    Tự động hóa quy trình: chạy unit test → git add → git commit
    Dùng trong project Python-Learning/03_TranslateApp
    
.PARAMETER Files
    Danh sách file cần stage (cách nhau bằng dấu phẩy).
    Ví dụ: "src/core/segmenter.py,tests/test_segmenter.py"
    Nếu bỏ trống, sẽ dùng -a (stage tất cả file đã tracked có thay đổi).

.PARAMETER Message
    Commit message theo Conventional Commits format.
    Ví dụ: "feat(core): implement text segmenter"

.PARAMETER SkipTests
    Nếu bật, bỏ qua bước chạy unit test (dùng khi chỉ commit doc/config).

.EXAMPLE
    # Stage file cụ thể + chạy test + commit
    .\dev-commit.ps1 -Files "src/core/segmenter.py,tests/test_segmenter.py" -Message "feat(core): implement text segmenter"

.EXAMPLE
    # Stage tất cả thay đổi + chạy test + commit
    .\dev-commit.ps1 -Message "refactor(core): apply TL review feedback"

.EXAMPLE
    # Chỉ commit doc, bỏ qua test
    .\dev-commit.ps1 -Files "docs/requirements/03-segmentation/opening/P1-SEG-001.md" -Message "docs(requirements): cập nhật task P1-SEG-001" -SkipTests
#>

param(
    [string]$Files = "",
    [Parameter(Mandatory = $true)]
    [string]$Message,
    [switch]$SkipTests
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host " DEV SKILL: Test → Stage → Commit" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

Set-Location $ProjectRoot

# ─── STEP 1: Run Unit Tests ───────────────────────────────────────────────────
if (-not $SkipTests) {
    Write-Host "[1/3] Running unit tests..." -ForegroundColor Yellow
    
    $pythonExe = Join-Path $ProjectRoot "venv\Scripts\python.exe"
    
    if (-not (Test-Path $pythonExe)) {
        Write-Host "      ⚠️  venv not found at $pythonExe" -ForegroundColor Red
        Write-Host "      Trying system python instead..." -ForegroundColor Yellow
        $pythonExe = "python"
    }
    
    & $pythonExe -m unittest discover -s tests -p "test_*.py" 2>&1 | Tee-Object -Variable testOutput
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "❌ Tests FAILED. Aborting commit." -ForegroundColor Red
        exit 1
    }
    
    Write-Host "      ✅ All tests passed." -ForegroundColor Green
} else {
    Write-Host "[1/3] Skipping tests (-SkipTests flag set)." -ForegroundColor DarkGray
}

Write-Host ""

# ─── STEP 2: Git Stage ────────────────────────────────────────────────────────
Write-Host "[2/3] Staging files..." -ForegroundColor Yellow

if ($Files -ne "") {
    # Stage specific files
    $fileList = $Files -split "," | ForEach-Object { $_.Trim() }
    foreach ($file in $fileList) {
        Write-Host "      git add $file"
        git add $file
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Failed to stage: $file" -ForegroundColor Red
            exit 1
        }
    }
    Write-Host "      ✅ Staged $($fileList.Count) file(s)." -ForegroundColor Green
} else {
    # Stage all tracked changes
    Write-Host "      git add -u (all tracked changes)"
    git add -u
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ git add failed." -ForegroundColor Red
        exit 1
    }
    Write-Host "      ✅ Staged all tracked changes." -ForegroundColor Green
}

Write-Host ""

# ─── STEP 3: Git Commit ───────────────────────────────────────────────────────
Write-Host "[3/3] Committing..." -ForegroundColor Yellow
Write-Host "      Message: $Message"

git commit -m $Message

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Commit failed." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host " ✅ DONE! Commit successful." -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
