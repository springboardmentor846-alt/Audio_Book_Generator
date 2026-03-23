import { useLocation } from "react-router-dom";
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

export default function StudyInsights() {
  const { state } = useLocation();

  if (!state) return <p>No data</p>;

  const { totalWords, questions, attempted } = state;

  const confidence = Math.round((attempted / questions) * 100 || 0);

  const barData = [
    { name: "Words", value: totalWords },
    { name: "Questions", value: questions },
    { name: "Attempted", value: attempted },
  ];

  const pieData = [
    { name: "Completed", value: attempted },
    { name: "Remaining", value: questions - attempted },
  ];

  return (
    <div className="min-h-screen bg-[#0f0f1a] text-white p-10">

      <h1 className="text-3xl font-bold mb-8">📊 Study Insights</h1>

      {/* CARDS */}
      <div className="grid md:grid-cols-4 gap-6 mb-10">
        <div className="bg-white/5 p-5 rounded-xl">
          <p>Words</p>
          <h2 className="text-2xl">{totalWords}</h2>
        </div>

        <div className="bg-white/5 p-5 rounded-xl">
          <p>Questions</p>
          <h2 className="text-2xl">{questions}</h2>
        </div>

        <div className="bg-white/5 p-5 rounded-xl">
          <p>Attempted</p>
          <h2 className="text-2xl">{attempted}</h2>
        </div>

        <div className="bg-white/5 p-5 rounded-xl">
          <p>Confidence</p>
          <h2 className="text-2xl text-green-400">{confidence}%</h2>
        </div>
      </div>

      {/* BAR */}
      <div className="bg-white/5 p-6 rounded-xl mb-8">
        <h2 className="mb-4">📊 Activity</h2>

        <ResponsiveContainer width="100%" height={250}>
          <BarChart data={barData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#22c55e" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* PIE */}
      <div className="bg-white/5 p-6 rounded-xl">
        <h2 className="mb-4">🎯 Progress</h2>

        <ResponsiveContainer width="100%" height={250}>
          <PieChart>
            <Pie data={pieData} dataKey="value" outerRadius={90}>
              {pieData.map((_, i) => (
                <Cell key={i} fill={i === 0 ? "#22c55e" : "#ef4444"} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

    </div>
  );
}