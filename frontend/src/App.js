import React, { useState } from 'react';
import axios from 'axios';

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

  return (
      <div>
        <h1>React and Flask Integration</h1>
        <input type="file" onChange={handleFileUpload} />
        <p>{message}</p>
      </div>
  );
};

export default App;
