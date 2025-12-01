import React, { useState } from "react";

interface UploadFormProps {
  onSubmit: (textData: string, fileData?: File) => void;
}

const UploadForm: React.FC<UploadFormProps> = ({ onSubmit }) => {
  const [textInput, setTextInput] = useState("");
  const [file, setFile] = useState<File | null>(null);

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setTextInput(e.target.value);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!textInput && !file) {
      alert("Please enter text or select a file to upload.");
      return;
    }
    onSubmit(textInput, file || undefined);
    setTextInput("");
    setFile(null);
  };

  return (
    <form
      className="upload-form flex flex-col space-y-4 p-4 border rounded shadow-md bg-white"
      onSubmit={handleSubmit}
    >
      <label className="font-bold">Enter Text:</label>
      <textarea
        value={textInput}
        onChange={handleTextChange}
        placeholder="Type your story or snippet here..."
        className="border p-2 rounded h-32"
      />

      <label className="font-bold">Or Upload PDF:</label>
      <input
        key={file ? file.name : "empty"}
        type="file"
        accept=".pdf"
        onChange={handleFileChange}
        className="border p-2 rounded"
      />

      <button
        type="submit"
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Submit
      </button>
    </form>
  );
};

export default UploadForm;
