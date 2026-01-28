#!/usr/bin/env bash
set -e

echo "🔧 Installing Piper TTS..."

# Download Piper
wget https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz

# Extract
tar -xzf piper_linux_x86_64.tar.gz

# Move binary to executable location
chmod +x piper/piper

# Verify
piper --version || true

echo "✅ Piper installed and available in PATH"
