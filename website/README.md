# Axle CLI Website

Official documentation website for Axle CLI.

## 🚀 Deployment

### Cloudflare Pages (Recommended)

1. **Connect Repository**
   - Log in to Cloudflare Dashboard
   - Go to Pages > Create a project
   - Connect to your GitHub repository

2. **Configure Build Settings**
   - **Build command:** Leave empty (static site)
   - **Build output directory:** `website`
   - **Root directory:** `/` (repository root)

3. **Environment Variables**
   - No variables needed for static site

4. **Deploy**
   - Click "Save and Deploy"
   - Cloudflare will automatically deploy on push to main branch

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
├── pages/
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
- Modify FAQ items in `pages/faq.html`

### Analytics

Add your analytics code to `js/main.js` in the `trackEvent` function.

## 📧 Newsletter

The newsletter uses Zoho Campaigns. To configure:

1. Get your Zoho Campaigns embed code
2. Replace the form in `index.html` and `pages/community.html`
3. Update the form action URL

## 🔗 Links

- Main Repository: https://github.com/skpaul82/axle-cli
- Documentation: https://www.axle.sanjoypaul.com
- Author: https://www.sanjoypaul.com

## 📄 License

MIT License - Same as main Axle CLI project.
