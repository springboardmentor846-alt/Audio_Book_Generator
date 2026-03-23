// import React, { useState } from "react";
// import axios from "axios";

// export default function App() {
//   const API = "http://localhost:5000";

//   // ================= STATE =================
//   const [activeTab, setActiveTab] = useState("upload");

//   const [file, setFile] = useState(null);
//   const [text, setText] = useState("");
//   const [chunks, setChunks] = useState([]);

//   const [docType, setDocType] = useState("");
//   const [confidence, setConfidence] = useState("");

//   const [rewrittenText, setRewrittenText] = useState("");
//   const [audioUrl, setAudioUrl] = useState("");
//   const [insights, setInsights] = useState(null);

//   const [style, setStyle] = useState("Standard");
//   const [rate, setRate] = useState(180);
//   const [volume, setVolume] = useState(1);
//   const [language, setLanguage] = useState("en");

//   const [loading, setLoading] = useState(false);

//   // ================= UPLOAD =================
//   const handleUpload = async () => {
//     if (!file) return alert("Please select a file");

//     try {
//       setLoading(true);

//       const formData = new FormData();
//       formData.append("file", file);

//       const res = await axios.post(`${API}/upload`, formData, {
//         headers: { "Content-Type": "multipart/form-data" },
//       });

//       setText(res.data.text);
//       setChunks(res.data.chunks);
//       setDocType(res.data.doc_type);
//       setConfidence(res.data.confidence);

//       setActiveTab("narration");
//     } catch (err) {
//       console.error(err.response?.data || err.message);
//       alert("Upload failed");
//     } finally {
//       setLoading(false);
//     }
//   };

//   // ================= REWRITE =================
//   const handleRewrite = async () => {
//     try {
//       setLoading(true);

//       const res = await axios.post(`${API}/rewrite`, {
//         chunks,
//         style,
//         doc_type: docType,
//       });

//       setRewrittenText(res.data.rewritten_text);
//     } catch (err) {
//       console.error(err);
//       alert("Rewrite failed");
//     } finally {
//       setLoading(false);
//     }
//   };

//   // ================= AUDIO =================
//   const handleAudio = async () => {
//     try {
//       setLoading(true);

//       const res = await axios.post(
//         `${API}/generate-audio`,
//         {
//           text: rewrittenText,
//           style,
//           rate,
//           volume,
//           language,
//         },
//         { responseType: "blob" }
//       );

//       const url = URL.createObjectURL(res.data);
//       setAudioUrl(url);
//     } catch (err) {
//       console.error(err);
//       alert("Audio generation failed");
//     } finally {
//       setLoading(false);
//     }
//   };

//   // ================= INSIGHTS =================
//   const handleInsights = async () => {
//     try {
//       const res = await axios.post(`${API}/insights`, {
//         text,
//         chunks,
//         doc_type: docType,
//         confidence,
//       });

//       setInsights(res.data);
//     } catch (err) {
//       console.error(err);
//     }
//   };

//   // ================= UI =================
//   return (
//     <div className="min-h-screen bg-gradient-to-br from-gray-100 to-gray-200 p-6">
//       <h1 className="text-4xl font-bold mb-6 text-gray-800">
//         🎧 AI Audiobook Studio
//       </h1>

//       {/* Tabs */}
//       <div className="flex gap-4 mb-6">
//         {["upload", "narration"].map((tab) => (
//           <button
//             key={tab}
//             onClick={() => setActiveTab(tab)}
//             className={`px-5 py-2 rounded-xl font-semibold transition ${
//               activeTab === tab
//                 ? "bg-blue-600 text-white shadow-lg"
//                 : "bg-white shadow"
//             }`}
//           >
//             {tab.toUpperCase()}
//           </button>
//         ))}
//       </div>

//       {/* Loader */}
//       {loading && (
//         <div className="mb-4 text-blue-600 font-semibold animate-pulse">
//           ⏳ Processing...
//         </div>
//       )}

