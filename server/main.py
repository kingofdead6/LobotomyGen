from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from agent import LobotomyAgent
from urllib.parse import quote
import os
import tempfile
import subprocess
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# --- CONFIG ---
TEXT_MODEL = os.getenv("TEXT_MODEL")
BG_MUSIC_PATH = os.getenv("BG_MUSIC_PATH", "./bgmusic.mp3")

# ----------------- UTILS -----------------
def merge_voice_with_music(
    voice_path: str,
    music_path: str,
    output_path: str,
    music_volume: float = 0.2,
):
    """
    Merge voice + background music using ffmpeg
    """
    command = [
        "ffmpeg",
        "-y",
        "-i", voice_path,
        "-stream_loop", "-1",
        "-i", music_path,
        "-filter_complex",
        f"[1:a]volume={music_volume}[bg];"
        f"[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        output_path
    ]

    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )


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
        jjk_agent = LobotomyAgent(hf_api_key, TEXT_MODEL)
        transformed_text = jjk_agent.transform_text(user_message)
        safe_text = quote(transformed_text[:1000])

        return jsonify({
            "transformed": transformed_text,
            "voice_api_url": (
                f"/voice_with_music?"
                f"text={safe_text}&voice={voice}&hf_api_key={hf_api_key}"
            )
        })

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
        jjk_agent = LobotomyAgent(hf_api_key, TEXT_MODEL)

        # Generate voice audio
        voice_audio = jjk_agent.generate_audio(text, voice)
        if not voice_audio:
            return jsonify({"error": "Voice generation failed"}), 500

        # Save voice to temp file
        temp_voice_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        with open(temp_voice_path, "wb") as f:
            f.write(voice_audio.read())

        # Output file
        temp_output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name

        # Merge using ffmpeg
        merge_voice_with_music(
            voice_path=temp_voice_path,
            music_path=BG_MUSIC_PATH,
            output_path=temp_output_path,
            music_volume=0.2,
        )

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


# ----------------- ENTRY -----------------
if __name__ == "__main__":
    print("Lobotomy Kaisen Server Starting... 🚀💀")
    print(f"Using Text model: {TEXT_MODEL}")
    print(f"Background music: {BG_MUSIC_PATH}")
    app.run(host="0.0.0.0", port=5000)
