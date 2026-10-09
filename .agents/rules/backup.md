# Backup / Deploy Rule for amazonebooks

When the user says **"backup"** for this project, always do **both** steps in order:

## Step 1 — Push to GitHub
```powershell
cd c:\googleamazon
git add -A
git commit -m "<meaningful commit message describing the changes>"
git push origin main
```

## Step 2 — Deploy to Cloudflare Pages (via Wrangler)
```powershell
cd c:\googleamazon\website
npx wrangler pages deploy dist --project-name amazonebooks
```

## Why both steps are needed
- The live site (ebooks.softcoverbooks.co.za) is served from Cloudflare Pages (amazonebooks.pages.dev).
- Cloudflare Pages serves files from the website/dist/ folder.
- website/dist/ is listed in .gitignore, so it is NEVER pushed to GitHub automatically.
- Therefore pushing to GitHub alone does NOT update the live site.
- Wrangler uploads the dist/ folder directly to Cloudflare Pages, which is the only way to update the live site.

## Summary
GitHub push = version control backup only.
Wrangler deploy = live site update.
"Backup" = always do both.
