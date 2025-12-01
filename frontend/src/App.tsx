import React, { useState } from "react";
import UploadPage from "./pages/UploadPage";
import ScenePreviewPage from "./pages/ScenePreviewPage";

const App: React.FC = () => {
  const [jobId, setJobId] = useState<string | null>(null);

  return (
    <div className="App">
      {!jobId ? (
        <UploadPage onUploadSuccess={setJobId} />
      ) : (
        <ScenePreviewPage jobId={jobId} />
      )}
    </div>
  );
};

export default App;
