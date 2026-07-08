import { BrowserRouter, Routes, Route } from "react-router-dom";
import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";
import OptimizedResume from "./pages/OptimizedResume";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Upload />} />
        <Route path="/dashboard/:resumeId" element={<Dashboard />} />
        <Route path="/optimize/:resumeId/:jobId" element={<OptimizedResume />} />
      </Routes>
    </BrowserRouter>
  );
}