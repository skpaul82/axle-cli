# Cloudflare Pages Deployment Guide

## Overview

This guide explains how to deploy ONLY the Axle CLI documentation website to Cloudflare Pages, NOT the full axle-cli tool.

## Quick Start

### Option 1: Direct Git Integration (Recommended)

1. **Connect Repository**
   - Log in to [Cloudflare Dashboard](https://dash.cloudflare.com/)
   - Go to **Workers & Pages** > **Create application** > **Pages** > **Connect to Git**
   - Select your GitHub account and choose the `axle-cli` repository

2. **Configure Build Settings**
   ```
   Project name: axle-cli-website
   Production branch: main
   Framework preset: None
   Build command: (leave empty)
   Build output directory: website
   Root directory: / (leave as default)
   ```

3. **Environment Variables** (Optional)
   ```
   No environment variables needed for static site
   ```

4. **Deploy**
   - Click **Save and Deploy**
   - Cloudflare will automatically deploy on every push to `main` branch

### Option 2: Direct Upload

1. **Build Locally**
   ```bash
   # No build needed - files are ready to deploy
   cd website/
   ```

2. **Create ZIP**
   ```bash
   zip -r website.zip .
   ```

3. **Upload to Cloudflare**
   - Go to Cloudflare Dashboard > Workers & Pages > Create application
   - Select **Upload Assets**
   - Upload your `website.zip`
   - Name your project: `axle-cli-website`

## Configuration Files

### `.pages.toml` (Root Directory)
This file tells Cloudflare Pages to deploy ONLY the website folder:

```toml
[build]
command = ""
publish = "website"
```

### `website/_headers`
Custom headers for security and caching.

### `website/_redirects`
URL redirects for clean navigation.

## What Gets Deployed

✅ **Deployed:**
- `website/index.html`
- `website/css/style.css`
- `website/js/main.js`
- `website/pages/*.html`
- All static assets

❌ **NOT Deployed:**
- Python source code
- Axle CLI tool files
- Documentation markdown files
- GitHub Actions workflows
- Any files outside `website/` directory

## Custom Domain Setup

1. **Add Custom Domain**
   - Go to your Pages project > Custom domains
   - Add: `www.axle.sanjoypaul.com`

2. **Update DNS**
   - Add CNAME record in your DNS:
   ```
   Type: CNAME
   Name: www
   Target: [your-cloudflare-pages-domain].pages.dev
   ```

3. **Verify**
   - Cloudflare will automatically provision SSL certificates
   - Wait for DNS propagation (usually < 24 hours)

## Previews and Branches

### Preview Deployments
Cloudflare automatically creates preview URLs for:
- Pull requests
- Commits to branches other than `main`

Example: `https://7b2c477.axle-cli-website.pages.dev`

### Production Deployment
- Main branch: `https://axle-cli-website.pages.dev`
- Custom domain: `https://www.axle.sanjoypaul.com`

## Automatic Deployments

Every push to `main` branch automatically triggers:
1. Cloudflare detects changes in `website/` directory
2. Copies files to CDN (no build process needed)
3. Deploys to production
4. Invalidates cache as needed

## Manual Deployment

If you need to trigger a manual deployment:

1. Via Cloudflare Dashboard:
   - Go to your Pages project
   - Click **Create deployment**
   - Select branch and commit

2. Via Wrangler CLI:
   ```bash
   npm install -g wrangler
   wrangler pages deploy website --project-name=axle-cli-website
   ```

## Performance Optimization

The website is already optimized:
- ✅ Minimal file sizes (no build dependencies)
- ✅ Efficient CSS with CSS Grid/Flexbox
- ✅ Optimized images (use WebP format when possible)
- ✅ CDN caching via Cloudflare
- ✅ Automatic minification (optional)

## Troubleshooting

### Issue: Wrong files deployed
**Solution:** Check `.pages.toml` has `publish = "website"`

### Issue: 404 errors
**Solution:** Verify `_redirects` file includes root redirect

### Issue: Styling not loading
**Solution:** Check file paths are relative (e.g., `css/style.css`)

### Issue: Copy buttons not working
**Solution:** Ensure JavaScript is enabled and no CSP blocks

## Monitoring

### Analytics
- Go to Cloudflare Dashboard > Analytics > Pages
- View: Page views, bandwidth, requests

### Logs
- Go to your Pages project > Logs
- View: Build logs, deployment history, real-time logs

## Rollback

If something goes wrong:
1. Go to your Pages project > Deployments
2. Find the last good deployment
3. Click **Rollback** > Confirm

## Cost

- **Free Tier**: 500 builds/month, unlimited bandwidth
- **Paid**: Starts at20/month for more builds

The Axle CLI website easily fits within the free tier.

## Support

- Cloudflare Pages Docs: https://developers.cloudflare.com/pages
- Community: https://community.cloudflare.com
- Axle CLI Issues: https://github.com/skpaul82/axle-cli/issues
