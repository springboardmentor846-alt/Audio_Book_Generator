import React, { useState } from "react";
import axios from "axios";

export default function StudyModeTest() {
  const API = "http://localhost:5000";

  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [chunks, setChunks] = useState([]);

  const [currentChunk, setCurrentChunk] = useState(0);
  const [audioUrl, setAudioUrl] = useState("");

  const [understood, setUnderstood] = useState(0);
  const [notUnderstood, setNotUnderstood] = useState(0);

  const [loading, setLoading] = useState(false);

  // ================= UPLOAD =================
  const handleUpload = async () => {
    if (!file) return alert("Select file");

    try {
      setLoading(true);

      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post(`${API}/upload`, formData);

      setText(res.data.text);

      // simple chunk split (no LLM)
      const splitChunks = res.data.text.split(". ").slice(0, 10);
      setChunks(splitChunks);

    } catch {
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  // ================= AUDIO =================
  const playChunkAudio = async (chunkText) => {
    try {
      const res = await axios.post(
        `${API}/generate-audio`,
        {
          text: chunkText,
          rate: 180,
          volume: 1,
          language: "en",
        },
        { responseType: "blob" }
      );

      const url = URL.createObjectURL(res.data);
      setAudioUrl(url);

    } catch {
      alert("Audio failed");
    }
  };

  // ================= NEXT =================
  const handleNext = () => {
    if (currentChunk < chunks.length - 1) {
      setCurrentChunk(currentChunk + 1);
      setAudioUrl("");
    }
  };

  // ================= UNDERSTANDING =================
  const handleUnderstand = (type) => {
    if (type === "yes") setUnderstood(understood + 1);
    else setNotUnderstood(notUnderstood + 1);

    handleNext();
  };

  // ================= SCORE =================
  const total = understood + notUnderstood;
  const score = total === 0 ? 0 : Math.round((understood / total) * 100);

  // ================= KEY POINTS =================
  const getKeyPoints = () => {
    if (!text) return [];

    return text
      .split(". ")
      .filter((s) => s.length > 60)
      .slice(0, 5);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f0f1a] via-[#141423] to-[#0b0b14] text-white px-6 py-10">

      {/* HEADER */}
      <h1 className="text-3xl font-bold mb-2">🧠 Study Mode (Test)</h1>
      <p className="text-gray-400 mb-8">
        Interactive learning with smart pauses (no AI rewrite yet)
      </p>

      {/* ================= UPLOAD ================= */}
      <div className="bg-white/5 p-6 rounded-xl mb-6">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />

        <button
          onClick={handleUpload}
          className="mt-4 bg-purple-600 px-5 py-2 rounded-lg"
        >
          Upload & Extract
        </button>

        {loading && (
          <p className="mt-2 text-purple-400 animate-pulse">
            Processing...
          </p>
        )}
      </div>

      {/* ================= KEY POINTS ================= */}
      {text && (
        <div className="bg-white/5 p-6 rounded-xl mb-6">
          <h2 className="font-semibold mb-3">📌 Key Points</h2>

          <ul className="list-disc pl-5 text-gray-300">
            {getKeyPoints().map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </div>
      )}

      {/* ================= CHUNK PLAYER ================= */}
      {chunks.length > 0 && (
        <div className="bg-white/5 p-6 rounded-xl mb-6">

          <h2 className="font-semibold mb-4">
            📖 Chunk {currentChunk + 1} / {chunks.length}
          </h2>

          <p className="text-gray-300 mb-4">
            {chunks[currentChunk]}
          </p>

          <button
            onClick={() => playChunkAudio(chunks[currentChunk])}
            className="bg-blue-600 px-4 py-2 rounded"
          >
            🔊 Play Audio
          </button>

          {audioUrl && (
            <audio controls src={audioUrl} className="mt-4 w-full" />
          )}

          {/* UNDERSTANDING */}
          <div className="mt-6 flex gap-4">
            <button
              onClick={() => handleUnderstand("yes")}
              className="bg-green-600 px-4 py-2 rounded"
            >
              ✅ Got it
            </button>

            <button
              onClick={() => handleUnderstand("no")}
              className="bg-red-600 px-4 py-2 rounded"
            >
              ❌ Explain Again
            </button>
          </div>

        </div>
      )}

      {/* ================= SCORE ================= */}
      {total > 0 && (
        <div className="bg-white/5 p-6 rounded-xl">
          <h2 className="font-semibold mb-2">📊 Understanding Score</h2>

          <p className="text-2xl font-bold text-purple-400">
            {score}%
          </p>

          <p className="text-gray-400 text-sm">
            Based on your responses during learning
          </p>
        </div>
      )}

    </div>
  );
}