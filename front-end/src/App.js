import React, { useState, useRef } from "react";
import "./App.css";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [voiceGender, setVoiceGender] = useState("Female");
  const [audioUrl, setAudioUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [statusMsg, setStatusMsg] = useState("");
  const [textPreview, setTextPreview] = useState("");
  
  const audioRef = useRef(null);
  const [playbackRate, setPlaybackRate] = useState(1);

  const handlePlaybackSpeed = (rate) => {
    setPlaybackRate(rate);
    if (audioRef.current) {
      audioRef.current.playbackRate = rate;
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setError(null);
      setAudioUrl(null);
      setStatusMsg("");
      setTextPreview("");
    }
  };

  const handleGenerate = async () => {
    if (!file) {
      setError("Please upload a file first.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setAudioUrl(null);
    setStatusMsg("Uploading and processing file... This may take a minute.");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("voice_gender", voiceGender);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data" // Browser will correctly set boundary
          }
        }
      );

      setStatusMsg("Audiobook generated successfully!");
      if (response.data.extracted_text) {
          setTextPreview(response.data.extracted_text);
      }
      // Add a cache buster so that if a new audiobook is generated, the audio player updates
      setAudioUrl(`${response.data.audio_url}?t=${new Date().getTime()}`);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || err.message || "An error occurred during generation.");
      setStatusMsg("");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownload = () => {
    if (!audioUrl) return;
    // Approach: fetch the valid URL and create an object URL to enforce download behavior.
    fetch(audioUrl)
      .then(res => res.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "audiobook.mp3";
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
      })
      .catch(err => {
        console.error("Download failed", err);
        // Fallback to opening the URL directly
        window.open(audioUrl, "_blank");
      });
  };

  return (
    <div className="app">
      {/* HEADER */}
      <div className="header">
        <h1 className="animatedTitle">AI Audiobook Generator</h1>
        <p>
          Upload any file, extract text, generate & download AI audio
        </p>
      </div>

      {/* UPLOAD SECTION */}
      <div className="card uploadCard">
        <div className="uploadIcon">☁</div>
        <p>Browse Files or Drag & Drop PDF / DOC / TXT</p>
        <input
          type="file"
          onChange={handleFileChange}
          accept=".pdf,.docx,.txt"
        />
        <small>File size up to 200MB</small>
        {file && <p style={{ color: "#4caf50", marginTop: "10px", fontWeight: "bold" }}>Selected: {file.name}</p>}
      </div>

      {/* TEXT PREVIEW */}
      <div className="card">
        <h3>Extracted Text</h3>
        <div className="textBox" style={{ whiteSpace: "pre-wrap", overflowY: "auto", maxHeight: "200px" }}>
          {textPreview ? textPreview : "The uploaded text will be extracted and processed securely during audiobook generation."}
        </div>
      </div>

      {/* VOICE SETTINGS */}
      <div className="card voiceSettings">
        <h3>Voice Settings</h3>
        
        <label style={{ display: "block", marginBottom: "10px", fontWeight: "bold" }}>Voice Selection</label>
        <div style={{ display: "flex", gap: "20px", justifyContent: "left", marginBottom: "15px" }}>
          <label style={{ display: "flex", alignItems: "center", gap: "5px", cursor: "pointer" }}>
            <input 
              type="radio" 
              name="voiceGender" 
              value="Female" 
              checked={voiceGender === "Female"} 
              onChange={(e) => setVoiceGender(e.target.value)} 
            />
            Female
          </label>
          <label style={{ display: "flex", alignItems: "center", gap: "5px", cursor: "pointer" }}>
            <input 
              type="radio" 
              name="voiceGender" 
              value="Male" 
              checked={voiceGender === "Male"} 
              onChange={(e) => setVoiceGender(e.target.value)} 
            />
            Male
          </label>
        </div>
        
        {/* We can hide previewBtn or make it functional if backend supported it. Currently non-functional.
        <button className="previewBtn">
          ▶ Preview Voice
        </button> */}
      </div>

      {/* GENERATE BUTTON */}
      {error && <div style={{ color: "#ff4d4d", marginBottom: "15px", fontWeight: "bold", textAlign: "center" }}>{error}</div>}
      {statusMsg && <div style={{ color: "#4dabf7", marginBottom: "15px", fontWeight: "bold", textAlign: "center" }}>{statusMsg}</div>}
      
      <button 
        className="generateBtn" 
        onClick={handleGenerate}
        disabled={isLoading || !file}
        style={{ 
          opacity: (isLoading || !file) ? 0.6 : 1, 
          cursor: (isLoading || !file) ? "not-allowed" : "pointer" 
        }}
      >
        {isLoading ? "Generating audiobook..." : "Generate Audiobook"}
      </button>

      {/* AUDIO OUTPUT */}
      <div className="card audioCard">
        <h3>Generated Audio</h3>
        
        <audio 
          controls 
          src={audioUrl || ""} 
          ref={audioRef}
          style={{ width: "100%", marginBottom: "15px" }} 
        />
        
        {audioUrl && (
          <div style={{ marginBottom: "15px", display: "flex", gap: "10px", justifyContent: "center" }}>
            {[0.5, 1, 1.5, 2].map((rate) => (
              <button 
                key={rate}
                onClick={() => handlePlaybackSpeed(rate)} 
                style={{ 
                  padding: "5px 10px", 
                  backgroundColor: playbackRate === rate ? "#4dabf7" : "#2a2d3e", 
                  color: "white", 
                  border: "1px solid #4dabf7", 
                  borderRadius: "5px", 
                  cursor: "pointer",
                  fontWeight: "bold"
                }}
              >
                {rate}x
              </button>
            ))}
          </div>
        )}

        <button 
          className="downloadBtn" 
          onClick={handleDownload}
          disabled={!audioUrl}
          style={{ 
            opacity: !audioUrl ? 0.6 : 1, 
            cursor: !audioUrl ? "not-allowed" : "pointer",
            width: "100%"
          }}
        >
          Download MP3
        </button>
      </div>
    </div>
  );
}

export default App;