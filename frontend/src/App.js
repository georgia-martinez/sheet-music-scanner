import React, { useState } from 'react';
import axios from 'axios';

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

  return (
      <div>
        <h1>Sheet Music Scanner</h1>
        <input type="file" onChange={handleFileUpload} />
        <p>{message}</p>
        {lineCount !== null && <p>Horizontal Lines Detected: {lineCount}</p>}
      </div>
  );
};

export default App;
