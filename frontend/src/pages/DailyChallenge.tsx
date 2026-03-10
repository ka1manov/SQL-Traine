import { useState, useEffect } from 'react';
import { Star, Play, Calendar } from 'lucide-react';
import SQLEditor from '../components/SQLEditor';
import DiffView from '../components/DiffView';
import ResultTable from '../components/ResultTable';
import StreakCalendar from '../components/StreakCalendar';
import Badge from '../components/Badge';
import { fetchDaily, checkTask, fetchStreaks, recordStreak, formatSQL } from '../utils/api';
import { useProgress } from '../hooks/useProgress';
import type { Task, CheckResponse, StreakData } from '../types';

export default function DailyChallenge() {
  const [task, setTask] = useState<Task | null>(null);
  const [sql, setSql] = useState('');
  const [result, setResult] = useState<CheckResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [streakData, setStreakData] = useState<StreakData>({ current_streak: 0, best_streak: 0, days: [] });
  const { recordAttempt } = useProgress();

  useEffect(() => {
    fetchDaily().then(setTask).catch(console.error);
    fetchStreaks().then(setStreakData).catch(() => {});
  }, []);

  const handleCheck = async () => {
    if (!task || !sql.trim()) return;
    setLoading(true);
    try {
      const res = await checkTask(task.id, sql);
      setResult(res);
      await recordAttempt(task.id, res.match_pct, res.correct);
      if (res.correct) {
        await recordStreak(task.id);
        fetchStreaks().then(setStreakData).catch(() => {});
      }
    } catch (err: any) {
      setResult({ correct: false, match_pct: 0, diff: null, actual: null, expected: null, error: err.message });
    } finally {
      setLoading(false);
    }
  };

  const handleFormat = async () => {
    try { setSql(await formatSQL(sql)); } catch {}
  };

  if (!task) return <div className="p-4 text-gray-500">Loading daily challenge...</div>;

  return (
    <div className="p-4 space-y-4 max-w-4xl">
      <div className="flex items-center gap-3 flex-wrap">
        <Star className="w-6 h-6 text-accent-yellow" />
        <h1 className="text-xl font-bold">Daily Challenge</h1>
        <div className="flex items-center gap-1 text-xs text-gray-500">
          <Calendar className="w-3.5 h-3.5" />
          {new Date().toLocaleDateString()}
        </div>
      </div>

      <div className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-4">
        <StreakCalendar data={streakData} />
      </div>

      <div className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-4">
        <div className="flex items-center gap-3 mb-2">
          <h2 className="font-semibold">{task.title}</h2>
          <Badge text={task.difficulty} />
        </div>
        <p className="text-gray-400 dark:text-gray-400 text-gray-600 text-sm">{task.description}</p>
        <p className="text-xs text-gray-600 mt-1">Tables: {task.tables.join(', ')}</p>
      </div>

      <SQLEditor value={sql} onChange={setSql} onRun={handleCheck} onFormat={handleFormat} height="180px" />

      <button onClick={handleCheck} disabled={loading}
        className="flex items-center gap-2 px-4 py-2 bg-accent-yellow hover:bg-yellow-600 text-black rounded-lg text-sm font-medium transition-colors disabled:opacity-50">
        <Play className="w-4 h-4" /> {loading ? 'Checking...' : 'Submit'}
      </button>

      {result?.error && (
        <div className="bg-red-900/20 border border-red-800 rounded-lg p-3 text-red-400 text-sm font-mono">{result.error}</div>
      )}
      {result?.diff && <DiffView diff={result.diff} />}
      {result?.actual && <ResultTable result={result.actual} maxHeight="200px" />}
    </div>
  );
}
