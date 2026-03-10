import { useState, useCallback } from 'react';
import { Layers, Play, CheckCircle2, XCircle, AlertTriangle } from 'lucide-react';
import SQLEditor from '../components/SQLEditor';
import Timer from '../components/Timer';
import DiffView from '../components/DiffView';
import ResultTable from '../components/ResultTable';
import Badge from '../components/Badge';
import { startMock, endMock, fetchTask, checkTask, formatSQL } from '../utils/api';
import type { Task, MockSession, MockResult, CheckResponse } from '../types';

export default function MockInterview() {
  const [session, setSession] = useState<MockSession | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [sql, setSql] = useState('');
  const [results, setResults] = useState<{ taskId: number; correct: boolean; match_pct: number }[]>([]);
  const [checkResult, setCheckResult] = useState<CheckResponse | null>(null);
  const [finalResult, setFinalResult] = useState<MockResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [difficulty, setDifficulty] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleStart = async () => {
    setError(null);
    try {
      const sess = await startMock(difficulty || undefined);
      setSession(sess);
      const taskDetails = await Promise.all(sess.task_ids.map(id => fetchTask(id)));
      setTasks(taskDetails);
      setCurrentIdx(0);
      setResults([]);
      setSql('');
      setCheckResult(null);
      setFinalResult(null);
    } catch (err: any) {
      setError(err.message || 'Failed to start mock interview');
    }
  };

  const handleSubmit = async () => {
    const task = tasks[currentIdx];
    if (!task || !sql.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const res = await checkTask(task.id, sql);
      setCheckResult(res);
      setResults(prev => [...prev, { taskId: task.id, correct: res.correct, match_pct: res.match_pct }]);
    } catch (err: any) {
      setError(err.message || 'Failed to check solution');
      setCheckResult({ correct: false, match_pct: 0, diff: null, actual: null, expected: null, error: err.message });
    } finally {
      setLoading(false);
    }
  };

  const handleNext = () => {
    if (currentIdx < tasks.length - 1) {
      setCurrentIdx(currentIdx + 1);
      setSql('');
      setCheckResult(null);
      setError(null);
    } else {
      handleFinish();
    }
  };

  const handleSkip = () => {
    setResults(prev => [...prev, { taskId: tasks[currentIdx].id, correct: false, match_pct: 0 }]);
    handleNext();
  };

  const handleFinish = useCallback(async () => {
    if (!session) return;
    try {
      const res = await endMock(session.session_id, results.map(r => ({
        task_id: r.taskId,
        correct: r.correct,
        match_pct: r.match_pct,
      })));
      setFinalResult(res);
    } catch (err: any) {
      setError(err.message || 'Failed to end mock interview');
    }
  }, [session, results]);

  const handleFormat = async () => {
    try { setSql(await formatSQL(sql)); } catch {}
  };

  if (finalResult) {
    const scoreColor = finalResult.total_score >= 80 ? 'text-accent-green' : finalResult.total_score >= 50 ? 'text-accent-yellow' : 'text-accent-red';
    return (
      <div className="p-4 space-y-4 max-w-2xl mx-auto pt-8">
        <h1 className="text-2xl font-bold text-center">Mock Interview Results</h1>
        <div className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-xl p-6 text-center">
          <div className={`text-5xl font-bold ${scoreColor} mb-2`}>{finalResult.total_score}%</div>
          <p className="text-gray-400 dark:text-gray-400 text-gray-600">Average Score</p>
          <p className="text-lg mt-2">
            {finalResult.tasks_solved}/{finalResult.total_tasks} tasks solved
          </p>
          {finalResult.time_used && (
            <p className="text-sm text-gray-500 mt-1">
              Time used: {Math.floor(finalResult.time_used / 60)}m {finalResult.time_used % 60}s
            </p>
          )}
        </div>
        <div className="space-y-2">
          {results.map((r, i) => {
            const t = tasks.find(t => t.id === r.taskId);
            return (
              <div key={i} className="flex items-center justify-between bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-3">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium">{t?.title || `Task #${r.taskId}`}</span>
                  {t && <Badge text={t.difficulty} />}
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-gray-400">{r.match_pct}%</span>
                  {r.correct
                    ? <CheckCircle2 className="w-4 h-4 text-accent-green" />
                    : <XCircle className="w-4 h-4 text-accent-red" />}
                </div>
              </div>
            );
          })}
        </div>
        <button onClick={() => { setSession(null); setFinalResult(null); setResults([]); }}
          className="w-full py-2 bg-accent-purple hover:bg-purple-600 rounded-lg text-sm font-medium text-white">
          Try Again
        </button>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="p-4 flex flex-col items-center gap-6 pt-16 max-w-md mx-auto">
        <Layers className="w-12 h-12 text-accent-purple" />
        <h1 className="text-2xl font-bold">Mock Interview</h1>
        <p className="text-gray-400 dark:text-gray-400 text-gray-600 text-center">5 random tasks, 30-minute timer. Test your SQL skills under pressure.</p>
        <select value={difficulty} onChange={e => setDifficulty(e.target.value)}
          className="bg-dark-card dark:bg-dark-card bg-white border border-dark-border dark:border-dark-border border-gray-200 rounded-lg px-4 py-2 text-sm">
          <option value="">All Difficulties</option>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
          <option value="expert">Expert</option>
        </select>
        {error && (
          <div className="flex items-center gap-2 text-accent-red text-sm">
            <AlertTriangle className="w-4 h-4" /> {error}
          </div>
        )}
        <button onClick={handleStart}
          className="flex items-center gap-2 px-6 py-3 bg-accent-purple hover:bg-purple-600 rounded-xl text-sm font-medium text-white">
          <Play className="w-4 h-4" /> Start Interview
        </button>
      </div>
    );
  }

  const task = tasks[currentIdx];

  return (
    <div className="p-4 space-y-4 max-w-4xl">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-lg font-bold">Question {currentIdx + 1}/{tasks.length}</h1>
          {task && <Badge text={task.difficulty} />}
          <div className="flex gap-1">
            {tasks.map((_, i) => (
              <div key={i} className={`w-2 h-2 rounded-full ${
                i < results.length ? (results[i]?.correct ? 'bg-accent-green' : 'bg-accent-red') :
                i === currentIdx ? 'bg-accent-purple' : 'bg-gray-600'
              }`} />
            ))}
          </div>
        </div>
        <Timer seconds={session.time_limit} onExpire={handleFinish} />
      </div>

      {task && (
        <>
          <div className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-4">
            <h2 className="font-semibold mb-1">{task.title}</h2>
            <p className="text-gray-400 dark:text-gray-400 text-gray-600 text-sm">{task.description}</p>
            <p className="text-xs text-gray-600 dark:text-gray-600 text-gray-500 mt-1">Tables: {task.tables.join(', ')}</p>
          </div>

          <SQLEditor value={sql} onChange={setSql} onRun={handleSubmit} onFormat={handleFormat} height="180px" />

          {error && (
            <div className="bg-red-900/20 dark:bg-red-900/20 bg-red-50 border border-red-800 dark:border-red-800 border-red-200 rounded-lg p-3 text-red-400 dark:text-red-400 text-red-600 text-sm">
              {error}
            </div>
          )}

          <div className="flex gap-2">
            <button onClick={handleSubmit} disabled={loading || !!checkResult}
              className="flex items-center gap-2 px-4 py-2 bg-accent-green hover:bg-green-600 rounded-lg text-sm font-medium text-white disabled:opacity-50">
              <Play className="w-4 h-4" /> {loading ? 'Checking...' : 'Submit'}
            </button>
            {!checkResult && (
              <button onClick={handleSkip}
                className="px-4 py-2 bg-dark-card dark:bg-dark-card bg-gray-100 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg text-sm text-gray-400 hover:bg-dark-hover">
                Skip
              </button>
            )}
            {checkResult && (
              <button onClick={handleNext}
                className="px-4 py-2 bg-accent-blue hover:bg-blue-600 rounded-lg text-sm font-medium text-white">
                {currentIdx < tasks.length - 1 ? 'Next Question' : 'Finish'}
              </button>
            )}
          </div>

          {checkResult && (
            <div className="flex items-center gap-2 text-sm">
              {checkResult.correct
                ? <><CheckCircle2 className="w-4 h-4 text-accent-green" /> <span className="text-accent-green font-medium">Correct! {checkResult.match_pct}% match</span></>
                : <><XCircle className="w-4 h-4 text-accent-red" /> <span className="text-accent-red">Not quite — {checkResult.match_pct}% match</span></>}
            </div>
          )}

          {checkResult?.diff && <DiffView diff={checkResult.diff} />}
          {checkResult?.actual && <ResultTable result={checkResult.actual} maxHeight="200px" />}
        </>
      )}
    </div>
  );
}
