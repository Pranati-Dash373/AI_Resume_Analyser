import { BrowserRouter, Routes, Route } from "react-router-dom";
import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Upload />} />
        <Route path="/dashboard/:resumeId" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}