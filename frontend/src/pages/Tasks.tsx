import { useState, useEffect, useContext } from 'react';
import { ArrowLeft, Play, Lightbulb, Eye, Bookmark, BookmarkCheck, AlignLeft } from 'lucide-react';
import SQLEditor from '../components/SQLEditor';
import ResultTable from '../components/ResultTable';
import DiffView from '../components/DiffView';
import TaskCard from '../components/TaskCard';
import TaskFilters from '../components/TaskFilters';
import Badge from '../components/Badge';
import { fetchTasks, checkTask, formatSQL, addBookmark, removeBookmark, fetchBookmarks } from '../utils/api';
import { useProgress } from '../hooks/useProgress';
import { AuthContext } from '../contexts/AuthContext';
import type { Task, CheckResponse } from '../types';

export default function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selected, setSelected] = useState<Task | null>(null);
  const [sql, setSql] = useState('');
  const [result, setResult] = useState<CheckResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [category, setCategory] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [showHint, setShowHint] = useState(false);
  const [showSolution, setShowSolution] = useState(false);
  const [bookmarks, setBookmarks] = useState<Set<number>>(new Set());
  const { isSolved, recordAttempt, getAttempts } = useProgress();
  const auth = useContext(AuthContext);

  useEffect(() => {
    fetchTasks(category || undefined, difficulty || undefined).then(setTasks).catch(console.error);
  }, [category, difficulty]);

  useEffect(() => {
    if (auth?.isLoggedIn) {
      fetchBookmarks().then(bm => setBookmarks(new Set(bm.map(b => b.task_id)))).catch(() => {});
    }
  }, [auth?.isLoggedIn]);

  const categories = [...new Set(tasks.map(t => t.category))];

  const handleCheck = async () => {
    if (!selected || !sql.trim()) return;
    setLoading(true);
    try {
      const res = await checkTask(selected.id, sql);
      setResult(res);
      await recordAttempt(selected.id, res.match_pct, res.correct);
    } catch (err: any) {
      setResult({ correct: false, match_pct: 0, diff: null, actual: null, expected: null, error: err.message });
    } finally {
      setLoading(false);
    }
  };

  const handleFormat = async () => {
    try { setSql(await formatSQL(sql)); } catch {}
  };

  const toggleBookmark = async (taskId: number) => {
    if (bookmarks.has(taskId)) {
      await removeBookmark(taskId);
      setBookmarks(prev => { const n = new Set(prev); n.delete(taskId); return n; });
    } else {
      await addBookmark(taskId);
      setBookmarks(prev => new Set(prev).add(taskId));
    }
  };

  const attempts = selected ? getAttempts(selected.id) : 0;

  if (selected) {
    return (
      <div className="p-4 space-y-4 max-w-5xl">
        <button onClick={() => { setSelected(null); setResult(null); setSql(''); setShowHint(false); setShowSolution(false); }}
          className="flex items-center gap-1 text-sm text-gray-400 hover:text-gray-200">
          <ArrowLeft className="w-4 h-4" /> Back to tasks
        </button>

        <div>
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-xl font-bold">{selected.title}</h1>
            <Badge text={selected.difficulty} />
            {auth?.isLoggedIn && (
              <button onClick={() => toggleBookmark(selected.id)} className="text-gray-400 hover:text-accent-yellow">
                {bookmarks.has(selected.id) ? <BookmarkCheck className="w-5 h-5 text-accent-yellow" /> : <Bookmark className="w-5 h-5" />}
              </button>
            )}
          </div>
          <p className="text-gray-400 dark:text-gray-400 text-gray-600 text-sm">{selected.description}</p>
          <p className="text-xs text-gray-600 mt-1">Tables: {selected.tables.join(', ')} | Attempts: {attempts}</p>
        </div>

        <div className="flex gap-2 flex-wrap">
          {selected.hint && (
            <button onClick={() => setShowHint(!showHint)}
              className="flex items-center gap-1 px-3 py-1.5 text-xs bg-dark-card hover:bg-dark-hover border border-dark-border rounded-lg text-yellow-400">
              <Lightbulb className="w-3.5 h-3.5" /> {showHint ? 'Hide' : 'Show'} Hint
            </button>
          )}
          {selected.solution_sql && (
            <button onClick={() => setShowSolution(!showSolution)}
              className="flex items-center gap-1 px-3 py-1.5 text-xs bg-dark-card hover:bg-dark-hover border border-dark-border rounded-lg text-gray-400">
              <Eye className="w-3.5 h-3.5" /> {showSolution ? 'Hide' : 'Show'} Solution
            </button>
          )}
          <button onClick={handleFormat}
            className="flex items-center gap-1 px-3 py-1.5 text-xs bg-dark-card hover:bg-dark-hover border border-dark-border rounded-lg text-gray-400">
            <AlignLeft className="w-3.5 h-3.5" /> Format
          </button>
        </div>

        {showHint && selected.hint && (
          <div className="bg-yellow-900/10 border border-yellow-800/30 rounded-lg p-3 text-yellow-400 text-sm">{selected.hint}</div>
        )}
        {showSolution && selected.solution_sql && (
          <div className="bg-dark-card border border-dark-border rounded-lg p-3 font-mono text-sm text-accent-blue">{selected.solution_sql}</div>
        )}

        <SQLEditor value={sql} onChange={setSql} onRun={handleCheck} onFormat={handleFormat} height="180px" />

        <button onClick={handleCheck} disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-accent-green hover:bg-green-600 rounded-lg text-sm font-medium text-white transition-colors disabled:opacity-50">
          <Play className="w-4 h-4" /> {loading ? 'Checking...' : 'Check Solution'}
        </button>

        {result && (
          <div className="space-y-3">
            {result.error && (
              <div className="bg-red-900/20 border border-red-800 rounded-lg p-3 text-red-400 text-sm font-mono">{result.error}</div>
            )}
            {result.diff && <DiffView diff={result.diff} />}
            {result.actual && (
              <div>
                <h3 className="text-sm font-medium text-gray-400 mb-1">Your Result</h3>
                <ResultTable result={result.actual} maxHeight="200px" />
              </div>
            )}
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <h1 className="text-xl font-bold">Practice Tasks</h1>
        <TaskFilters categories={categories} selectedCategory={category} selectedDifficulty={difficulty}
          onCategoryChange={setCategory} onDifficultyChange={setDifficulty} />
      </div>
      <div className="grid gap-2">
        {tasks.map(t => (
          <TaskCard key={t.id} task={t} solved={isSolved(t.id)} onClick={() => { setSelected(t); setSql(''); setResult(null); }} />
        ))}
      </div>
      {tasks.length === 0 && <p className="text-gray-500 text-sm">No tasks found.</p>}
    </div>
  );
}
