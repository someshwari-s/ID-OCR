import React, { useState } from "react";
import AadharCardUploader from "./AadharCardUploader";
import PanCardUploader from "./PanCardUploader";
import "./App.css"; // Import CSS for styling

const App = () => {
  const [showAadharCardUploader, setShowAadharCardUploader] = useState(false);
  const [showPanCardUploader, setShowPanCardUploader] = useState(false);

  const handleAadharCardClick = () => {
    setShowAadharCardUploader(true);
    setShowPanCardUploader(false);
  };

  const handlePanCardClick = () => {
    setShowPanCardUploader(true);
    setShowAadharCardUploader(false);
  };

  const handleBackButtonClick = () => {
    setShowAadharCardUploader(false);
    setShowPanCardUploader(false);
  };

  return (
    <div className="container">
      <h1>OCR Recognition</h1>
      {!showAadharCardUploader && !showPanCardUploader && (
        <>
          <p>Please select the type of card you want to upload:</p>
          <button className="button-primary" onClick={handleAadharCardClick}>
            Upload Aadhar Card
          </button>
          <button className="button-primary" onClick={handlePanCardClick}>
            Upload Pan Card
          </button>
        </>
      )}

      {showAadharCardUploader && (
        <>
          <button className="button-back" onClick={handleBackButtonClick}>
            Back
          </button>
          <AadharCardUploader />
        </>
      )}

      {showPanCardUploader && (
        <>
          <button className="button-back" onClick={handleBackButtonClick}>
            Back
          </button>
          <PanCardUploader />
        </>
      )}
    </div>
  );
};

export default App;
