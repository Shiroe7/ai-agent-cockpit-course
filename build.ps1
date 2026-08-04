$ErrorActionPreference = "Stop"

$xelatexCommand = Get-Command xelatex.exe -ErrorAction SilentlyContinue
if ($xelatexCommand) {
    $xelatexPath = $xelatexCommand.Source
} else {
    $fallback = "D:\texlive\2026\bin\windows\xelatex.exe"
    if (Test-Path -LiteralPath $fallback) {
        $xelatexPath = $fallback
    } else {
        throw "XeLaTeX was not found. Install TeX Live and add xelatex.exe to PATH."
    }
}

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$targets = @(
    @{ Folder = "slides"; File = "lesson10.tex" },
    @{ Folder = "slides"; File = "lesson11.tex" },
    @{ Folder = "slides"; File = "lesson12.tex" },
    @{ Folder = "docs"; File = "experiment_guide.tex" },
    @{ Folder = "docs"; File = "experiment_report_template.tex" },
    @{ Folder = "docs"; File = "capstone_design_template.tex" },
    @{ Folder = "docs"; File = "work_summary_acceptance.tex" }
)

foreach ($target in $targets) {
    $folder = Join-Path $root $target.Folder
    Push-Location $folder
    try {
        Write-Host "Building $($target.Folder)/$($target.File)"
        for ($pass = 1; $pass -le 2; $pass++) {
            & $xelatexPath -interaction=nonstopmode -halt-on-error $target.File
            if ($LASTEXITCODE -ne 0) {
                throw "Build failed: $($target.File), pass $pass."
            }
        }
    } finally {
        Pop-Location
    }
}

Write-Host "All TeX sources and PDFs are up to date."
