import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

export default function Dashboard() {
  const { resumeId } = useParams();
  const [data, setData] = useState(null);
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const [resumeRes, matchRes] = await Promise.all([
        axios.get(`http://localhost:8000/resume/${resumeId}`),
        axios.get(`http://localhost:8000/jobs/match/${resumeId}`)
      ]);
      setData(resumeRes.data);
      setMatches(matchRes.data.matches);
      setLoading(false);
    }
    load();
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

        {/* Job Matches */}
        <h2 className="text-xl font-semibold text-gray-800 mb-4">🎯 Top Job Matches</h2>
        {matches.length === 0 ? (
          <div className="bg-white rounded-2xl border border-gray-100 p-6 text-center text-gray-400">
            No jobs in database yet. Run seed_jobs.py to add jobs.
          </div>
        ) : (
          <div className="space-y-3">
            {matches.map((job, i) => (
              <div key={i} className="bg-white rounded-2xl border border-gray-100 p-5">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <p className="font-semibold text-gray-800">{job.title}</p>
                    <p className="text-gray-500 text-sm">{job.company} · {job.location}</p>
                  </div>
                  <div className="text-right">
                    <p className={`text-2xl font-bold ${job.match_score >= 75 ? "text-green-600" : job.match_score >= 50 ? "text-amber-500" : "text-red-400"}`}>
                      {job.match_score}%
                    </p>
                    <p className="text-gray-400 text-xs">match</p>
                  </div>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2 mb-3">
                  <div
                    className={`h-2 rounded-full ${job.match_score >= 75 ? "bg-green-500" : job.match_score >= 50 ? "bg-amber-400" : "bg-red-400"}`}
                    style={{ width: `${job.match_score}%` }}
                  />
                </div>
                <div className="flex flex-wrap gap-2 mb-2">
                  {job.matched_skills?.map(s => (
                    <span key={s} className="bg-green-50 text-green-700 text-xs px-2 py-0.5 rounded-full">{s}</span>
                  ))}
                  {job.missing_skills?.map(s => (
                    <span key={s} className="bg-gray-100 text-gray-400 text-xs px-2 py-0.5 rounded-full line-through">{s}</span>
                  ))}
                </div>
                <p className="text-gray-500 text-sm italic">{job.recommendation}</p>
              </div>
            ))}
          </div>
        )}

      </div>
    </div>
  );
}