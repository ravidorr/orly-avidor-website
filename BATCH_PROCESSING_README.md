# Batch Cake Image Processing with Google Nano Banana Pro

This directory contains everything needed to batch process 103 cake images using Google's Gemini 3 Pro Image model (also known as "Nano Banana Pro").

## Quick Start

### 1. Prerequisites Installed ✅
- Python 3.9+ ✅
- Required packages installed ✅
  - `google-genai`
  - `Pillow`
  - `python-dotenv`

### 2. API Key Configured ✅
- API key stored securely in `.env` file ✅
- `.env` is excluded from git (never committed) ✅

### 3. Run the Batch Processor

```bash
cd ~/personal-dev/orly-avidor-website
python3 batch_process_cakes.py
```

## What the Script Does

The `batch_process_cakes.py` script will:

1. **Load all 103 images** from `images/cakes/`
2. **Process each image** through Google Nano Banana Pro AI with your exact specifications
3. **Save processed images** to `images/cakes-processed/`
4. **Create a log file** (`processing_log.txt`) tracking all operations
5. **Handle errors gracefully** and skip already-processed images
6. **Respect API rate limits** with automatic delays between requests

## Expected Output Format

Each processed image will be:
- ✅ **Square format:** 2048x2048 pixels (1:1 aspect ratio)
- ✅ **White background:** Pure white (#FFFFFF)
- ✅ **Centered cake:** Precisely centered in frame
- ✅ **90% cake size:** Cake occupies 90% of image area
- ✅ **Consistent lighting:** Soft, even studio lighting at 5500K
- ✅ **Super realistic:** Professional product photography quality
- ✅ **Preserved details:** Original cake design completely intact

## Processing Time & Cost

**Estimated Processing Time:**
- ~5 minutes per image (including API processing + rate limit delays)
- Total: **8-10 hours** for all 103 images

**Estimated Cost:**
- Google Gemini 3 Pro Image: ~$0.04 - $0.13 per image
- Total estimated cost: **$5 - $15 USD** for 103 images

**Note:** You can run the script and leave it running overnight. It will save progress and can be resumed if interrupted.

## Monitoring Progress

### Real-time Console Output
The script shows live progress:
```
🍰 Orly's Cake Gallery - AI Batch Processor
============================================================
[1/103] 🔄 Processing cake001.jpg... ✅ Done!
[2/103] 🔄 Processing cake002.jpg... ✅ Done!
[3/103] ⏭️  Skipping cake003.jpg (already processed)
```

### Check the Log File
```bash
tail -f processing_log.txt
```

### View Processed Images
```bash
open images/cakes-processed/
```

## Troubleshooting

### Rate Limit Errors
If you hit rate limits:
1. The script automatically sleeps 3 seconds between requests
2. On errors, it waits 5 seconds before continuing
3. If you hit daily limits, stop the script and resume tomorrow
4. Already-processed images are skipped automatically

### API Key Issues
If you see authentication errors:
```bash
# Verify .env file exists and has the key
cat .env

# Should show:
# GOOGLE_API_KEY=AIzaSy...
```

### Out of Memory
If processing fails due to memory:
- The script pre-crops large images to squares
- Reduce image size before processing if needed

### Check Script Status
```bash
# Count processed images
ls images/cakes-processed/ | wc -l

# Count original images
ls images/cakes/ | wc -l

# Progress: X/103 complete
```

## Resuming Interrupted Processing

The script is designed to be resumable:
- Already-processed images are **automatically skipped**
- Just re-run the script: `python3 batch_process_cakes.py`
- It will continue from where it left off

## Quality Control

After processing completes:

### 1. Visual Review
```bash
# Open processed images folder
open images/cakes-processed/

# Look for:
# ✓ Consistent white backgrounds
# ✓ Centered cakes
# ✓ Similar sizing across all images
# ✓ No added/removed decorations
```

### 2. Side-by-Side Comparison
Compare originals vs processed:
- Original: `images/cakes/cake001.jpg`
- Processed: `images/cakes-processed/cake001_processed.png`

### 3. Check Log for Errors
```bash
grep "❌" processing_log.txt
```

### 4. Reprocess Failed Images
If any images failed:
1. Note the filenames from the log
2. Manually delete the failed output files (if any)
3. Re-run the script - it will retry only failed/missing images

## File Structure

```
orly-avidor-website/
├── .env                          # API key (SECRET - not in git)
├── batch_process_cakes.py        # Main processing script
├── requirements.txt              # Python dependencies
├── BATCH_PROCESSING_README.md    # This file
├── processing_log.txt            # Auto-generated processing log
├── images/
│   ├── cakes/                    # 103 original images
│   ├── cakes-processed/          # 103 AI-processed images (output)
│   └── cakes-original-backup/    # Backup copies (optional)
```

## After Processing is Complete

### 1. Review All Images
```bash
# Count successful outputs
ls images/cakes-processed/*.png | wc -l
# Should show 103
```

### 2. Backup Originals
```bash
cp -r images/cakes/* images/cakes-original-backup/
```

### 3. Integrate into Website
- Update `index.html` to create image gallery
- Use images from `images/cakes-processed/`
- See main `AI_IMAGE_PROCESSING_GUIDE.md` for gallery HTML/CSS

### 4. Deploy to Server
```bash
git add images/cakes-processed/
git commit -m "Add AI-processed cake gallery images"
git push origin main
ssh avidor "~/deploy-website.sh"
```

## Security Notes

### API Key Protection
✅ **Your API key is safe:**
- Stored in `.env` file
- `.env` is in `.gitignore`
- Will **NEVER** be committed to git
- Only exists locally on your machine

### Best Practices
- 🔒 Never share `.env` file
- 🔒 Never commit API keys to git
- 🔒 Regenerate key if accidentally exposed
- 🔒 Use environment variables for production

## Cost Management

### Monitor Your Usage
- Check [Google Cloud Console](https://console.cloud.google.com) for API usage
- Set up billing alerts to avoid surprises
- Free tier may have daily limits (~50 images/day)

### Batch Processing Tips
- **Process in smaller batches** (e.g., 20 images at a time)
- **Check costs** after first batch before continuing
- **Review quality** before processing all 103 images

## Support & Documentation

- **This Project:** See `AI_IMAGE_PROCESSING_GUIDE.md`
- **Google Nano Banana Pro:** https://blog.google/technology/ai/nano-banana-pro/
- **Gemini API Docs:** https://ai.google.dev/docs
- **Processing Issues:** Check `processing_log.txt`

## Summary

You're all set to process 103 cake images! Simply run:

```bash
python3 batch_process_cakes.py
```

The script will handle everything automatically:
- ✅ Load images
- ✅ Apply AI transformation
- ✅ Save results
- ✅ Log progress
- ✅ Handle errors
- ✅ Resume if interrupted

**Estimated time:** 8-10 hours (can run overnight)
**Estimated cost:** $5-15 USD

Happy processing! 🍰✨