//       {/* ================= UPLOAD TAB ================= */}
//       {activeTab === "upload" && (
//         <div className="bg-white p-6 rounded-2xl shadow-lg space-y-4">
//           <input
//             type="file"
//             onChange={(e) => setFile(e.target.files[0])}
//           />

//           <button
//             onClick={handleUpload}
//             className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg"
//           >
//             Upload & Extract
//           </button>

//           {docType && (
//             <div className="bg-gray-100 p-3 rounded-lg">
//               📄 <b>{docType}</b> ({confidence}% confidence)
//             </div>
//           )}

//           {text && (
//             <textarea
//               value={text}
//               readOnly
//               className="w-full h-56 p-3 border rounded-lg"
//             />
//           )}
//         </div>
//       )}

//       {/* ================= NARRATION TAB ================= */}
//       {activeTab === "narration" && (
//         <div className="bg-white p-6 rounded-2xl shadow-lg space-y-5">
//           {/* Controls */}
//           <div className="flex gap-4 flex-wrap">
//             <select
//               value={style}
//               onChange={(e) => setStyle(e.target.value)}
//               className="p-2 border rounded"
//             >
//               <option>Standard</option>
//               <option>Dramatic</option>
//               <option>Cinematic</option>
//             </select>

//             <select
//               value={language}
//               onChange={(e) => setLanguage(e.target.value)}
//               className="p-2 border rounded"
//             >
//               <option value="en">English</option>
//               <option value="hi">Hindi</option>
//               <option value="es">Spanish</option>
//               <option value="fr">French</option>
//             </select>
//           </div>

//           {/* Sliders */}
//           <div>
//             <label className="font-semibold">Speech Rate: {rate}</label>
//             <input
//               type="range"
//               min="100"
//               max="250"
//               value={rate}
//               onChange={(e) => setRate(e.target.value)}
//               className="w-full"
//             />
//           </div>

//           <div>
//             <label className="font-semibold">Volume: {volume}</label>
//             <input
//               type="range"
//               min="0"
//               max="1"
//               step="0.1"
//               value={volume}
//               onChange={(e) => setVolume(e.target.value)}
//               className="w-full"
//             />
//           </div>

//           {/* Rewrite */}
//           <button
//             onClick={handleRewrite}
//             className="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-lg"
//           >
//             Convert to Audiobook Style
//           </button>

//           {rewrittenText && (
//             <textarea
//               value={rewrittenText}
//               readOnly
//               className="w-full h-56 p-3 border rounded-lg"
//             />
//           )}

//           {/* Audio */}
//           <button
//             onClick={handleAudio}
//             className="bg-purple-600 hover:bg-purple-700 text-white px-5 py-2 rounded-lg"
//           >
//             Generate Audio
//           </button>

//           {audioUrl && (
//             <div>
//               <audio controls src={audioUrl} className="w-full" />
//             </div>
//           )}

//           {/* Insights */}
//           <button
//             onClick={handleInsights}
//             className="bg-gray-800 text-white px-5 py-2 rounded-lg"
//           >
//             Show Insights
//           </button>

//           {insights && (
//             <div className="bg-gray-100 p-4 rounded-lg grid grid-cols-2 gap-4">
//               <p>📊 Words: {insights.total_words}</p>
//               <p>🧩 Chunks: {insights.total_chunks}</p>
//               <p>⏱ Time: {insights.estimated_minutes} min</p>
//               <p>
//                 📄 Type: {insights.doc_type} ({insights.confidence}%)
//               </p>
//             </div>
//           )}
//         </div>
//       )}
//     </div>
//   );
// }

import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Upload from "./pages/Upload";
import StudyMode from "./pages/StudyMode";
import ListenerMode from "./pages/ListenerMode";
import Insights from "./pages/Insights";
import StudyInsights from "./pages/StudyInsights";



export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/study" element={<StudyMode />} />
       
        <Route path="/insights" element={<Insights />} />
        <Route path="/study-insights" element={<StudyInsights />} />
      </Routes>
    </BrowserRouter>
  );
}