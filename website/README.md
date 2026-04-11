# Axle CLI Website

Official documentation website for Axle CLI.

## 🚀 Deployment

### Cloudflare Pages (Recommended for Website ONLY)

⚠️ **IMPORTANT**: This configuration deploys ONLY the website documentation, NOT the full axle-cli tool.

1. **Connect Repository**
   - Log in to Cloudflare Dashboard
   - Go to Pages > Create a project > Connect to Git
   - Select your `axle-cli` repository

2. **Configure Build Settings**
   - **Project name:** `axle-cli-website`
   - **Production branch:** `main`
   - **Framework preset:** None
   - **Build command:** Leave empty ⬚ (static site, no build needed)
   - **Build output directory:** `website` ⬅️ IMPORTANT: Only deploys website folder
   - **Root directory:** `/` (repository root)

3. **Deploy**
   - Click "Save and Deploy"
   - Cloudflare will deploy ONLY the `website/` directory

4. **Custom Domain** (Optional)
   - Add custom domain: `www.axle.sanjoypaul.com`
   - Update DNS CNAME record to point to Cloudflare

**What Gets Deployed:**
- ✅ `website/index.html` and all pages
- ✅ `website/css/` and `website/js/` files
- ✅ Static website content only

**What Does NOT Get Deployed:**
- ❌ Python source code
- ❌ Axle CLI tool files
- ❌ Documentation markdown files
- ❌ Any files outside `website/` directory

### Manual Deployment

Simply upload the contents of the `website/` directory to your web server.

## 📁 Structure

```
website/
├── index.html          # Homepage
├── css/
│   └── style.css       # Main stylesheet
├── js/
│   └── main.js         # JavaScript functionality
├── /
│   ├── docs.html       # Documentation
│   ├── faq.html        # FAQ with search
│   └── community.html  # Community page
├── assets/             # Images and other assets
├── _headers            # Cloudflare headers
└── _redirects          # Cloudflare redirects
```

## 🎨 Features

- **Responsive Design:** Works on all devices
- **Fast Loading:** Minimal dependencies, optimized CSS
- **SEO Friendly:** Proper meta tags and semantic HTML
- **Accessible:** ARIA labels and keyboard navigation
- **Interactive FAQ:** Search and category filtering
- **Newsletter:** Zoho Campaigns integration

## 🛠️ Customization

### Colors

Edit CSS variables in `css/style.css`:

```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #64748b;
    /* ... */
}
```

### Content

- Edit HTML files directly
- Update navigation links in all pages
- Modify FAQ items in `/faq.html`

### Analytics

Add your analytics code to `js/main.js` in the `trackEvent` function.

## 📧 Newsletter

The newsletter uses Zoho Campaigns. To configure:

1. Get your Zoho Campaigns embed code
2. Replace the form in `index.html` and `/community.html`
3. Update the form action URL

## 🔗 Links

- Main Repository: https://github.com/skpaul82/axle-cli
- Documentation: https://www.axle.sanjoypaul.com
- Author: https://www.sanjoypaul.com

## 📄 License

MIT License - Same as main Axle CLI project.
