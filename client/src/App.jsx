import { useState } from "react";
import backgroundImg from "./assets/lk_background.jpg"; // Suggested: abstract cursed energy or anime scene
import energyEffect from "./assets/energy_overlay.png"; // Suggested: glowing effect overlay

const VOICES = [
  { label: "Joe (medium)", value: "joe" },
  { label: "Norman (medium)", value: "norman" },
  { label: "lessac (medium)", value: "lessac" },
];

export default function App() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [audioUrl, setAudioUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [voice, setVoice] = useState(VOICES[0].value);

  const handleTransform = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setOutput("");
    setAudioUrl(null);

    try {
      const res = await fetch("http://localhost:5000/transform", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input, voice }),
      });

      const data = await res.json();
      setOutput(data.transformed);

      if (data.voice_api_url) {
        setAudioUrl(`http://localhost:5000${data.voice_api_url}`);
      }
    } catch (e) {
      setOutput("DOMAIN EXPANSION FAILED 💀");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center p-6 relative overflow-hidden"
      style={{
        background: `url(${backgroundImg}) center/cover no-repeat`,
      }}
    >
      {/* Overlay energy effect */}
      <img
        src={energyEffect}
        alt="Energy Effect"
        className="absolute inset-0 w-full h-full object-cover mix-blend-overlay opacity-30 pointer-events-none animate-pulse-slow"
      />

      <div className="relative z-10 w-full max-w-3xl bg-black/40 backdrop-blur-xl rounded-3xl shadow-2xl p-8 space-y-6 border border-red-600/50">
        <h1 className="text-4xl md:text-5xl font-extrabold text-center text-red-500 tracking-wide drop-shadow-lg animate-pulse">
          🧠 Lobotomy Kaisen
        </h1>

        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Speak, sorcerer…"
          className="w-full h-36 md:h-40 rounded-2xl bg-black/70 border border-red-700 p-5 text-white text-lg placeholder-red-400 focus:outline-none focus:ring-2 focus:ring-red-500 transition-shadow shadow-red-500/50"
        />

        <select
          value={voice}
          onChange={(e) => setVoice(e.target.value)}
          className="w-full p-3 rounded-xl bg-black/70 border border-red-700 text-white focus:outline-none focus:ring-2 focus:ring-red-500 text-lg"
        >
          {VOICES.map((v) => (
            <option key={v.value} value={v.value}>
              {v.label}
            </option>
          ))}
        </select>

        <div className="flex gap-4">
          <button
            onClick={handleTransform}
            disabled={loading}
            className="flex-1 py-4 rounded-2xl bg-red-600 hover:bg-red-700 transition-all font-bold text-lg shadow-red-500/70 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "DOMAIN EXPANDING…" : "Lobotomize"}
          </button>
        </div>

        {output && (
          <div className="bg-black/60 border border-red-700 rounded-2xl p-5 whitespace-pre-wrap text-lg shadow-lg shadow-red-500/40 animate-fade-in">
            {output}
          </div>
        )}

        {audioUrl && (
          <div className="flex flex-col items-center mt-4 space-y-2">
            <audio controls autoPlay className="w-full rounded-xl">
              <source src={audioUrl} type="audio/mpeg" />
            </audio>
            <a
              href={audioUrl}
              download={`lobotomy_voice_${voice}.mp3`}
              className="text-red-500 hover:text-red-400 hover:underline font-semibold transition-colors"
            >
              ⬇️ Download Audio
            </a>
          </div>
        )}

        <p className="text-xs text-center text-red-400/60 mt-4">
          Powered by HF Text + Piper TTS • CC0 Voices
        </p>
      </div>
    </div>
  );
}
