import React from "react";
import UploadForm from "../components/UploadForm";
import { BASE_URL } from "../api/config";

interface UploadPageProps {
  onUploadSuccess: (jobId: string) => void;
}

const UploadPage: React.FC<UploadPageProps> = ({ onUploadSuccess }) => {
  const checkJob = async (jobId: string) => {
    const res = await fetch(`${BASE_URL}/upload/jobs/${jobId}`);
    if (!res.ok) throw new Error("Failed to fetch job status");
    return res.json();
  };

  const handleSubmit = async (text: string, file?: File) => {
    if (!text && !file) {
      alert("Please enter text or select a file to upload.");
      return;
    }

    const formData = new FormData();
    if (file) formData.append("file", file);
    if (text) formData.append("text", text);

    try {
      const res = await fetch(`${BASE_URL}/upload/file`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Upload failed");
      const data = await res.json();
      const jobId = data.job_id;

      // Poll backend until scenes are generated
      let job;
      do {
        await new Promise((r) => setTimeout(r, 2000));
        job = await checkJob(jobId);
        console.log("Job status:", job.status);
      } while (job.status !== "done");

      alert("Scenes generated successfully!");
      onUploadSuccess(jobId);

    } catch (err: any) {
      console.error(err);
      alert(err.message || "Error uploading story");
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Upload Story</h1>
      <UploadForm onSubmit={handleSubmit} />
    </div>
  );
};

export default UploadPage;
