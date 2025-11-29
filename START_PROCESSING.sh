#!/bin/bash
# Quick start script for batch processing cake images

echo "🍰 Orly's Cake Gallery - Batch Processor"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ ERROR: .env file not found!"
    echo "Please create .env file with your API key:"
    echo ""
    echo "GOOGLE_API_KEY=your_key_here"
    echo ""
    exit 1
fi

# Check if Python packages are installed
if ! python3 -c "import google.genai" 2>/dev/null; then
    echo "📦 Installing required packages..."
    pip3 install -r requirements.txt
fi

echo "✅ Environment ready!"
echo ""
echo "Starting batch processing of 103 cake images..."
echo "This will take approximately 8-10 hours."
echo ""
echo "You can:"
echo "  - Let it run in the background"
echo "  - Press Ctrl+C to stop (safe to resume later)"
echo "  - Monitor progress in processing_log.txt"
echo ""
read -p "Press Enter to start, or Ctrl+C to cancel..."
echo ""

# Run the batch processor
python3 batch_process_cakes.py

echo ""
echo "✅ Processing complete!"
echo "Check images/cakes-processed/ for results"
