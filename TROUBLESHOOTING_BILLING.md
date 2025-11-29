# Troubleshooting: Quota Exceeded / Billing Issues

## Problem
Getting "RESOURCE_EXHAUSTED" / "Quota exceeded for metric" errors even with billing enabled.

## Error Message
```
429 RESOURCE_EXHAUSTED
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_input_token_count
* Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests
```

## Root Cause
The API key is using the **free tier quota** instead of the paid tier, even though billing is enabled.

## Solutions

### Step 1: Verify Billing is Enabled on Correct Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project (check the project dropdown at the top)
3. Go to **Billing** → **Account Management**
4. Verify billing is enabled for THIS specific project
5. Note the project ID

### Step 2: Check Which Project Your API Key Belongs To

1. Go to [Google AI Studio](https://aistudio.google.com)
2. Click on **Get API Key** (top right)
3. Check which project the API key is associated with
4. **Important:** The API key must be from a project with billing enabled

### Step 3: Create New API Key with Billing Enabled

If the API key is from a different project:

1. In [Google Cloud Console](https://console.cloud.google.com)
2. Select the project **with billing enabled**
3. Go to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **API Key**
5. Copy the new API key
6. Update `.env` file:
   ```
   GOOGLE_API_KEY=your_new_api_key_here
   ```

### Step 4: Enable Required APIs

Make sure these APIs are enabled on your billing-enabled project:

1. Go to **APIs & Services** → **Library**
2. Search for and enable:
   - Generative Language API
   - Vertex AI API (if needed)

### Step 5: Check Quota Limits

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **IAM & Admin** → **Quotas**
3. Search for: `generativelanguage.googleapis.com`
4. Check if you see "free tier" or "paid tier" limits
5. If still showing free tier, billing might not be fully activated

### Step 6: Wait for Billing Activation

Sometimes billing activation takes time:
- **Immediate:** API key creation
- **Minutes:** Quota updates
- **Hours:** Full billing activation
- **24-48 hours:** In rare cases

### Step 7: Check Your Usage Dashboard

Visit: https://ai.dev/usage?tab=rate-limit

This shows:
- Current quota limits
- Usage statistics
- Whether you're on free or paid tier

## Alternative: Use Google AI Studio Web Interface

While troubleshooting billing, you can process images manually:

1. Go to [Google AI Studio](https://aistudio.google.com)
2. Create a new prompt
3. Upload one cake image at a time
4. Paste the prompt from `NANO_BANANA_PRO_PROMPT.txt`
5. Generate and download the result

**Pros:** Works immediately, no billing issues
**Cons:** Manual process for all 103 images (tedious)

## Alternative Models

If Nano Banana Pro requires paid tier, try these free tier models:

### Option 1: Use Gemini 2.5 Flash with Image Understanding

```python
MODEL_ID = "gemini-2.5-flash"
```

This won't generate new images but could help with:
- Analyzing cake images
- Creating descriptions
- Quality checking

### Option 2: Use Imagen for Image Generation

```python
MODEL_ID = "imagen-4.0-generate-001"  # or imagen-4.0-fast-generate-001
```

These are dedicated image generation models that might have better free tier support.

## Checking Current Project & Billing Status

Run this diagnostic script:

```bash
python3 -c "
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))

print('Checking API configuration...')
print('=' * 60)

# This will show quota/billing errors if any
try:
    response = client.models.get(model='nano-banana-pro-preview')
    print(f'Model: {response.name}')
    print(f'Display Name: {response.display_name if hasattr(response, \"display_name\") else \"N/A\"}')
    print('✅ API key working')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

## Contact Google Support

If billing is definitely enabled but still hitting free tier limits:

1. Go to [Google Cloud Support](https://cloud.google.com/support)
2. Create a support case
3. Mention:
   - API key is hitting free tier limits
   - Billing is enabled on the project
   - Requesting quota increase or paid tier activation

## Expected Behavior When Billing Works

When billing is properly enabled, you should see:
- **No quota errors** for reasonable usage
- **Pay-per-use** charges (~$0.04-0.13 per image)
- **Higher rate limits** (not free tier restrictions)

## Cost Monitoring

Once billing works:
1. Set up billing alerts in Google Cloud Console
2. Monitor costs at: https://console.cloud.google.com/billing
3. Expected cost for 103 images: **$5-15 USD**

## Summary

**Most likely issue:** API key is from a project without billing, or billing hasn't fully activated yet.

**Quick fix:** Create a new API key from a billing-enabled project.

**Workaround:** Use Google AI Studio web interface manually while resolving billing.
