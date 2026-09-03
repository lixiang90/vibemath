param(
    [string]$MagmaPath = "",
    [string]$TranscriptDirectory = "."
)

$ErrorActionPreference = "Stop"
$ExpectedCertificateHash = "74843e4e53c7d09793fa857a2ce57d37a21be855ce135fec9f22b5b00aab5e08"
$ExpectedMagmaScriptHash = "ae6a61f417f82e29d6e496229399a05ce88a0f085d5e6f29869e9c03acdf00e8"
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Certificate = Join-Path $Here "STUDENT_ELLIPTIC_ROUND_03_certificate.json"
$MagmaScript = Join-Path $Here "STUDENT_ELLIPTIC_ROUND_03_magma_same_m_and_descent_H.m"

if (-not (Test-Path -LiteralPath $Certificate)) {
    throw "Missing local certificate: $Certificate"
}
if (-not (Test-Path -LiteralPath $MagmaScript)) {
    throw "Missing Magma script: $MagmaScript"
}

$ActualHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $Certificate).Hash.ToLowerInvariant()
if ($ActualHash -ne $ExpectedCertificateHash) {
    throw "Certificate hash mismatch. Expected $ExpectedCertificateHash but got $ActualHash"
}
$ActualMagmaScriptHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $MagmaScript).Hash.ToLowerInvariant()
if ($ActualMagmaScriptHash -ne $ExpectedMagmaScriptHash) {
    throw "Magma script hash mismatch. Expected $ExpectedMagmaScriptHash but got $ActualMagmaScriptHash"
}

if ([string]::IsNullOrWhiteSpace($MagmaPath)) {
    $MagmaCommand = Get-Command magma -ErrorAction Stop
    $MagmaPath = $MagmaCommand.Source
}
if (-not (Test-Path -LiteralPath $MagmaPath)) {
    throw "Magma executable not found at: $MagmaPath"
}

$ResolvedTranscriptDirectory = [System.IO.Path]::GetFullPath($TranscriptDirectory)
[System.IO.Directory]::CreateDirectory($ResolvedTranscriptDirectory) | Out-Null
$Stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$Transcript = Join-Path $ResolvedTranscriptDirectory "STUDENT_ELLIPTIC_ROUND_03_magma_transcript_$Stamp.txt"

"AUDIT_WRAPPER_BEGIN" | Tee-Object -FilePath $Transcript
"CERTIFICATE_SHA256 $ActualHash" | Tee-Object -FilePath $Transcript -Append
"MAGMA_SCRIPT_SHA256 $ActualMagmaScriptHash" | Tee-Object -FilePath $Transcript -Append
"MAGMA_EXECUTABLE $MagmaPath" | Tee-Object -FilePath $Transcript -Append

$VersionOutput = & $MagmaPath --version 2>&1
$VersionExit = $LASTEXITCODE
$VersionOutput | Tee-Object -FilePath $Transcript -Append
if ($VersionExit -ne 0) {
    throw "Magma version probe failed with exit code $VersionExit. Transcript: $Transcript"
}

"MAGMA_SCRIPT $MagmaScript" | Tee-Object -FilePath $Transcript -Append
"MAGMA_INVOCATION -b -n <script>" | Tee-Object -FilePath $Transcript -Append
& $MagmaPath -b -n $MagmaScript 2>&1 | Tee-Object -FilePath $Transcript -Append
$MagmaExit = $LASTEXITCODE
"MAGMA_EXIT_CODE $MagmaExit" | Tee-Object -FilePath $Transcript -Append
if ($MagmaExit -ne 0) {
    throw "Magma failed with exit code $MagmaExit. Transcript retained at: $Transcript"
}

$FailurePattern = '(?i)\bwarning\b|runtime error|internal error|user error|syntax error|\bGRH\b|conditional|not proven|terminated|abort|exception'
$FailureLines = Select-String -LiteralPath $Transcript -Pattern $FailurePattern
if ($FailureLines) {
    $FailureLines | ForEach-Object { $_.Line } | Write-Error
    throw "Audit stopped because the transcript contains a warning, error, or conditionality marker. Transcript retained at: $Transcript"
}

$TranscriptText = Get-Content -Raw -LiteralPath $Transcript
foreach ($Marker in @(
    "SAME_M_FIBRE_PRODUCT_LOCAL_CERTIFICATES_OK",
    "FAKE_TWO_SELMER_DESCENT_COMPLETED",
    "FAKE_TWO_SELMER_CARDINALITY",
    "AUDIT_COMPLETED"
)) {
    if (-not $TranscriptText.Contains($Marker)) {
        throw "Missing required completion marker '$Marker'. Transcript retained at: $Transcript"
    }
}

"AUDIT_WRAPPER_COMPLETED" | Tee-Object -FilePath $Transcript -Append
Write-Output "Clean audited transcript: $Transcript"
