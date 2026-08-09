# Download all book cover images locally
$imageDir = "public\images\covers"
New-Item -ItemType Directory -Force -Path $imageDir | Out-Null

$urls = Get-Content "image_urls.txt" | Where-Object { $_ -match "https://" }

$headers = @{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    "Referer" = "https://panther-ebooks.com/"
    "Accept" = "image/webp,image/apng,image/*,*/*;q=0.8"
}

$count = 0
$failed = 0
foreach ($url in $urls) {
    $url = $url.Trim()
    if (-not $url) { continue }
    
    # Generate filename from URL
    $filename = ($url -split "/")[-1]
    # Prepend a unique prefix from the path to avoid collisions
    $parts = $url -split "/"
    if ($parts.Count -ge 3) {
        $prefix = $parts[-3]  # product ID
        $filename = "${prefix}_${filename}"
    }
    $outPath = Join-Path $imageDir $filename
    
    if (Test-Path $outPath) {
        Write-Host "SKIP (exists): $filename"
        $count++
        continue
    }
    
    try {
        Invoke-WebRequest -Uri $url -OutFile $outPath -Headers $headers -TimeoutSec 30 -ErrorAction Stop
        $size = (Get-Item $outPath).Length
        Write-Host "OK ($size bytes): $filename"
        $count++
    } catch {
        Write-Host "FAIL: $url -> $_"
        $failed++
    }
    Start-Sleep -Milliseconds 100
}

Write-Host "`nDone: $count downloaded, $failed failed"
