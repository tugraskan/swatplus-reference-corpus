<#
Run Hermes on each user-docs input table, one fresh session per table, and
verify each one with `user-docs-check --committed` before starting the next.
Stops at the first table that is not done, so nothing piles up unchecked.

Usage (PowerShell, from anywhere):
  .\run_hermes_docs_tables.ps1                      # the remaining work list
  .\run_hermes_docs_tables.ps1 -Tables plants.plt   # just one table

Hermes' full report for each table is saved under .swatref\hermes-runs\.
#>
param(
    [string[]]$Tables = @(
        'hyd-sed-lte.cha', 'nutrients.cha', 'pesticide.pes', 'plants.plt',
        'ls_unit.def', 'recall_db.rec'
    ),
    # The skill needs about eight tool calls; a loop is cut off well before it can do damage.
    [int]$MaxTurns = 25
)

$repo = 'C:\Users\taci.ugraskan\source\repos\swatplus-reference-corpus-main\swatplus-reference-corpus-main'
$docs = 'external/SWATPlus-user-documentation'
$hermes = Join-Path $env:LOCALAPPDATA 'hermes\bin\hermes.exe'
$swatref = Join-Path $repo '.venv\Scripts\swatref.exe'
$logs = Join-Path $repo '.swatref\hermes-runs'

Set-Location $repo
New-Item -ItemType Directory -Force $logs | Out-Null
$branch = git -C $docs branch --show-current
if ($branch -ne 'hermes/input-tables-62.0.1') {
    Write-Host "Docs checkout is on '$branch', not hermes/input-tables-62.0.1. Stopping." -ForegroundColor Red
    exit 1
}

foreach ($t in $Tables) {
    # A previous table left unfinished would be mixed into this one's commit.
    $dirty = git -C $docs status --porcelain -- io-docs
    if ($dirty) {
        Write-Host "Uncommitted docs changes before $t; finish or discard them first:" -ForegroundColor Red
        $dirty
        exit 1
    }

    $log = Join-Path $logs "$t.txt"
    Write-Host "`n=== $t : Hermes is working (fresh session) ===" -ForegroundColor Cyan
    & $hermes chat -Q --in $repo --max-turns $MaxTurns -q "/swat-docs-table Fix $t." | Tee-Object -FilePath $log

    Write-Host "`n=== $t : independent check ===" -ForegroundColor Cyan
    & $swatref schema --source release_62_0_1 user-docs-check $t --docs-root $docs --committed
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`nSTOPPED at ${t}: not done. Hermes' report: $log" -ForegroundColor Red
        exit 1
    }
}
Write-Host "`nAll tables done and committed:" -ForegroundColor Green
& $swatref schema --source release_62_0_1 user-docs-check codes.bsn topography.hyd soil_plant.ini `
    weather-sta.cli hru.con hyd-sed-lte.cha nutrients.cha pesticide.pes plants.plt ls_unit.def recall_db.rec `
    --docs-root $docs --committed
