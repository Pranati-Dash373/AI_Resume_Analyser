import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

export default function OptimizedResume() {
  const { resumeId, jobId } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function load() {
      try {
        const res = await axios.get(
          `http://localhost:8000/jobs/optimize/${resumeId}/${jobId}`
        );
        setData(res.data);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setLoading(false);
      }
    }
    load();
  }, [resumeId, jobId]);

  const handleCopy = () => {
    navigator.clipboard.writeText(data.optimized_resume);
    alert("Resume copied to clipboard!");
  };

  const handlePrint = () => {
    window.print();
  };

  const parseResume = (text) => {
    const sections = [];
    let currentSection = null;
    let currentItems = [];

    text.split('\n').forEach(line => {
      line = line.trim();
      if (!line) return;

      const isHeader = ['EXPERIENCE', 'EDUCATION', 'SKILLS', 'PROJECTS',
        'SUMMARY', 'OBJECTIVE', 'CERTIFICATIONS', 'ACHIEVEMENTS',
        'WORK EXPERIENCE', 'TECHNICAL SKILLS', 'INTERNSHIP',
        'INTERNSHIP &TRAINING', 'INTERNSHIP & TRAINING'].some(h =>
          line.toUpperCase().includes(h));

      if (isHeader) {
        if (currentSection) {
          sections.push({ title: currentSection, items: currentItems });
        }
        currentSection = line.replace(':', '');
        currentItems = [];
      } else if (currentSection) {
        currentItems.push(line);
      }
    });

    if (currentSection) {
      sections.push({ title: currentSection, items: currentItems });
    }

    return sections;
  };

  if (loading) return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full mx-auto mb-4"/>
        <p className="text-gray-500 font-medium">AI is optimizing your resume...</p>
        <p className="text-gray-400 text-sm mt-2">This may take 30-60 seconds</p>
      </div>
    </div>
  );

  if (!data) return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <p className="text-red-500">Something went wrong. Please try again.</p>
    </div>
  );

  const lines = data.optimized_resume.split('\n').filter(line => line.trim());
  const name = lines[0] || "Your Name";
  const contact = lines[1] || "";
  const sections = parseResume(data.optimized_resume);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto">

        {/* Top Controls */}
        <div className="print:hidden mb-6 flex items-center justify-between">
          <button
            onClick={() => navigate(-1)}
            className="text-indigo-600 hover:text-indigo-800 font-medium"
          >
            ← Back
          </button>
          <div className="flex gap-3">
            <button
              onClick={handleCopy}
              className="bg-gray-200 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-300"
            >
              📋 Copy Text
            </button>
            <button
              onClick={handlePrint}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700"
            >
              🖨️ Download as PDF
            </button>
          </div>
        </div>

        {/* ATS Score + Info Cards */}
        <div className="print:hidden grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-2xl border border-gray-100 p-5 flex flex-col items-center justify-center">
            <p className={`text-5xl font-bold ${
              data.ats_score >= 75 ? "text-green-600" :
              data.ats_score >= 50 ? "text-amber-500" : "text-red-500"
            }`}>{data.ats_score}</p>
            <p className="text-gray-400 text-sm mt-1">ATS Score</p>
            <div className="w-full bg-gray-100 rounded-full h-2 mt-3">
              <div
                className={`h-2 rounded-full ${
                  data.ats_score >= 75 ? "bg-green-500" :
                  data.ats_score >= 50 ? "bg-amber-400" : "bg-red-400"
                }`}
                style={{ width: `${data.ats_score}%` }}
              />
            </div>
          </div>

          <div className="bg-white rounded-2xl border border-gray-100 p-5">
            <h3 className="font-semibold text-green-700 mb-2">✅ Changes Made</h3>
            <ul className="space-y-1">
              {data.changes_made?.slice(0, 4).map((change, i) => (
                <li key={i} className="text-gray-600 text-xs flex gap-2">
                  <span className="text-green-400">•</span>{change}
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-white rounded-2xl border border-gray-100 p-5">
            <h3 className="font-semibold text-indigo-700 mb-2">🔑 Keywords Added</h3>
            <div className="flex flex-wrap gap-1">
              {data.keywords_added?.map((kw, i) => (
                <span key={i} className="bg-indigo-50 text-indigo-700 text-xs px-2 py-0.5 rounded-full border border-indigo-100">
                  {kw}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Job Target */}
        <div className="print:hidden bg-indigo-50 rounded-2xl border border-indigo-100 p-4 mb-6">
          <p className="text-indigo-800 font-semibold">
            🎯 Optimized for: {data.job_title} at {data.company}
          </p>
        </div>

        {/* RESUME DOCUMENT */}
        <div className="bg-white shadow-lg rounded-2xl overflow-hidden">

          {/* Header - Name centered */}
          <div className="bg-indigo-700 text-white p-8 text-center">
            <h1 className="text-3xl font-bold tracking-wide">{name}</h1>
            {contact && (
              <p className="text-indigo-200 mt-2 text-sm">{contact}</p>
            )}
            <div className="mt-3 flex flex-wrap gap-2 justify-center">
              {data.keywords_added?.map((kw, i) => (
                <span key={i} className="bg-indigo-600 text-indigo-100 text-xs px-2 py-0.5 rounded-full">
                  {kw}
                </span>
              ))}
            </div>
          </div>

          {/* Resume Body - sections only, no duplicate name */}
          <div className="p-8">
            {sections.length > 0 ? (
              sections.map((section, i) => (
                <div key={i} className="mb-5">
                  <h2 className="text-indigo-700 font-bold text-sm uppercase tracking-widest border-b border-indigo-100 pb-1 mb-2">
                    {section.title}
                  </h2>
                  <div className="space-y-1">
                    {section.items.slice(0, 5).map((item, j) => (
                      <p key={j} className={`text-gray-700 text-sm leading-relaxed ${
                        item.startsWith('-') || item.startsWith('•')
                          ? 'pl-4' : ''
                      }`}>
                        {item}
                      </p>
                    ))}
                  </div>
                </div>
              ))
            ) : (
              <div className="whitespace-pre-wrap text-gray-700 text-sm leading-relaxed">
                {data.optimized_resume}
              </div>
            )}
          </div>

        </div>

        {/* Bottom Buttons */}
        <div className="print:hidden mt-6 flex justify-center gap-4">
          <button
            onClick={handleCopy}
            className="bg-gray-200 text-gray-700 px-6 py-3 rounded-xl font-medium hover:bg-gray-300"
          >
            📋 Copy Resume Text
          </button>
          <button
            onClick={handlePrint}
            className="bg-indigo-600 text-white px-6 py-3 rounded-xl font-medium hover:bg-indigo-700"
          >
            🖨️ Download as PDF
          </button>
        </div>

      </div>
    </div>
  );
}