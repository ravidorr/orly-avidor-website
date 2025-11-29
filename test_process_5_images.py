#!/usr/bin/env python3
"""
TEST SCRIPT: Process only 5 cake images to verify quality before full batch

This script processes just the first 5 images to:
1. Test API connectivity
2. Verify output quality
3. Check cost per image
4. Confirm the AI prompt works as expected
"""

import os
import time
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file!")

INPUT_FOLDER = "images/cakes"
OUTPUT_FOLDER = "images/cakes-test-output"  # Separate folder for test
MODEL_ID = "gemini-3-pro-image-preview"

# Your Exact Prompt
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
print("🧪 TEST MODE: Processing 5 images only")
print("=" * 60)
print(f"Model: {MODEL_ID}")
print(f"Input: {INPUT_FOLDER}")
print(f"Output: {OUTPUT_FOLDER}")
print("=" * 60)

client = genai.Client(api_key=API_KEY)

# Create test output directory
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Get first 5 images only
all_images = sorted([
    f for f in os.listdir(INPUT_FOLDER)
    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
])

TEST_COUNT = 5
test_images = all_images[:TEST_COUNT]

print(f"\n🍌 Processing first {TEST_COUNT} images as test:\n")
for i, img in enumerate(test_images, 1):
    print(f"  {i}. {img}")

print("\n" + "=" * 60)
print("Starting test processing...")
print()

# Track timing and success
start_time = time.time()
processed = 0
errors = 0

for index, filename in enumerate(test_images, 1):
    input_path = os.path.join(INPUT_FOLDER, filename)
    output_filename = Path(filename).stem + "_test_processed.png"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    print(f"[{index}/{TEST_COUNT}] 🔄 Processing {filename}...")
    print(f"    Original: {input_path}")

    try:
        # Load image
        img = Image.open(input_path)
        original_size = img.size
        print(f"    Size: {original_size[0]}x{original_size[1]}")

        # Pre-crop to square if needed
        width, height = img.size
        if width != height:
            min_dim = min(width, height)
            left = (width - min_dim) // 2
            top = (height - min_dim) // 2
            right = left + min_dim
            bottom = top + min_dim
            img = img.crop((left, top, right, bottom))
            print(f"    Pre-cropped to: {min_dim}x{min_dim}")

        # Convert image to bytes for API
        import io
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()

        # Send to API
        print(f"    Sending to Nano Banana Pro...")
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

        # Save result
        saved = False
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data:
                    image_data = part.inline_data.data
                    with open(output_path, 'wb') as f:
                        f.write(image_data)

                    # Check output file size
                    file_size = os.path.getsize(output_path)
                    file_size_mb = file_size / (1024 * 1024)

                    print(f"    ✅ Saved: {output_filename}")
                    print(f"    Output size: {file_size_mb:.2f} MB")
                    processed += 1
                    saved = True
                    break

        if not saved:
            print(f"    ❌ No image returned from API")
            errors += 1

        # Brief pause between requests
        if index < TEST_COUNT:
            print(f"    Waiting 3 seconds before next image...")
            print()
            time.sleep(3)

    except Exception as e:
        print(f"    ❌ Error: {str(e)}")
        errors += 1
        print()
        time.sleep(5)

# Calculate statistics
end_time = time.time()
total_time = end_time - start_time
avg_time = total_time / TEST_COUNT if TEST_COUNT > 0 else 0

print("\n" + "=" * 60)
print("🧪 TEST RESULTS")
print("=" * 60)
print(f"Images processed: {processed}/{TEST_COUNT}")
print(f"Errors: {errors}")
print(f"Total time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
print(f"Average per image: {avg_time:.1f} seconds")
print(f"\nProcessed images saved to: {OUTPUT_FOLDER}")
print("=" * 60)

# Estimated full batch time
if processed > 0:
    total_images = len(all_images)
    estimated_total_time = avg_time * total_images
    estimated_hours = estimated_total_time / 3600

    print(f"\n📊 FULL BATCH ESTIMATE (if you process all {total_images} images):")
    print(f"   Estimated time: {estimated_hours:.1f} hours")
    print(f"   Estimated cost: ${0.04 * total_images:.2f} - ${0.13 * total_images:.2f} USD")

print("\n💡 NEXT STEPS:")
print("   1. Open the test output folder:")
print(f"      open {OUTPUT_FOLDER}")
print("   2. Compare original vs processed images")
print("   3. Verify quality meets your requirements")
print("   4. If satisfied, run the full batch:")
print("      python3 batch_process_cakes.py")
print("\n   If quality needs adjustment, modify the prompt in batch_process_cakes.py")
