#!/bin/bash
# Quick fix script for Django admin CSS not loading

echo "🔧 Fixing Static Files for Django Admin..."
echo ""

# Navigate to project directory
cd "/Users/akil/Desktop/kuwait project/edupulse"

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install WhiteNoise
echo "📥 Installing WhiteNoise..."
pip install whitenoise

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Static files collected successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Update edupulse/settings.py - Add this line to MIDDLEWARE (after SecurityMiddleware):"
echo "   'whitenoise.middleware.WhiteNoiseMiddleware',"
echo ""
echo "2. Uncomment this line in edupulse/settings.py:"
echo "   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'"
echo ""
echo "3. Restart your Django server"
echo ""
echo "🎉 Done! Your admin CSS should now load properly."

