import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="relative min-h-screen text-white overflow-hidden bg-gradient-to-br from-[#0f172a] via-[#1e1b4b] to-[#020617]">

      {/* 🌌 BACKGROUND GLOW BLOBS */}
      <div className="absolute top-[-100px] left-[-100px] w-[400px] h-[400px] bg-purple-600 opacity-30 blur-[120px] rounded-full"></div>
      <div className="absolute bottom-[-100px] right-[-100px] w-[400px] h-[400px] bg-blue-500 opacity-30 blur-[120px] rounded-full"></div>

      {/* 🔝 NAVBAR */}
      <div className="relative z-10 flex justify-between items-center px-12 py-6 backdrop-blur-lg bg-white/5 border-b border-white/10">
        <h1 className="text-2xl font-bold text-purple-400">🎧 AudioAI</h1>

        <div className="flex gap-6 text-gray-300">
          <a href="#">Home</a>
          <a href="#">Features</a>
          <a href="#">About</a>
        </div>

        <Link to="/upload">
          <button className="bg-gradient-to-r from-purple-500 to-blue-500 px-5 py-2 rounded-xl shadow-lg hover:scale-105 transition">
            Get Started
          </button>
        </Link>
      </div>

      {/* 🚀 HERO */}
      <div className="relative z-10 grid md:grid-cols-2 items-center px-12 py-20 gap-10">

        <div>
          <h1 className="text-5xl font-bold leading-tight">
            Turn Anything into <br />
            <span className="bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
              Smart Audio Experience
            </span>
          </h1>

          <p className="text-gray-300 mt-6 text-lg">
            Whether you're a student revising concepts or someone who loves
            listening to stories — AudioAI transforms text into immersive,
            intelligent audio.
          </p>

          <div className="flex gap-4 mt-8">
            <Link to="/listen">
              <button className="bg-purple-600 px-6 py-3 rounded-xl hover:scale-105 transition">
                🎧 Listen Mode
              </button>
            </Link>

            <Link to="/study">
              <button className="border border-white/20 px-6 py-3 rounded-xl hover:bg-white/10 transition">
                🧠 Study Mode
              </button>
            </Link>
          </div>
        </div>

        {/* IMAGE */}
        <div className="relative">
          <img
            src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4"
            className="rounded-2xl shadow-2xl"
          />

          <div className="absolute bottom-4 left-4 bg-white/10 backdrop-blur-lg px-4 py-2 rounded-xl border border-white/10">
            🎧 Now Playing: AI Generated Audio
          </div>
        </div>
      </div>

      {/* 💡 WHAT IS THIS */}
      <div className="relative z-10 px-12 py-20 text-center max-w-4xl mx-auto">
        <h2 className="text-3xl font-bold mb-6">
          What is AudioAI?
        </h2>

        <p className="text-gray-300 text-lg leading-relaxed">
          AudioAI is a next-generation AI platform that transforms written
          content into immersive audio experiences.  
          <br /><br />
          📚 For learners — it simplifies study material, generates summaries,
          and boosts retention.  
          🎧 For listeners — it turns any text into podcasts, stories, or
          audiobooks you can enjoy anywhere.
        </p>
      </div>

      {/* 🎯 FEATURES */}
      <div className="relative z-10 px-12 py-20">
        <h2 className="text-3xl font-bold mb-12 text-center">
          Built for Learning & Listening
        </h2>

        <div className="grid md:grid-cols-3 gap-10">

          {[
            {
              title: "🎧 AI Audio Engine",
              text: "Convert any document into smooth, human-like narration.",
            },
            {
              title: "🧠 Adaptive Study Mode",
              text: "AI tracks your understanding and adjusts difficulty dynamically.",
            },
            {
              title: "🌍 Multi-Language",
              text: "Listen in different languages with automatic translation.",
            },
          ].map((f, i) => (
            <div
              key={i}
              className="bg-white/10 backdrop-blur-lg border border-white/10 p-6 rounded-2xl shadow-lg hover:scale-105 transition"
            >
              <h3 className="text-xl font-semibold text-purple-300 mb-3">
                {f.title}
              </h3>
              <p className="text-gray-300">{f.text}</p>
            </div>
          ))}

        </div>
      </div>

      {/* 🎧 AUDIO CONTENT */}
      <div className="relative z-10 px-12 py-20">
        <h2 className="text-3xl font-bold mb-10 text-center">
          What You Can Explore
        </h2>

        <div className="grid md:grid-cols-3 gap-8">

          {[
            {
              img: "https://images.unsplash.com/photo-1522202176988-66273c2fd55f",
              title: "Study Notes",
            },
            {
              img: "https://images.unsplash.com/photo-1509021436665-8f07dbf5bf1d",
              title: "Stories & Podcasts",
            },
            {
              img: "https://images.unsplash.com/photo-1492724441997-5dc865305da7",
              title: "Books & Articles",
            },
          ].map((item, i) => (
            <div
              key={i}
              className="bg-white/10 backdrop-blur-lg rounded-2xl overflow-hidden border border-white/10 hover:scale-105 transition"
            >
              <img src={item.img} className="h-48 w-full object-cover" />

              <div className="p-4">
                <h3 className="font-semibold">{item.title}</h3>
                <p className="text-gray-300 text-sm">
                  AI-powered immersive audio
                </p>
              </div>
            </div>
          ))}

        </div>
      </div>

      {/* 💬 TESTIMONIALS */}
      <div className="relative z-10 px-12 py-20">
        <h2 className="text-3xl font-bold mb-12 text-center">
          Loved by Learners & Listeners
        </h2>

        <div className="grid md:grid-cols-3 gap-8">

          {[
            {
              name: "Riya (Student)",
              text: "I revise entire subjects while walking. This changed how I study.",
            },
            {
              name: "Aman (Professional)",
              text: "Feels like a personal podcast generator. I use it daily.",
            },
            {
              name: "Neha (Story Lover)",
              text: "I convert blogs into stories and listen before sleeping. Amazing experience.",
            },
          ].map((t, i) => (
            <div
              key={i}
              className="bg-white/10 backdrop-blur-lg p-6 rounded-2xl border border-white/10 shadow-lg"
            >
              <p className="text-gray-200 italic">“{t.text}”</p>
              <h4 className="mt-4 text-purple-300">{t.name}</h4>
            </div>
          ))}

        </div>
      </div>

      {/* 🚀 CTA */}
      <div className="relative z-10 text-center py-20">
        <h2 className="text-4xl font-bold mb-6">
          Experience the Future of Learning
        </h2>

        <Link to="/upload">
          <button className="bg-gradient-to-r from-purple-500 to-blue-500 px-8 py-3 rounded-xl shadow-lg hover:scale-105 transition">
            Start Now 🚀
          </button>
        </Link>
      </div>

      {/* 🧾 FOOTER */}
      <div className="relative z-10 px-12 py-10 border-t border-white/10 bg-white/5 backdrop-blur-lg flex flex-col md:flex-row justify-between">

        <div>
          <h1 className="text-xl text-white font-bold mb-2">🎧 AudioAI</h1>
          <p className="max-w-sm text-gray-300">
            AI-powered platform transforming reading into listening and
            learning experiences.
          </p>
        </div>

        <div className="flex gap-10 mt-6 md:mt-0">

          <div>
            <h4 className="text-white mb-2">Product</h4>
            <p>Features</p>
            <p>Study Mode</p>
            <p>Listen Mode</p>
          </div>

          <div>
            <h4 className="text-white mb-2">Contact</h4>
            <p>Email: contact@audioai.com</p>
            <p>Support: help.audioai.com</p>
          </div>

        </div>

      </div>

    </div>
  );
}