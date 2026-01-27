from huggingface_hub import InferenceClient
import io
import traceback


class LobotomyAgent:
    def __init__(self, token, model_name):
        self.client = InferenceClient(token=token)
        self.model_name = model_name
        self.system_prompt = self._load_prompt()

        # Piper config
        self.voice_map = {
                        "joe": "piper_models/en_US-joe-medium.onnx",
                        "norman": "piper_models/en_US-norman-medium.onnx",
                        "narrator": "piper_models/en_US-narrator-medium.onnx",
                        }


    def _load_prompt(self):
        try:
            with open("prompt.txt", "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            print("Warning: prompt.txt not found → fallback prompt")
            return "You are the Narrator of the Lobotomy. Lobotomize everything into insane JJK brainrot."

    def transform_text(self, user_input):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input},
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=120,               
                temperature=0.95,               
                top_p=0.92,                    
                presence_penalty=0.5,          
                frequency_penalty=0.3,         
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[TEXT GEN ERROR] {type(e).__name__}: {e}")
            traceback.print_exc()
            return "DOMAIN EXPANSION: ERROR VOID! Brain agendad... Nah, I'd crash."

    def generate_audio(self, text ,voice="joe"):
        import subprocess
        import uuid
        import os
        import io

        try:
            filename = f"/tmp/{uuid.uuid4()}.wav"
            model_path = self.voice_map.get(voice, self.voice_map["joe"])
            process = subprocess.run(
                [
                    "piper",
                    "--model", model_path,
                    "--output_file", filename
                ],
                input=text.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )

            with open(filename, "rb") as f:
                audio_bytes = f.read()

            os.remove(filename)

            return io.BytesIO(audio_bytes)

        except Exception as e:
            print("[PIPER TTS ERROR]", e)
            return None
