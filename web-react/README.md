# DailyToolsOps React website

React 18, Vite and React Router. Original static sources remain in ../website.
Run from this directory with Node 22+ and Python 3.9+:

```sh
npm install
npm run dev
npm run build
npm test
npm run preview
```

Preview at http://127.0.0.1:4173/DailyToolsOps/. Production output is dist/.
GitHub Actions builds and deploys the production artifact to the existing Pages site. GitHub Pages source must be GitHub Actions. No server rewrite is needed because every public route has a physical index.html. The 404.html page provides recovery links.

SEO metadata lives in src/components/SEO.jsx, canonical origin and base in src/data/site.js, sitemap and robots generation in scripts/prerender.mjs. Add packs to the repository catalog and maintain their INSTRUCTIONS.md; scripts/prepare.py uses the existing validated build pipeline to generate guide content and downloads. Add new standalone React pages to App.jsx and the pre-render route list. The favicon is a local SVG; social.png is a generated placeholder branded with the project name, replace it with an approved social image when available.

The legacy website and its tests remain intact for comparison and rollback. The React browser audit runs against the actual project base path. Documentation uses the existing escaped Markdown renderer to preserve exact formatting and heading anchors.
