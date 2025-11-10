import logo from './images.png';
import './App.css';
import React, { useState } from 'react';

function App() {
  const [file, setFile] = useState(null);
  const [outputUrl, setOutputUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setOutputUrl(null);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const droppedFile = event.dataTransfer.files[0];
    if (droppedFile) {
      setFile(droppedFile);
      setOutputUrl(null);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleStandardize = async (anonymous = false) => {
    if (!file) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('anonymous', anonymous);

    try {
      const res = await fetch('http://localhost:8000/api/cv/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setOutputUrl(data.output_pdf);
    } catch (err) {
      console.error("Erreur lors de l'envoi :", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <br/>
        <p>Bienvenue sur l'application de standardisation de CV</p>
      </header>

      <main>
        <input
          type="file"
          accept=".pdf,.docx,.jpg,.jpeg,.png"
          onChange={handleFileChange}
        />

        <div
  onDrop={handleDrop}
  onDragOver={handleDragOver}
  style={{
    border: '2px dashed #888',
    borderRadius: '8px',
    padding: '40px',
    marginTop: '20px',
    backgroundColor: '#BBDFE6',
    textAlign: 'center',
    minHeight: '25px',
    maxWidth: '300px',
    width: '100%',
    marginLeft: 'auto',
    marginRight: 'auto'
  }}
>
  {file ? file.name : 'Votre CV ici'}
</div>
  <br/>
        <div style={{ marginTop: "20px" }}>
          <button
            onClick={() => handleStandardize(false)}
            disabled={!file || isLoading}
          >
            Standardiser
          </button>

          <button
            onClick={() => handleStandardize(true)}
            disabled={!file || isLoading}
            style={{ marginLeft: "10px" }}
          >
            Standardiser de manière anonyme
          </button>
        </div>

        {isLoading && <p>Standardisation en cours...</p>}

        {outputUrl && (
          <a href={outputUrl} target="_blank" rel="noopener noreferrer" download>
            <br/>
            Visionner votre CV standardisé
          </a>
        )}
      </main>
    </div>
  );
}

export default App;