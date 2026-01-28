#!/usr/bin/env bash
set -e

echo "🔧 Installing Piper TTS..."

# Create tools directory
mkdir -p tools
cd tools

# Download Piper Linux binary (CPU)
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_linux_x86_64.tar.gz

# Extract
tar -xzf piper_linux_x86_64.tar.gz

# Make executable
chmod +x piper

# Move to PATH
mv piper /usr/local/bin/piper

# Verify install
piper --version

echo "✅ Piper installed successfully"
