import React, { useState } from 'react';
import axios from 'axios';
import * as Tone from "tone";
import './App.css'

const App = () => {
  const [message, setMessage] = useState("");
  const [lineCount, setLineCount] = useState(null);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (!["image/jpeg", "image/png"].includes(file.type)) {
      setMessage("Please upload a JPG or PNG file.");
      return;
    }

    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await axios.post("http://127.0.0.1:5000/process-image", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setMessage("File processed successfully!");
      setLineCount(response.data.horizontal_lines_count);
    } catch (error) {
      console.error("Error uploading file:", error);
      setMessage("Failed to process the file. Please try again.");
    }
  };

  const synth = new Tone.Synth().toDestination();

  const playNoteA = () => {
    synth.triggerAttackRelease("A3", "8n");
  }

  const playNoteB = () => {
    synth.triggerAttackRelease("B3", "8n");
  }

  const playNoteC = () => {
    synth.triggerAttackRelease("C4", "8n");
  }

  const playNoteD = () => {
    synth.triggerAttackRelease("D4", "8n");
  }

  const playNoteE = () => {
    synth.triggerAttackRelease("E4", "8n");
  }

  const playNoteF = () => {
    synth.triggerAttackRelease("F4", "8n");
  }

  const playNoteG = () => {
    synth.triggerAttackRelease("G4", "8n");
  }

  return (
      <div>
        <h1>Sheet Music Scanner</h1>
        <input type="file" onChange={handleFileUpload} />
        <p>{message}</p>
        <button class="white-key" onClick={playNoteA}>A</button>
        <button class="white-key" onClick={playNoteB}>B</button>
        <button class="white-key" onClick={playNoteC}>C</button>
        <button class="white-key" onClick={playNoteD}>D</button>
        <button class="white-key" onClick={playNoteE}>E</button>
        <button class="white-key" onClick={playNoteF}>F</button>
        <button class="white-key" onClick={playNoteG}>G</button>
        {lineCount !== null && <p>Horizontal Lines Detected: {lineCount}</p>}
      </div>
  );
};

export default App;
