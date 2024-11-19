import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
  const [message, setMessage] = useState("");
  const [uploadedFileName, setUploadedFileName] = useState("");

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload-pdf", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      // Update the message and file name
      setMessage(response.data.message);
      setUploadedFileName(file.name);
    } catch (error) {
      console.error("Error uploading file:", error);
      setMessage("Failed to upload file.");
    }
  };

  return (
      <div>
        <h1>Upload and Download PDF</h1>

        {/* File upload input */}
        <input type="file" accept=".pdf" onChange={handleFileUpload} />
        <p>{message}</p>

        {/* Show download link if file is uploaded */}
        {uploadedFileName && (
            <a
                href={`http://127.0.0.1:5000/get-pdf/${uploadedFileName}`}
                target="_blank"
                rel="noopener noreferrer"
            >
              Download {uploadedFileName}
            </a>
        )}
      </div>
  );
};

export default App;
