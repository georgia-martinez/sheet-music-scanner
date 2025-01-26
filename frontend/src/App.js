import React, { useState } from 'react';
import axios from 'axios';
import * as Tone from "tone";
import './App.css'

const App = () => {
  const [message, setMessage] = useState("");
  const [lineCount, setLineCount] = useState(null);

  const synth = new Tone.Synth().toDestination();

  const song_json = {
      "bpm": 90,
      "notes": [ { "note": "A4", "duration": "4n", "time": 1}]
  }

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

  function parseJSON(example_json){
    var note = example_json.notes[0].note;
    var duration = example_json.notes[0].duration;
  }



  return (
      <div>
        <h1>Sheet Music Scanner</h1>
        <input type="file" onChange={handleFileUpload} />
        <p>{message}</p>
        <button class="white-key">E</button>
        <button class="white-key">F
          <button class="black-key">F#</button>
        </button>
        <button class="white-key">G
          <button class="black-key">G#</button>
        </button>
        <button class="white-key">A
          <button class="black-key">A#</button>
        </button>
        <button class="white-key" >B</button>
        <button class="white-key">C
          <button class="black-key">C#</button>
        </button>
        <button class="white-key">D
          <button class="black-key">D#</button>
        </button>
        <button class="white-key">E</button>
        {lineCount !== null && <p>Horizontal Lines Detected: {lineCount}</p>}
      </div>
  );
};

export default App;
