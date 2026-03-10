import { useState, useEffect } from 'react';
import { Trophy, Medal } from 'lucide-react';
import { fetchLeaderboard } from '../utils/api';
import type { LeaderboardEntry } from '../types';

export default function Leaderboard() {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboard()
      .then(setEntries)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const getRankIcon = (idx: number) => {
    if (idx === 0) return <Medal className="w-5 h-5 text-yellow-400" />;
    if (idx === 1) return <Medal className="w-5 h-5 text-gray-300" />;
    if (idx === 2) return <Medal className="w-5 h-5 text-amber-600" />;
    return <span className="w-5 h-5 flex items-center justify-center text-xs text-gray-500 font-medium">{idx + 1}</span>;
  };

  return (
    <div className="p-4 space-y-4 max-w-3xl">
      <div className="flex items-center gap-2">
        <Trophy className="w-6 h-6 text-accent-yellow" />
        <h1 className="text-xl font-bold">Leaderboard</h1>
      </div>
      <p className="text-sm text-gray-400 dark:text-gray-400 text-gray-600">Top performers ranked by tasks solved.</p>

      {loading && <div className="text-gray-500 text-sm">Loading leaderboard...</div>}

      {!loading && entries.length === 0 && (
        <div className="text-gray-500 text-sm">No entries yet. Solve tasks to appear on the leaderboard!</div>
      )}

      {entries.length > 0 && (
        <div className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-dark-border dark:border-dark-border border-gray-200">
                <th className="text-left px-4 py-3 text-gray-500 font-medium w-12">#</th>
                <th className="text-left px-4 py-3 text-gray-500 font-medium">User</th>
                <th className="text-right px-4 py-3 text-gray-500 font-medium">Solved</th>
                <th className="text-right px-4 py-3 text-gray-500 font-medium">Attempts</th>
                <th className="text-right px-4 py-3 text-gray-500 font-medium">Avg Match</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((entry, idx) => (
                <tr key={entry.username}
                  className={`border-b border-dark-border dark:border-dark-border border-gray-100 last:border-0 ${
                    idx < 3 ? 'bg-dark-hover/30 dark:bg-dark-hover/30 bg-yellow-50/30' : ''
                  }`}>
                  <td className="px-4 py-3">{getRankIcon(idx)}</td>
                  <td className="px-4 py-3 font-medium">{entry.username}</td>
                  <td className="px-4 py-3 text-right text-accent-green font-medium">{entry.tasks_solved}</td>
                  <td className="px-4 py-3 text-right text-gray-400">{entry.total_attempts}</td>
                  <td className="px-4 py-3 text-right">
                    <span className={`font-medium ${
                      entry.avg_match_pct >= 80 ? 'text-accent-green' :
                      entry.avg_match_pct >= 50 ? 'text-accent-yellow' : 'text-accent-red'
                    }`}>
                      {Math.round(entry.avg_match_pct)}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
