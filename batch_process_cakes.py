#!/usr/bin/env python3
"""
Batch Cake Image Processing with Google Nano Banana Pro (Gemini 3 Pro Image)

This script processes 103 cake images to create a unified professional gallery format.
All images will be transformed to:
- Perfect square (2048x2048px)
- White background
- Centered cake, 90% of frame
- Consistent lighting and super-realistic quality
"""

import os
import time
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()  # Load API key from .env file

API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file!")

INPUT_FOLDER = "images/cakes"              # Original cake images
OUTPUT_FOLDER = "images/cakes-processed"   # Processed output
BACKUP_FOLDER = "images/cakes-original-backup"  # Safety backup
MODEL_ID = "gemini-3-pro-image-preview"    # Nano Banana Pro model

# Your Exact Prompt from NANO_BANANA_PRO_PROMPT.txt
PROMPT_TEXT = """
Transform this cake image into a professional product photograph with these exact specifications:

COMPOSITION:
- Perfect square format (1:1 aspect ratio, 2048x2048 pixels)
- Pure white background (#FFFFFF)
- Cake centered precisely in the frame
- Cake occupies 90% of the image area
- Professional product photography perspective

LIGHTING & COLOR:
- Soft, even studio lighting
- Consistent color temperature (neutral white, 5500K)
- No harsh shadows
- Natural highlights that enhance cake details
- Color-accurate representation

CRITICAL REQUIREMENTS:
- DO NOT add any decorative elements not present in the original cake
- DO NOT remove any existing cake decorations or features
- DO NOT modify the cake's design, colors, or structure
- PRESERVE all original cake details exactly as they appear
- Maintain super-realistic, photographic quality
- NO artistic filters or stylization

STYLE: Professional product photography, super realistic, magazine-quality
"""

# --- SETUP ---
print("🍰 Orly's Cake Gallery - AI Batch Processor")
print("=" * 60)
print(f"Model: {MODEL_ID}")
print(f"Input: {INPUT_FOLDER}")
print(f"Output: {OUTPUT_FOLDER}")
print("=" * 60)

client = genai.Client(api_key=API_KEY)

# Create output directories
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(BACKUP_FOLDER, exist_ok=True)

# --- BATCH PROCESSING ---
image_files = sorted([
    f for f in os.listdir(INPUT_FOLDER)
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
])
total = len(image_files)

print(f"\n🍌 Found {total} cake images to process")

# Progress tracking
processed = 0
errors = 0
skipped = 0

# Create a log file
log_file = "processing_log.txt"
with open(log_file, 'w') as log:
    log.write(f"Orly's Cake Gallery - Processing Log\n")
    log.write(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    log.write(f"Total images: {total}\n")
    log.write("=" * 60 + "\n\n")

for index, filename in enumerate(image_files, 1):
    input_path = os.path.join(INPUT_FOLDER, filename)
    output_filename = Path(filename).stem + "_processed.png"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    # Skip if already processed
    if os.path.exists(output_path):
        print(f"[{index}/{total}] ⏭️  Skipping {filename} (already processed)")
        skipped += 1
        continue

    print(f"[{index}/{total}] 🔄 Processing {filename}...", end=" ", flush=True)

    try:
        # Load image
        img = Image.open(input_path)

        # Optional: Pre-crop to square to help the AI
        # (The AI will handle it, but square inputs help)
        width, height = img.size
        if width != height:
            # Center crop to square
            min_dim = min(width, height)
            left = (width - min_dim) // 2
            top = (height - min_dim) // 2
            right = left + min_dim
            bottom = top + min_dim
            img = img.crop((left, top, right, bottom))

        # Convert image to bytes for API
        import io
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()

        # Send to Gemini 3 Pro Image (Nano Banana Pro)
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=PROMPT_TEXT),
                        types.Part.from_bytes(data=img_bytes, mime_type="image/png")
                    ]
                )
            ],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                safety_settings=[
                    types.SafetySetting(
                        category="HARM_CATEGORY_DANGEROUS_CONTENT",
                        threshold="BLOCK_ONLY_HIGH"
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_HARASSMENT",
                        threshold="BLOCK_ONLY_HIGH"
                    )
                ]
            )
        )

        # Extract and Save Image
        saved = False
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_data = part.inline_data.data
                    with open(output_path, 'wb') as f:
                        f.write(image_data)
                    print("✅ Done!")
                    processed += 1
                    saved = True

                    # Log success
                    with open(log_file, 'a') as log:
                        log.write(f"✅ [{index}/{total}] {filename} -> {output_filename}\n")
                    break

        if not saved:
            print("❌ No image returned")
            errors += 1
            with open(log_file, 'a') as log:
                log.write(f"❌ [{index}/{total}] {filename} - No image returned\n")

        # Sleep to respect rate limits
        # Adjust based on your API tier (2-5 seconds recommended)
        time.sleep(3)

    except Exception as e:
        print(f"❌ Error: {str(e)[:50]}...")
        errors += 1
        with open(log_file, 'a') as log:
            log.write(f"❌ [{index}/{total}] {filename} - Error: {str(e)}\n")

        # Sleep longer on error to avoid rate limit issues
        time.sleep(5)

# --- SUMMARY ---
print("\n" + "=" * 60)
print("🎉 Batch Processing Complete!")
print("=" * 60)
print(f"Total images: {total}")
print(f"✅ Processed: {processed}")
print(f"⏭️  Skipped (already done): {skipped}")
print(f"❌ Errors: {errors}")
print(f"\nProcessed images saved to: {OUTPUT_FOLDER}")
print(f"Log file: {log_file}")

# Final log entry
with open(log_file, 'a') as log:
    log.write("\n" + "=" * 60 + "\n")
    log.write(f"Completed: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    log.write(f"Processed: {processed}/{total}\n")
    log.write(f"Skipped: {skipped}\n")
    log.write(f"Errors: {errors}\n")

print("\n💡 Next steps:")
print("1. Review processed images in images/cakes-processed/")
print("2. Check processing_log.txt for details")
print("3. Re-run script to retry any failed images")
print("4. When satisfied, integrate into website gallery")
