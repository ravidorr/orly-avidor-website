# Orly Avidor's Personal Website

This is the source code for [orly.avidor.org](https://orly.avidor.org).

## Website Information

- **URL:** https://orly.avidor.org
- **Hosted on:** DigitalOcean (Ubuntu 24.04 LTS)
- **Web Server:** Nginx
- **SSL:** Let's Encrypt

## Local Development

1. Clone this repository
2. Edit HTML/CSS files
3. Test locally by opening index.html in a browser
4. Commit and push changes
5. Deploy to server (see deployment section)

## Deployment

### Manual Deployment

From your local machine:
```bash
scp -r ./* avidor:/var/www/orly.avidor.org/
```

### Git Deployment (Recommended)

On the server:
```bash
ssh avidor
cd /var/www/orly.avidor.org
git pull origin main
```

## File Structure

```
/
├── index.html          # Main homepage
├── css/                # Stylesheets (optional)
├── js/                 # JavaScript (optional)
├── images/             # Images (optional)
└── README.md           # This file
```

## License

Copyright © 2025 Orly Avidor. All rights reserved.
