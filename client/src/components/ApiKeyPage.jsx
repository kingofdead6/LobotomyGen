import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

export default function ApiKeyPage() {
  const navigate = useNavigate();
  const [apiKey, setApiKey] = useState("");

  const handleSave = () => {
    if (!apiKey.trim()) return alert("Enter your Hugging Face API key!");
    Cookies.set("hf_api_key", apiKey, { expires: 7 }); // saved for 7 days
    navigate("/generate"); // redirect to generator page
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6 bg-black/90 text-white">
      <div className="w-full max-w-md bg-black/60 backdrop-blur-xl rounded-3xl shadow-2xl p-8 space-y-6 border border-red-600/50">
        <h1 className="text-4xl font-extrabold text-red-500 text-center tracking-wide animate-pulse">
          🔑 Enter Hugging Face API
        </h1>

        <input
          type="password"
          placeholder="hf_xxxxx..."
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          className="w-full p-4 rounded-2xl bg-black/70 border border-red-700 text-white text-lg placeholder-red-400 focus:outline-none focus:ring-2 focus:ring-red-500"
        />

        <button
          onClick={handleSave}
          className="w-full py-4 rounded-2xl bg-red-600 hover:bg-red-700 transition-all font-bold text-lg shadow-red-500/70 hover:scale-105"
        >
          Save & Continue
        </button>

        <p className="text-xs text-red-400/60 text-center">
          Your API key is saved locally in cookies for 7 days.
        </p>
      </div>
    </div>
  );
}
