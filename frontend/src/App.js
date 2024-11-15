import React, { useState } from 'react';
import axios from 'axios';
import * as Tone from "tone";

const App = () => {
  const [message, setMessage] = useState("");

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await axios.post("http://127.0.0.1:5000/process-image", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setMessage(response.data.message);
    } catch (error) {
      console.error("Error uploading file:", error);
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
        <h1>React and Flask Integration</h1>
        <input type="file" onChange={handleFileUpload} />
        <p>{message}</p>
        <button onClick={playNoteA}>A</button>
        <button onClick={playNoteB}>B</button>
        <button onClick={playNoteC}>C</button>
        <button onClick={playNoteD}>D</button>
        <button onClick={playNoteE}>E</button>
        <button onClick={playNoteF}>F</button>
        <button onClick={playNoteG}>G</button>
      </div>
  );
};

export default App;
