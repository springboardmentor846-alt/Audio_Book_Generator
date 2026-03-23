import React, { useState } from "react";
import axios from "axios";
import MindMap from "../components/MindMap";
import { useNavigate } from "react-router-dom";



export default function StudyMode() {
  const API = "http://localhost:5000";

  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [rewrittenText, setRewrittenText] = useState("");
  const [qa, setQa] = useState([]);
  const [mindmap, setMindmap] = useState(null);

  const [loading, setLoading] = useState(false);

  // STATE
  const [audioUrl, setAudioUrl] = useState("");
  const [language, setLanguage] = useState("en");
  const [generatingAudio, setGeneratingAudio] = useState(false);

  const [activeQA, setActiveQA] = useState({});
  const navigate = useNavigate();
  const [attempted, setAttempted] = useState(0);

  // ================= UPLOAD =================
  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(`${API}/upload`, formData);
    setText(res.data.text);
  };

  // ================= LLM ENRICH =================
  const handleStudyProcess = async () => {
    setLoading(true);

    const res = await axios.post(`${API}/rewrite-study`, {
      text,
      doc_type: "Study Notes"
    });

    setRewrittenText(res.data.notes);
    setQa(res.data.qa);
    setMindmap(res.data.mindmap);

    setLoading(false);
  };


  // =================  audio =================
  const handleAudio = async () => {
    try {
      setGeneratingAudio(true);

      const res = await axios.post(
        `${API}/generate-audio`,
        {
          text: rewrittenText,
          language,
          rate: 180,
          volume: 1,
        },
        { responseType: "blob" }
      );

      setAudioUrl(URL.createObjectURL(res.data));
    } catch {
      alert("Audio failed");
    } finally {
      setGeneratingAudio(false);
    }
  };

  const generateHint = (answer) => {
  const words = answer.split(" ");
  return words.slice(0, Math.ceil(words.length / 3)).join(" ") + "...";
};

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f0f1a] via-[#141423] to-[#0b0b14] text-white px-6 py-10">

      <h1 className="text-3xl font-bold mb-2">🎓 Study Mode</h1>
      <p className="text-gray-400 mb-8">
        Learn deeply with structured notes, mind maps & smart revision.
      </p>

      {/* UPLOAD */}
      <div className="bg-white/5 p-6 rounded-2xl mb-6">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />

        <button
          onClick={handleUpload}
          className="mt-4 bg-purple-600 px-6 py-2 rounded-lg"
        >
          Upload
        </button>
      </div>

      {/* TEXT */}
      {text && (
        <div className="bg-white/5 p-6 rounded-2xl mb-6">
          <h2 className="mb-4 font-semibold">Extracted Text</h2>
          <div className="max-h-[200px] overflow-y-auto text-sm text-gray-300">
            {text}
          </div>

          <button
            onClick={handleStudyProcess}
            className="mt-6 bg-green-600 px-6 py-2 rounded-lg"
          >
            Generate Study Content
          </button>
        </div>
      )}

      {loading && (
        <div className="text-purple-400 animate-pulse">
          Generating smart study content...
        </div>
      )}

      {/* NOTES */}
      {rewrittenText && (
        <div className="bg-white/5 p-6 rounded-2xl mb-6">
          <h2 className="mb-4 font-semibold">📘 Smart Notes</h2>
          <div className="text-gray-300 whitespace-pre-line text-sm">
            {rewrittenText}
          </div>
        </div>
      )}

      {/* AUDIO */}
      {/* AUDIO SECTION */}
      {rewrittenText && (
        <div className="bg-white/5 p-6 rounded-2xl mb-6 border border-white/10">
          <h2 className="mb-4 font-semibold">🎧 Study Audio</h2>

          <div className="flex gap-4 items-center flex-wrap">

            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-black/40 p-2 rounded"
            >
              <option value="en">English</option>
              <option value="hi">Hindi</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
              <option value="ja">Japanese</option>
              <option value="zh">Chinese</option>
            </select>

            <button
              onClick={handleAudio}
              className="bg-purple-600 px-5 py-2 rounded-lg"
            >
              Generate Audio
            </button>
          </div>

          {generatingAudio && (
            <p className="text-purple-400 mt-3 animate-pulse">
              Generating audio...
            </p>
          )}

          {audioUrl && (
            <audio controls src={audioUrl} className="w-full mt-4" />
          )}
        </div>
      )}

      {/* MINDMAP */}
      {mindmap && <MindMap data={mindmap} />}

      {/* Q&A */}
      {qa.length > 0 && (
        <div className="bg-white/5 p-6 rounded-2xl mt-6">
          <h2 className="mb-4 font-semibold">🎯 Important Questions</h2>

          {qa.map((q, i) => (
            <div key={i} className="mb-6 border-b border-white/10 pb-4">

              <p className="font-medium">{q.question}</p>

              <div className="flex gap-3 mt-3 flex-wrap">

                <button
                  onClick={() =>
                    setActiveQA((prev) => ({
                      ...prev,
                      [i]: { ...prev[i], hint: !prev[i]?.hint },
                    }))
                  }
                  className="text-xs bg-yellow-500/20 px-3 py-1 rounded"
                >
                  Hint
                </button>

                <button
                  onClick={() => {
                    setAttempted(prev => prev + 1);
                    setActiveQA((prev) => ({
                      ...prev,
                      [i]: { ...prev[i], answer: !prev[i]?.answer },
                    }));
                  }}
                >
                  Answer
                </button>

              </div>

{activeQA[i]?.hint && (
  <p className="text-yellow-400 mt-2 text-sm">
    💡 {generateHint(q.answer)}
  </p>
)}

              {activeQA[i]?.answer && (
                <p className="text-green-400 mt-2 text-sm">
                  ✅ {q.answer}
                </p>
              )}

            </div>
          ))}
        </div>
      )}

      <button
  onClick={() =>
    navigate("/study-insights", {
      state: {
        totalWords: text.split(" ").length,
        questions: qa.length,
        attempted,
        mindmapNodes: JSON.stringify(mindmap).length,
      },
    })
  }
  className="mt-6 bg-blue-600 px-6 py-2 rounded-lg"
>
  📊 View Study Insights
</button>

    </div>
  );
}