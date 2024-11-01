// frontend/src/App.js
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [links, setLinks] = useState([]);
  const [error, setError] = useState(null);

  const fetchLinks = async () => {
    try {
      const response = await axios.get("http://localhost:8000/soundcloud-links");
      setLinks(response.data);
      setError(null);
    } catch (error) {
      console.error("Error fetching SoundCloud links:", error);
      setError("Failed to fetch SoundCloud links. Please try again later.");
    }
  };

  return (
    <div className="App">
      <h1>SoundCloud Playlist</h1>
      <button onClick={fetchLinks}>Fetch SoundCloud Links</button>
      {error && <p className="error">{error}</p>}
      {links.length > 0 ? (
        links.map((link, index) => (
          <div key={index} className="player">
            <iframe
              width="100%"
              height="450"
              scrolling="no"
              frameBorder="no"
              allow="autoplay"
              src={link}
            ></iframe>
            <div style={{ fontSize: "10px", color: "#cccccc", lineBreak: "anywhere", wordBreak: "normal", overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis", fontFamily: "Interstate,Lucida Grande,Lucida Sans Unicode,Lucida Sans,Garuda,Verdana,Tahoma,sans-serif", fontWeight: "100" }}>
              <a href="https://soundcloud.com/zeinramadan" title="Zein" target="_blank" style={{ color: "#cccccc", textDecoration: "none" }}>Zein</a> · 
              <a href="https://soundcloud.com/zeinramadan/sets/demos/s-IXwayE1EYEL" title="Demos" target="_blank" style={{ color: "#cccccc", textDecoration: "none" }}>Demos</a>
            </div>
          </div>
        ))
      ) : (
        <p>No SoundCloud links found in emails.</p>
      )}
    </div>
  );
}

export default App;
