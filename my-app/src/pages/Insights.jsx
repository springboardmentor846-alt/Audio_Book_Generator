import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

export default function Insights() {
  const { state } = useLocation();
  const navigate = useNavigate();

  const data = state;

  if (!data) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-[#0b0b14] text-white">
        <h2 className="text-2xl mb-4">No insights found</h2>
        <button
          onClick={() => navigate("/upload")}
          className="bg-purple-600 px-6 py-2 rounded-lg"
        >
          Go Back
        </button>
      </div>
    );
  }

  // ================= SMART CALCULATIONS =================

  const words = data.total_words;
  const chunks = data.total_chunks;

  const readingSpeed = 200; // wpm
  const listeningSpeed = 160; // wpm

  const readingTime = Math.ceil(words / readingSpeed);
  const listeningTime = Math.ceil(words / listeningSpeed);

  const timeSaved = readingTime - listeningTime;

  const efficiency = Math.round(
    (readingTime / listeningTime) * 100
  );

  // Difficulty Logic
  let difficulty = "Easy";
  if (words > 2000 || chunks > 15) difficulty = "Medium";
  if (words > 5000 || chunks > 30) difficulty = "Hard";

  // Mode Recommendation
  const recommendedMode =
    difficulty === "Hard" ? "🧠 Study Mode" : "🎧 Listener Mode";

  // ================= CHART DATA =================

  const barData = [
    { name: "Reading", value: readingTime },
    { name: "Listening", value: listeningTime },
  ];

  const pieData = [
    { name: "Content", value: words },
    { name: "Chunks", value: chunks },
  ];

  const COLORS = ["#8b5cf6", "#3b82f6"];

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0f0f1a] via-[#141423] to-[#0b0b14] text-white px-6 py-10">

      {/* HEADER */}
      <h1 className="text-3xl font-bold mb-2">📊 Smart Insights Dashboard</h1>
      <p className="text-gray-400 mb-10">
        AI-powered analysis of your content & audio efficiency
      </p>

      {/* ================= METRICS ================= */}
      <div className="grid md:grid-cols-4 gap-6 mb-10">

        <div className="bg-white/5 p-5 rounded-xl">
          <p className="text-gray-400 text-sm">Total Words</p>
          <h2 className="text-2xl font-bold">{words}</h2>
        </div>

        <div className="bg-white/5 p-5 rounded-xl">
          <p className="text-gray-400 text-sm">Chunks</p>
          <h2 className="text-2xl font-bold">{chunks}</h2>
        </div>

        <div className="bg-white/5 p-5 rounded-xl">
          <p className="text-gray-400 text-sm">Listening Time</p>
          <h2 className="text-2xl font-bold">{listeningTime} min</h2>
        </div>

        <div className="bg-white/5 p-5 rounded-xl">
          <p className="text-gray-400 text-sm">Efficiency</p>
          <h2 className="text-2xl font-bold text-purple-400">
            {efficiency}%
          </h2>
        </div>

      </div>

      {/* ================= SMART INSIGHTS ================= */}
      <div className="grid md:grid-cols-3 gap-6 mb-10">

        <div className="bg-gradient-to-r from-purple-600/20 to-blue-600/20 p-5 rounded-xl">
          <h3 className="font-semibold mb-2">⏱ Time Saved</h3>
          <p className="text-gray-300">
            Reading: {readingTime} min <br />
            Listening: {listeningTime} min <br />
            <span className="text-purple-400 font-semibold">
              You save ~{Math.abs(timeSaved)} min
            </span>
          </p>
        </div>

        <div className="bg-gradient-to-r from-purple-600/20 to-blue-600/20 p-5 rounded-xl">
          <h3 className="font-semibold mb-2">🧠 Difficulty</h3>
          <p className="text-gray-300">
            This content is{" "}
            <span className="text-purple-400 font-semibold">
              {difficulty}
            </span>
          </p>
        </div>

        <div className="bg-gradient-to-r from-purple-600/20 to-blue-600/20 p-5 rounded-xl">
          <h3 className="font-semibold mb-2">🎯 Recommendation</h3>
          <p className="text-gray-300">
            Best suited for{" "}
            <span className="text-purple-400 font-semibold">
              {recommendedMode}
            </span>
          </p>
        </div>

      </div>

      {/* ================= CHARTS ================= */}
      <div className="grid md:grid-cols-2 gap-8">

        {/* TIME COMPARISON */}
        <div className="bg-white/5 p-6 rounded-2xl">
          <h2 className="mb-4 font-semibold">⏱ Reading vs Listening</h2>

          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={barData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#22c55e" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* CONTENT SPLIT */}
        <div className="bg-white/5 p-6 rounded-2xl">
          <h2 className="mb-4 font-semibold">📊 Content Structure</h2>

          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={pieData} dataKey="value" outerRadius={90} label>
                {pieData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

      </div>

      {/* ================= AI SUMMARY ================= */}
      <div className="bg-gradient-to-r from-purple-600/20 to-blue-600/20 p-6 rounded-xl mt-10">
        <h2 className="font-semibold mb-2">🧠 AI Summary</h2>

        <p className="text-gray-300">
          This {difficulty.toLowerCase()}-level document contains{" "}
          <span className="text-purple-400 font-semibold">
            {words} words
          </span>{" "}
          and is best consumed via{" "}
          <span className="text-purple-400 font-semibold">
            {recommendedMode}
          </span>.
          Listening reduces effort and allows passive learning,
          especially for longer content.
        </p>
      </div>

    </div>
  );
}