import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";

export default function Dashboard() {
  const { resumeId } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [matches, setMatches] = useState([]);
  const [queryUsed, setQueryUsed] = useState("");
  const [loading, setLoading] = useState(true);

  const [role, setRole] = useState("");
  const [location, setLocation] = useState("India");
  const [jobsLoading, setJobsLoading] = useState(false);
  const [jobsError, setJobsError] = useState("");

  async function loadJobs({ roleOverride, refresh } = {}) {
    setJobsLoading(true);
    setJobsError("");
    try {
      const params = { location };
      if (roleOverride) params.role = roleOverride;
      if (refresh) params.refresh = true;
      const res = await api.get(`/jobs/match/${resumeId}`, { params });
      setMatches(res.data.matches || []);
      setQueryUsed(res.data.query_used || "");
    } catch (err) {
      setJobsError(
        err.response?.data?.detail ||
        "Couldn't load live job listings. Check that RAPIDAPI_KEY is set on the backend."
      );
    } finally {
      setJobsLoading(false);
    }
  }

  useEffect(() => {
    async function load() {
      const [resumeRes] = await Promise.all([
        api.get(`/resume/${resumeId}`),
        loadJobs()
      ]);
      setData(resumeRes.data);
      setLoading(false);
    }
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [resumeId]);

  if (loading) return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin w-10 h-10 border-4 border-indigo-200 border-t-indigo-600 rounded-full mx-auto mb-4"/>
        <p className="text-gray-500">Loading your results...</p>
      </div>
    </div>
  );

  const { score, feedback } = data;
  const scoreColor = score >= 75 ? "text-green-600" : score >= 50 ? "text-amber-500" : "text-red-500";

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">

        <h1 className="text-2xl font-semibold text-gray-800 mb-6">
          Your Resume Report
        </h1>

        {/* Score Card */}
        <div className="bg-white rounded-2xl border border-gray-100 p-6 mb-4 flex items-center gap-6">
          <div className="text-center">
            <p className={`text-6xl font-bold ${scoreColor}`}>{score}</p>
            <p className="text-gray-400 text-sm mt-1">out of 100</p>
          </div>
          <div className="flex-1">
            <div className="w-full bg-gray-100 rounded-full h-4 mb-3">
              <div
                className={`h-4 rounded-full ${score >= 75 ? "bg-green-500" : score >= 50 ? "bg-amber-400" : "bg-red-400"}`}
                style={{ width: `${score}%` }}
              />
            </div>
            <p className="text-gray-600 text-sm leading-relaxed">{feedback.summary}</p>
          </div>
        </div>

        {/* Missing Keywords */}
        {feedback.missing_keywords?.length > 0 && (
          <div className="bg-white rounded-2xl border border-gray-100 p-6 mb-4">
            <h2 className="font-semibold text-gray-700 mb-3">🔍 Missing Keywords</h2>
            <div className="flex flex-wrap gap-2">
              {feedback.missing_keywords.map(kw => (
                <span key={kw} className="bg-red-50 text-red-600 text-sm px-3 py-1 rounded-full border border-red-100">
                  {kw}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Strengths and Suggestions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div className="bg-white rounded-2xl border border-gray-100 p-6">
            <h2 className="font-semibold text-green-700 mb-3">✅ Strengths</h2>
            <ul className="space-y-2">
              {feedback.strengths?.map((s, i) => (
                <li key={i} className="text-gray-600 text-sm flex gap-2">
                  <span className="text-green-400 mt-0.5">•</span>{s}
                </li>
              ))}
            </ul>
          </div>
          <div className="bg-white rounded-2xl border border-gray-100 p-6">
            <h2 className="font-semibold text-amber-700 mb-3">💡 Suggestions</h2>
            <ul className="space-y-2">
              {feedback.suggestions?.map((s, i) => (
                <li key={i} className="text-gray-600 text-sm flex gap-2">
                  <span className="text-amber-400 mt-0.5">•</span>{s}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Job Search Controls */}
        <div className="bg-white rounded-2xl border border-gray-100 p-5 mb-4">
          <h2 className="text-xl font-semibold text-gray-800 mb-3">🎯 Live Job Matches</h2>
          <form
            className="flex flex-wrap gap-3 items-end"
            onSubmit={(e) => {
              e.preventDefault();
              loadJobs({ roleOverride: role, refresh: true });
            }}
          >
            <div className="flex-1 min-w-[180px]">
              <label className="block text-xs text-gray-500 mb-1">Role (optional override)</label>
              <input
                type="text"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                placeholder={queryUsed || "e.g. Backend Developer"}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-400"
              />
            </div>
            <div className="w-40">
              <label className="block text-xs text-gray-500 mb-1">Location</label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-indigo-400"
              />
            </div>
            <button
              type="submit"
              disabled={jobsLoading}
              className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50"
            >
              {jobsLoading ? "Searching..." : "🔍 Search Jobs"}
            </button>
          </form>
          {queryUsed && !jobsLoading && (
            <p className="text