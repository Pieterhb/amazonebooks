import { defineConfig } from 'vite';
import { resolve } from 'path';
import fs from 'fs';

// Helper to recursively find all HTML files in website
function getHtmlEntries(dir = __dirname, baseDir = __dirname) {
  let entries = {};
  const files = fs.readdirSync(dir);
  for (const file of files) {
    if (file === 'node_modules' || file === 'dist' || file === '.wrangler' || file === '.git') continue;
    const fullPath = resolve(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      Object.assign(entries, getHtmlEntries(fullPath, baseDir));
    } else if (file.endsWith('.html')) {
      const rel = fullPath.replace(baseDir, '').replace(/^[\\/]/, '').replace(/[\\/]/g, '_').replace('.html', '');
      entries[rel || 'index'] = fullPath;
    }
  }
  return entries;
}

export default defineConfig({
  root: '.',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    rollupOptions: {
      input: getHtmlEntries(__dirname, __dirname),
    },
  },
  server: {
    port: 3000,
  }
});
