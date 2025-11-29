# Orly's Website Setup Documentation

Complete setup guide for orly.avidor.org static website.

## Server Information

- **Domain:** orly.avidor.org
- **Server:** avidor.org droplet
- **IP Address:** 134.199.242.83 (Reserved IP)
- **Location:** NYC3 - DigitalOcean
- **OS:** Ubuntu 24.04 LTS
- **Web Server:** Nginx 1.24.0
- **SSL:** Let's Encrypt (auto-renewal enabled)

## Website Access

- **URL:** https://orly.avidor.org
- **SSL Certificate Expires:** 2026-02-27 (auto-renews)
- **Website Directory:** `/var/www/orly.avidor.org`

## SSH Access

### Configuration
SSH config is in `~/.ssh/config`:

```bash
# Connect as ravidor user
ssh avidor

# Connect as root
ssh avidor-root
```

### Users
- **ravidor:** Regular user with sudo access (no password required)
- **root:** Root user

## DNS Configuration (DigitalOcean)

Domain `avidor.org` with the following records:

| Type | Hostname | Value | TTL |
|------|----------|-------|-----|
| A | @ | 134.199.242.83 | 3600 |
| A | orly | 134.199.242.83 | 3600 |
| A | www | 134.199.242.83 | 3600 |

**Name Servers:**
- ns1.digitalocean.com
- ns2.digitalocean.com
- ns3.digitalocean.com

## Website File Structure

```
/var/www/orly.avidor.org/
├── index.html          # Main homepage
├── css/                # CSS stylesheets (optional)
├── js/                 # JavaScript files (optional)
├── images/             # Image assets (optional)
└── ...                 # Additional static files
```

## Nginx Configuration

**Config File:** `/etc/nginx/sites-available/orly.avidor.org`

```nginx
server {
    server_name orly.avidor.org;

    root /var/www/orly.avidor.org;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logs
    access_log /var/log/nginx/orly.avidor.org.access.log;
    error_log /var/log/nginx/orly.avidor.org.error.log;

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/orly.avidor.org/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/orly.avidor.org/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    if ($host = orly.avidor.org) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80;
    listen [::]:80;
    server_name orly.avidor.org;
    return 404; # managed by Certbot
}
```

## Common Tasks

### Upload New Content

#### Via SCP (from local machine)
```bash
# Upload a single file
scp /path/to/file.html avidor:/var/www/orly.avidor.org/

# Upload entire directory
scp -r /path/to/directory/* avidor:/var/www/orly.avidor.org/
```

#### Via SSH (edit directly on server)
```bash
ssh avidor
cd /var/www/orly.avidor.org
nano index.html
# Edit and save
```

### View Website Logs

```bash
# Access logs
ssh avidor "sudo tail -f /var/log/nginx/orly.avidor.org.access.log"

# Error logs
ssh avidor "sudo tail -f /var/log/nginx/orly.avidor.org.error.log"
```

### Restart Nginx

```bash
# Test configuration
ssh avidor "sudo nginx -t"

# Reload nginx (no downtime)
ssh avidor "sudo systemctl reload nginx"

# Restart nginx (brief downtime)
ssh avidor "sudo systemctl restart nginx"
```

### Renew SSL Certificate (Manual)

Certificates auto-renew, but to manually renew:

```bash
ssh avidor "sudo certbot renew"
```

### Check SSL Certificate Expiry

```bash
ssh avidor "sudo certbot certificates"
```

## Firewall Configuration

Ensure ports are open:

```bash
# Check firewall status
ssh avidor "sudo ufw status"

# Allow HTTP and HTTPS (if not already allowed)
ssh avidor "sudo ufw allow 80/tcp && sudo ufw allow 443/tcp"
```

## GitHub Repository

**Repository:** https://github.com/ravidorr/orly-avidor-website

The website is version-controlled using Git and hosted on GitHub for easy collaboration and deployment.

## Website Deployment Workflow

### Option 1: Git Workflow (Recommended)

This is the preferred method for making changes to the website.

#### Clone the repository locally
```bash
git clone git@github.com:ravidorr/orly-avidor-website.git
cd orly-avidor-website
```

#### Make changes locally
```bash
# Edit files
nano index.html

# Test by opening in browser
open index.html
```

#### Commit and push changes
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

#### Deploy to server
```bash
ssh avidor "cd /var/www/orly.avidor.org && git pull origin main"
```

### Option 2: Direct Editing on Server
```bash
ssh avidor
cd /var/www/orly.avidor.org
nano index.html
# Edit content
git add .
git commit -m "Update via server"
git push origin main
```

### Option 3: Local Development + SCP Upload
```bash
# Develop locally
# Test in browser
# Upload to server
scp -r ./website/* avidor:/var/www/orly.avidor.org/

# Then commit changes on server
ssh avidor "cd /var/www/orly.avidor.org && git add . && git commit -m 'Update via SCP' && git push"
```

## Current Website Content

The site currently has a basic "Under Construction" page with:
- Responsive design
- Modern gradient background
- Mobile-friendly layout
- Clean typography

Location: `/var/www/orly.avidor.org/index.html`

## Backup Recommendations

### Manual Backup
```bash
# From local machine
scp -r avidor:/var/www/orly.avidor.org ./backups/orly-website-$(date +%Y%m%d)
```

### Automated Backup (to be set up)
Consider setting up:
- Daily backups to DigitalOcean Spaces
- Weekly snapshots of the entire droplet
- Version control with Git

## Troubleshooting

### Website not loading
1. Check DNS propagation: `dig orly.avidor.org`
2. Check nginx status: `ssh avidor "sudo systemctl status nginx"`
3. Check error logs: `ssh avidor "sudo tail -20 /var/log/nginx/orly.avidor.org.error.log"`

### SSL certificate issues
1. Check certificate validity: `ssh avidor "sudo certbot certificates"`
2. Test renewal: `ssh avidor "sudo certbot renew --dry-run"`
3. Check nginx SSL config: `ssh avidor "sudo nginx -t"`

### Permission issues
```bash
# Fix ownership
ssh avidor "sudo chown -R ravidor:ravidor /var/www/orly.avidor.org"

# Fix permissions
ssh avidor "sudo chmod -R 755 /var/www/orly.avidor.org"
```

## Security Best Practices

1. **Keep system updated**
   ```bash
   ssh avidor "sudo apt update && sudo apt upgrade -y"
   ```

2. **Monitor logs regularly**
   - Check access logs for unusual traffic
   - Review error logs for issues

3. **SSL certificates**
   - Auto-renewal is configured via certbot timer
   - Certificates renew automatically 30 days before expiry

4. **Firewall**
   - Only necessary ports are open (22, 80, 443)
   - SSH key authentication only (no password login)

## Next Steps

To customize the website:
1. Edit `/var/www/orly.avidor.org/index.html`
2. Add CSS in a separate file or `<style>` tag
3. Add images to `/var/www/orly.avidor.org/images/`
4. Consider using a static site generator (Hugo, Jekyll, etc.)

## Additional Resources

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [DigitalOcean Community Tutorials](https://www.digitalocean.com/community/tutorials)

## Setup History

- **2025-11-29:** Initial setup completed
  - Domain configured in DigitalOcean
  - DNS records created (avidor.org, orly.avidor.org, www.avidor.org)
  - Nginx installed and configured
  - SSL certificate obtained (expires 2026-02-27)
  - Basic website deployed
  - GitHub repository created: https://github.com/ravidorr/orly-avidor-website
  - Git initialized on server with deploy key
  - Initial commit pushed to GitHub
