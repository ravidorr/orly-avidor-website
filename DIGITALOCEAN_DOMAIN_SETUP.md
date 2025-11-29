# DigitalOcean Domain Setup Guide

This guide explains how to add and manage domains in DigitalOcean, following the same pattern as `murphys-laws.com`.

## Overview

- **Existing Domain:** murphys-laws.com (already configured)
- **New Domain:** avidor.org (to be added)
- **DNS Management:** DigitalOcean Cloud Console

## Steps to Add avidor.org to DigitalOcean

### 1. Add Domain in DigitalOcean Control Panel

1. Log in to [DigitalOcean Cloud Console](https://cloud.digitalocean.com/)
2. Click **Create** in the top right corner
3. Select **Domains/DNS**
4. Click **Add a domain**
5. Enter your domain name: `avidor.org`
6. Click **Add Domain**

### 2. Configure Name Servers at Your Domain Registrar

Before the domain will work, you need to update the name servers at your domain registrar (where you purchased `avidor.org`) to point to DigitalOcean's name servers:

```
ns1.digitalocean.com
ns2.digitalocean.com
ns3.digitalocean.com
```

**Steps:**
1. Log in to your domain registrar (e.g., GoDaddy, Namecheap, Google Domains, etc.)
2. Find the DNS or Name Server settings for `avidor.org`
3. Replace the existing name servers with DigitalOcean's name servers listed above
4. Save the changes

**Note:** DNS propagation can take 24-48 hours, but usually completes within a few hours.

### 3. Add DNS Records

Once the domain is added, you'll need to create DNS records. Common records include:

#### A Record (Points domain to an IP address)
- **Type:** A
- **Hostname:** `@` (for avidor.org) or subdomain name (e.g., `www`)
- **Value:** Your droplet's IP address (e.g., `45.55.74.28` if using murphys-n8n)
- **TTL:** 3600 (default)

#### CNAME Record (Subdomain alias)
- **Type:** CNAME
- **Hostname:** Subdomain (e.g., `www`)
- **Value:** `@` or `avidor.org`
- **TTL:** 3600

#### MX Record (Email routing, if needed)
- **Type:** MX
- **Hostname:** `@`
- **Mail Server:** Your mail server
- **Priority:** 10
- **TTL:** 3600

#### TXT Record (Domain verification, SPF, etc.)
- **Type:** TXT
- **Hostname:** `@` or subdomain
- **Value:** Your verification string or SPF record
- **TTL:** 3600

### 4. Example Configuration (Similar to murphys-laws.com)

If you want to host a service on `avidor.org` similar to how `n8n.murphys-laws.com` is configured:

**DNS Records:**
```
Type    Hostname    Value               TTL
A       @           45.55.74.28         3600
A       subdomain   45.55.74.28         3600
CNAME   www         @                   3600
```

**Nginx Configuration (on server):**
```nginx
server {
    server_name subdomain.avidor.org;
    listen 443 ssl http2;
    listen 80;

    # SSL certificates will be managed by Certbot
    # Your application configuration here
}
```

### 5. SSL Certificate Setup (Optional but Recommended)

If you're hosting a website/service, secure it with SSL using Let's Encrypt:

```bash
ssh murphys-n8n  # or your target server
sudo certbot --nginx -d avidor.org -d www.avidor.org
```

## Verification

### Check DNS Propagation

```bash
# Check A record
dig avidor.org

# Check name servers
dig NS avidor.org

# Check from multiple locations
nslookup avidor.org
```

### Verify in DigitalOcean

1. Go to **Networking** → **Domains** in the DigitalOcean console
2. Click on `avidor.org`
3. Verify all DNS records are correct

## Common Use Cases

### 1. Simple Website
- Add A record pointing `@` to your droplet IP
- Add CNAME record for `www` pointing to `@`

### 2. Subdomain for Service (like n8n)
- Add A record for subdomain (e.g., `app.avidor.org`) pointing to droplet IP
- Configure nginx on the server
- Set up SSL with Certbot

### 3. Email Setup
- Add MX records for your email provider
- Add SPF, DKIM, and DMARC TXT records as required

## Current Domain Configuration

### murphys-laws.com
- **Droplet IP:** 45.55.74.28
- **Active Subdomains:**
  - n8n.murphys-laws.com (n8n instance with SSL)
- **Server:** murphys-n8n

## Troubleshooting

### Domain not resolving
- Check name servers are correctly set at registrar
- Wait for DNS propagation (up to 48 hours)
- Verify DNS records in DigitalOcean console

### SSL certificate issues
- Ensure DNS is properly propagated first
- Check nginx configuration
- Verify ports 80 and 443 are open

### Subdomain not working
- Verify A or CNAME record exists for subdomain
- Check nginx server_name configuration
- Clear browser cache

## Additional Resources

- [DigitalOcean: How to Add Domains](https://docs.digitalocean.com/products/networking/dns/how-to/add-domains/)
- [DigitalOcean: DNS Records Management](https://docs.digitalocean.com/products/networking/dns/how-to/manage-records/)
- [DNS Quickstart Guide](https://docs.digitalocean.com/products/networking/dns/getting-started/quickstart/)
- [Point to DigitalOcean Name Servers](https://docs.digitalocean.com/products/networking/dns/getting-started/dns-registrars/)

## Notes

- DigitalOcean is **not** a domain registrar - you need to purchase domains elsewhere
- DNS management in DigitalOcean is free
- Changes to DNS records typically propagate within minutes
- Always backup existing DNS records before making changes
