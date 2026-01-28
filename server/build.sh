#!/usr/bin/env bash
set -e

echo "🔧 Installing Piper TTS..."

wget -q https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz
tar -xzf piper_linux_x86_64.tar.gz
rm piper_linux_x86_64.tar.gz

mkdir -p piper_models

# Download joe medium (add others if needed)
wget -q https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/joe/medium/en_US-joe-medium.onnx -O piper_models/en_US-joe-medium.onnx
wget -q https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/joe/medium/en_US-joe-medium.onnx.json -O piper_models/en_US-joe-medium.onnx.json

# Force permissions
chmod -R 755 piper/
chmod -R 644 piper_models/*
chmod 755 piper/piper   # explicit on binary

# Move to system bin (avoids relative path and permission issues)
cp piper/piper /usr/local/bin/piper

# Debug output
ls -la piper/ piper_models/
file piper/piper
ls -l /usr/local/bin/piper
/usr/local/bin/piper --help || echo "Piper --help failed (expected without model)"

echo "✅ Piper ready at /usr/local/bin/piper"