// frontend/src/App.js
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [embedCodes, setEmbedCodes] = useState([]);
  const [error, setError] = useState(null);

  const fetchEmbedCodes = async () => {
    try {
      const response = await axios.get("http://localhost:8000/soundcloud-embed-codes");
      setEmbedCodes(response.data.embed_codes);
      setError(null);
    } catch (error) {
      console.error("Error fetching SoundCloud embed codes:", error);
      setError("Failed to fetch SoundCloud embed codes. Please try again later.");
    }
  };

  return (
    <div className="App">
      <h1>SoundCloud Playlist</h1>
      <button onClick={fetchEmbedCodes}>Fetch SoundCloud Embed Codes</button>
      {error && <p className="error">{error}</p>}
      {embedCodes.length > 0 ? (
        embedCodes.map((embedHtml, index) => (
          <div key={index} className="player" dangerouslySetInnerHTML={{ __html: embedHtml }} />
        ))
      ) : (
        <p>No SoundCloud links found in emails.</p>
      )}
    </div>
  );
}

export default App;
