import { useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Upload() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { "application/pdf": [".pdf"] },
    maxFiles: 1,
    onDrop: async (files) => {
      if (!files[0]) return;
      setLoading(true);
      setError("");
      const formData = new FormData();
      formData.append("file", files[0]);
      try {
        const res = await axios.post(
          "http://localhost:8000/resume/upload",
          formData,
          { headers: { "Content-Type": "multipart/form-data" } }
        );
        navigate(`/dashboard/${res.data.resume_id}`);
      } catch (err) {
        setError("Upload failed. Make sure the backend is running.");
      } finally {
        setLoading(false);
      }
    }
  });

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-10 w-full max-w-xl">
        <h1 className="text-2xl font-semibold text-gray-800 mb-2">
          AI Resume Analyser
        </h1>
        <p className="text-gray-500 mb-8">
          Upload your PDF resume and AI will score it and match you to jobs.
        </p>
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-colors
            ${isDragActive ? "border-indigo-400 bg-indigo-50" : "border-gray-200 hover:border-indigo-300"}`}
        >
          <input {...getInputProps()} />
          <p className="text-5xl mb-4">📄</p>
          <p className="text-gray-600 font-medium">
            {isDragActive ? "Drop it here!" : "Drag & drop your PDF resume here"}
          </p>
          <p className="text-gray-400 text-sm mt-2">or click to browse files</p>
        </div>
        {loading && (
          <div className="mt-6 flex items-center gap-3 text-indigo-600 font-medium">
            <div className="animate-spin w-5 h-5 border-2 border-indigo-300 border-t-indigo-600 rounded-full"/>
            Analysing your resume with AI...
          </div>
        )}
        {error && <p className="mt-4 text-red-500 text-sm">{error}</p>}
      </div>
    </div>
  );
}