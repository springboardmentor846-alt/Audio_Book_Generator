import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Upload() {
  const API = "http://localhost:5000";

  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [chunks, setChunks] = useState([]);

  const [docType, setDocType] = useState("");
  const [confidence, setConfidence] = useState("");

  const [rewrittenText, setRewrittenText] = useState("");
  const [audioUrl, setAudioUrl] = useState("");

  const [style, setStyle] = useState("Standard");
  const [rate, setRate] = useState(180);
  const [volume, setVolume] = useState(1);
  const [language, setLanguage] = useState("en");

  // STEP LOADERS
  const [uploading, setUploading] = useState(false);
  const [rewriting, setRewriting] = useState(false);
  const [generating, setGenerating] = useState(false);

  const navigate = useNavigate();

const handleInsights = async () => {
  const res = await axios.post(`${API}/insights`, {
    text,
    chunks,
    doc_type: docType,
    confidence,
  });

  navigate("/insights", { state: res.data });
};

  // ================= UPLOAD =================
  const handleUpload = async () => {
    if (!file) return alert("Select file");

    try {
      setUploading(true);

      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post(`${API}/upload`, formData);

      setText(res.data.text);
      setChunks(res.data.chunks);
      setDocType(res.data.doc_type);
      setConfidence(res.data.confidence);
    } catch (err) {
      alert("Upload failed");
    } finally {
      setUploading(false);
    }
  };

  // ================= REWRITE =================
  const handleRewrite = async () => {
    try {
      setRewriting(true);

      const res = await axios.post(`${API}/rewrite`, {
        chunks,
        style,
        doc_type: docType,
      });

      setRewrittenText(res.data.rewritten_text);
    } catch {
      alert("Rewrite failed");
    } finally {
      setRewriting(false);
    }
  };

  // ================= AUDIO =================
  const handleAudio = async () => {
    try {
      setGenerating(true);

      const res = await axios.post(
        `${API}/generate-audio`,
        {
          text: rewrittenText,
          style,
          rate,
          volume,
          language,
        },
        { responseType: "blob" }
      );

      setAudioUrl(URL.createObjectURL(res.data));
    } catch {
      alert("Audio failed");
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f0f1a] via-[#141423] to-[#0b0b14] text-white px-6 py-10">

      {/* HEADER */}
      <h1 className="text-3xl font-bold mb-2">🎧 Listener Mode</h1>
      <p className="text-gray-400 mb-8">
        Convert any content into immersive audio.  
        Switch to <span className="text-purple-400">Study Mode</span> for quizzes & learning.
      </p>

      {/* ================= STEP 1 ================= */}
      <div className="bg-white/5 backdrop-blur-lg p-6 rounded-2xl border border-white/10 mb-6">
        <h2 className="text-lg font-semibold mb-4">📂 Upload</h2>

        <input type="file" onChange={(e) => setFile(e.target.files[0])} />

        <button
          onClick={handleUpload}
          className="mt-4 bg-purple-600 px-5 py-2 rounded-lg"
        >
          Upload & Extract
        </button>

        {uploading && (
          <div className="mt-3 text-sm text-purple-400 animate-pulse">
            Processing file...
          </div>
        )}
      </div>

      {/* DOC TYPE */}
{docType && (
        <div className="bg-gradient-to-r from-purple-600/20 to-blue-600/20 p-5 rounded-xl mb-6 border border-purple-400/20">
          <h3 className="text-lg font-semibold mb-1">
            📄 Detected Document Type: {docType}
          </h3>
          <p className="text-gray-300 text-sm">
            Confidence: {confidence}% — Audio will be optimized accordingly.
            You can manually override tone below.
          </p>
        </div>
      )}

      {/* ================= TEXT ================= */}
      {text && (
        <div className="bg-white/5 p-6 rounded-2xl mb-6">
          <h2 className="text-lg font-semibold mb-4">Extracted Text</h2>

          <div className="max-h-[250px] overflow-y-auto bg-black/40 p-4 rounded-lg text-sm">
            {text}
          </div>
        </div>
      )}

      {/* ================= CONTROLS ================= */}
      {text && (
        <div className="bg-white/5 p-6 rounded-2xl mb-6">

          <h2 className="text-lg font-semibold mb-4">🎛 Audio Settings</h2>

          {/* GRID CONTROLS */}
          <div className="grid md:grid-cols-3 gap-4">

            {/* STYLE */}
            <div>
              <label className="text-sm text-gray-400">Tone</label>
              <select
                value={style}
                onChange={(e) => setStyle(e.target.value)}
                className="w-full p-2 mt-1 rounded bg-black/50"
              >
                <option>Standard</option>
                <option>Dramatic</option>
                <option>Cinematic</option>
              </select>
            </div>

            {/* LANGUAGE */}
            <div>
              <label className="text-sm text-gray-400">Language</label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full p-2 mt-1 rounded bg-black/50"
              >
                <option value="en">English</option>
                <option value="hi">Hindi</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
                <option value="it">Italian</option>
                <option value="ja">Japanese</option>
                <option value="zh">Chinese</option>
              </select>
            </div>

            {/* SPEED */}
            <div>
              <label className="text-sm text-gray-400">Speed</label>
              <input
                type="range"
                min="120"
                max="220"
                value={rate}
                onChange={(e) => setRate(e.target.value)}
                className="w-full"
              />
            </div>

            {/* VOLUME */}
            <div>
              <label className="text-sm text-gray-400">Volume</label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={volume}
                onChange={(e) => setVolume(e.target.value)}
                className="w-full"
              />
            </div>

          </div>

          <button
            onClick={handleRewrite}
            className="mt-6 bg-green-600 px-6 py-2 rounded-lg"
          >
            ✨ Rewrite
          </button>

          {rewriting && (
            <div className="mt-3 text-sm text-green-400 animate-pulse">
              AI rewriting...
            </div>
          )}
        </div>
      )}

      {/* ================= REWRITTEN ================= */}
      {rewrittenText && (
        <div className="bg-white/5 p-6 rounded-2xl mb-6">
          <h2 className="text-lg font-semibold mb-4">AI Narration</h2>

          <div className="max-h-[250px] overflow-y-auto bg-black/40 p-4 rounded-lg text-sm">
            {rewrittenText}
          </div>

          <button
            onClick={handleAudio}
            className="mt-6 bg-purple-600 px-6 py-2 rounded-lg"
          >
            🎧 Generate Audio
          </button>

          {generating && (
            <div className="mt-3 text-sm text-purple-400 animate-pulse">
              Generating audio...
            </div>
          )}
        </div>
      )}

      {/* ================= AUDIO ================= */}
      {audioUrl && (
        <div className="bg-white/5 p-6 rounded-2xl">
          <h2 className="text-lg font-semibold mb-4">Your Audio</h2>
          <audio controls src={audioUrl} className="w-full" />
        </div>
      )}

      {audioUrl && (
  <button
    onClick={handleInsights}
    className="mt-6 bg-blue-600 px-6 py-2 rounded-lg"
  >
    📊 View Insights
  </button>
)}
    </div>
  );
}
