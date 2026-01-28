#!/usr/bin/env bash
set -e

echo "🔧 Installing Piper TTS..."

wget -q https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz
tar -xzf piper_linux_x86_64.tar.gz
rm piper_linux_x86_64.tar.gz

# Force permissions
chmod -R 755 piper/
chmod 644 piper/*.onnx piper/*.json 2>/dev/null || true   # models if you add them later

# Debug: show permissions
ls -l piper/piper
file piper/piper   # should say ELF 64-bit ...

# Optional: test run (won't work without model yet, but checks binary)
./piper/piper --help || true

echo "✅ Piper ready at $(pwd)/piper/piper"