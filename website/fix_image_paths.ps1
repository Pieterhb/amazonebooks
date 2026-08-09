# Replace all remote img URLs in main.js with local /images/covers/ paths

$content = Get-Content "main.js" -Raw

function Get-LocalPath($url) {
    $parts = $url -split "/"
    $filename = $parts[-1]
    if ($parts.Count -ge 3) {
        $prefix = $parts[-3]
        $filename = $prefix + "_" + $filename
    }
    $localFile = "public\images\covers\" + $filename
    if (-not (Test-Path $localFile)) {
        Write-Host ("Missing: " + $filename + " -- using fallback")
        $filename = "www.softcoverbooks.co.za_Swart%20Luiperd%20Logo.jpg"
    }
    return "/images/covers/" + $filename
}

# Find all external img URLs
$pattern = 'https://(app\.sqrindle\.com|www\.softcoverbooks\.co\.za)/[^\s'"'"'"]+\.jpg'
$matchList = [regex]::Matches($content, $pattern)

$replacements = @{}
foreach ($m in $matchList) {
    $url = $m.Value
    if (-not $replacements.ContainsKey($url)) {
        $local = Get-LocalPath $url
        $replacements[$url] = $local
        Write-Host ($url + " -> " + $local)
    }
}

foreach ($url in $replacements.Keys) {
    $content = $content.Replace($url, $replacements[$url])
}

Set-Content "main.js" $content -NoNewline -Encoding UTF8
Write-Host ("`nDone. Replaced " + $replacements.Count + " unique URLs.")
