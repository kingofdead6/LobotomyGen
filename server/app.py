from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from agent import LobotomyAgent
from urllib.parse import quote
import os
from pydub import AudioSegment
import tempfile
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# --- CONFIG ---
TEXT_MODEL = os.getenv("TEXT_MODEL")
BG_MUSIC_PATH = os.getenv("BG_MUSIC_PATH", "./bgmusic.mp3")

# ----------------- ROUTES -----------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/transform", methods=["POST"])
def transform():
    data = request.get_json() or request.form
    user_message = data.get("message")
    voice = data.get("voice", "joe")
    hf_api_key = data.get("hf_api_key") 

    if not hf_api_key:
        return jsonify({"error": "No Hugging Face API key provided"}), 401

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Initialize agent per request with user's HF key
        jjk_agent = LobotomyAgent(hf_api_key, TEXT_MODEL)
        transformed_text = jjk_agent.transform_text(user_message)
        safe_text = quote(transformed_text[:500])

        return jsonify(
            {
                "transformed": transformed_text,
                "voice_api_url": f"/voice_with_music?text={safe_text}&voice={voice}&hf_api_key={hf_api_key}",
            }
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/voice_with_music", methods=["GET"])
def voice_with_music():
    text = request.args.get("text", "")
    voice = request.args.get("voice", "joe")
    hf_api_key = request.args.get("hf_api_key") 

    if not hf_api_key:
        return jsonify({"error": "No Hugging Face API key provided"}), 401

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Initialize agent per request with user's HF key
        jjk_agent = LobotomyAgent(hf_api_key, TEXT_MODEL)
        voice_audio = jjk_agent.generate_audio(text, voice)
        if not voice_audio:
            return jsonify({"error": "Voice generation failed"}), 500

        # Save voice to temp file
        temp_voice_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        with open(temp_voice_path, "wb") as f:
            f.write(voice_audio.read())

        # Merge with background music
        final_audio = AudioSegment.from_wav(temp_voice_path)
        bg_audio = AudioSegment.from_file(BG_MUSIC_PATH)

        # Loop background if shorter than voice
        if len(bg_audio) < len(final_audio):
            bg_audio = bg_audio * ((len(final_audio) // len(bg_audio)) + 1)
        bg_audio = bg_audio[:len(final_audio)]

        merged = final_audio.overlay(bg_audio - 10)  # reduce bg volume slightly

        temp_output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        merged.export(temp_output_path, format="mp3")

        return send_file(
            temp_output_path,
            as_attachment=True,
            mimetype="audio/mpeg",
            download_name="lobotomy_with_music.mp3"
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Lobotomy Kaisen Server Starting... 🚀💀")
    print(f"Using Text model: {TEXT_MODEL}")
    print(f"Fixed background music: {BG_MUSIC_PATH}")
    app.run(debug=True, host="0.0.0.0", port=5000)
