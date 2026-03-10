import { useState, useEffect } from 'react';
import { Briefcase, ChevronRight, Play, CheckCircle2, Eye } from 'lucide-react';
import SQLEditor from '../components/SQLEditor';
import ResultTable from '../components/ResultTable';
import DiffView from '../components/DiffView';
import { fetchAssignments, executeSQL, checkTask as checkTaskApi, formatSQL } from '../utils/api';
import type { Assignment, ExecuteResponse, CheckResponse } from '../types';
import { useProgress } from '../hooks/useProgress';

export default function TakeHome() {
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [selected, setSelected] = useState<Assignment | null>(null);
  const [stepIdx, setStepIdx] = useState(0);
  const [sql, setSql] = useState('');
  const [result, setResult] = useState<ExecuteResponse | null>(null);
  const [checkResult, setCheckResult] = useState<CheckResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [showSolution, setShowSolution] = useState(false);
  const [stepsDone, setStepsDone] = useState<Set<number>>(new Set());

  useEffect(() => {
    fetchAssignments().then(setAssignments).catch(console.error);
  }, []);

  const runAndCheck = async () => {
    if (!sql.trim() || !selected) return;
    setLoading(true);
    setCheckResult(null);
    try {
      const res = await executeSQL(sql);
      setResult(res);

      // Auto-check if step has a solution
      const step = selected.steps[stepIdx];
      if (step.solution_sql && !res.error) {
        const expectedRes = await executeSQL(step.solution_sql);
        // Simple comparison
        const actualJson = JSON.stringify(res.rows);
        const expectedJson = JSON.stringify(expectedRes.rows);
        if (actualJson === expectedJson) {
          setStepsDone(prev => new Set(prev).add(stepIdx));
          setCheckResult({ correct: true, match_pct: 100, diff: null, actual: res, expected: expectedRes, error: null });
        } else {
          setCheckResult({ correct: false, match_pct: 0, diff: null, actual: res, expected: expectedRes, error: null });
        }
      }
    } catch (err: any) {
      setResult({ columns: [], rows: [], row_count: 0, error: err.message, execution_time_ms: 0 });
    } finally {
      setLoading(false);
    }
  };

  const handleFormat = async () => {
    try { setSql(await formatSQL(sql)); } catch {}
  };

  if (selected) {
    const step = selected.steps[stepIdx];
    return (
      <div className="p-4 space-y-4 max-w-4xl">
        <button onClick={() => { setSelected(null); setStepIdx(0); setSql(''); setResult(null); setCheckResult(null); setStepsDone(new Set()); }}
          className="text-sm text-gray-400 hover:text-gray-200">← Back to assignments</button>

        <div>
          <h1 className="text-xl font-bold">{selected.title}</h1>
          <p className="text-sm text-gray-400">{selected.company} — Tables: {selected.tables.join(', ')}</p>
        </div>

        <div className="flex gap-2 flex-wrap">
          {selected.steps.map((s, i) => (
            <button key={i} onClick={() => { setStepIdx(i); setSql(''); setResult(null); setCheckResult(null); setShowSolution(false); }}
              className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-medium ${
                stepIdx === i ? 'bg-accent-blue text-white' : 'bg-dark-card border border-dark-border text-gray-400 hover:bg-dark-hover'
              }`}>
              {stepsDone.has(i) && <CheckCircle2 className="w-3 h-3 text-accent-green" />}
              Step {s.step}
            </button>
          ))}
        </div>

        <div className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border rounded-lg p-4">
          <h3 className="font-medium mb-1">{step.title}</h3>
          <p className="text-sm text-gray-400">{step.description}</p>
          <p className="text-xs text-gray-600 mt-2">Hint: {step.hint}</p>
        </div>

        {step.solution_sql && (
          <button onClick={() => setShowSolution(!showSolution)}
            className="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-300">
            <Eye className="w-3.5 h-3.5" /> {showSolution ? 'Hide' : 'Show'} Solution
          </button>
        )}
        {showSolution && step.solution_sql && (
          <div className="bg-dark-card border border-dark-border rounded-lg p-3 font-mono text-sm text-accent-blue">{step.solution_sql}</div>
        )}

        <SQLEditor value={sql} onChange={setSql} onRun={runAndCheck} onFormat={handleFormat} height="160px" />

        <div className="flex gap-2 items-center">
          <button onClick={runAndCheck} disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-accent-blue hover:bg-blue-600 rounded-lg text-sm font-medium text-white disabled:opacity-50">
            <Play className="w-4 h-4" /> {loading ? 'Running...' : 'Run & Check'}
          </button>
          {checkResult?.correct && <span className="text-accent-green text-sm font-medium flex items-center gap-1"><CheckCircle2 className="w-4 h-4" /> Correct!</span>}
          {checkResult && !checkResult.correct && <span className="text-accent-red text-sm">Not quite — check your output</span>}
        </div>

        <ResultTable result={result} maxHeight="300px" />
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4 max-w-3xl">
      <div className="flex items-center gap-2">
        <Briefcase className="w-6 h-6 text-accent-yellow" />
        <h1 className="text-xl font-bold">Take-Home Projects</h1>
      </div>
      <p className="text-sm text-gray-400">Real-world SQL projects inspired by top tech companies.</p>
      <div className="space-y-3">
        {assignments.map(a => (
          <button key={a.id} onClick={() => setSelected(a)}
            className="w-full text-left bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-4 hover:bg-dark-hover transition-colors">
            <div className="flex items-center justify-between">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="font-medium">{a.title}</h3>
                  <span className="text-xs bg-dark-bg dark:bg-dark-bg bg-gray-200 px-2 py-0.5 rounded text-gray-500">{a.company}</span>
                </div>
                <p className="text-sm text-gray-400">{a.description}</p>
                <p className="text-xs text-gray-600 mt-1">{a.steps.length} steps</p>
              </div>
              <ChevronRight className="w-5 h-5 text-gray-600" />
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
