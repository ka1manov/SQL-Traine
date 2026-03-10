import { useState, useEffect } from 'react';
import { ArrowLeft, Play, Lightbulb, Eye, BookOpen, AlignLeft } from 'lucide-react';
import SQLEditor from '../components/SQLEditor';
import ResultTable from '../components/ResultTable';
import DiffView from '../components/DiffView';
import Badge from '../components/Badge';
import {
  fetchInterviewQuestions, fetchInterviewMeta, fetchInterviewQuestion,
  checkInterviewQuestion, formatSQL,
} from '../utils/api';
import type { InterviewQuestion, InterviewMeta, CheckResponse } from '../types';

export default function InterviewQuestions() {
  const [questions, setQuestions] = useState<InterviewQuestion[]>([]);
  const [meta, setMeta] = useState<InterviewMeta | null>(null);
  const [selected, setSelected] = useState<InterviewQuestion | null>(null);
  const [sql, setSql] = useState('');
  const [result, setResult] = useState<CheckResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [company, setCompany] = useState('');
  const [pattern, setPattern] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [showHint, setShowHint] = useState(false);
  const [showSolution, setShowSolution] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);

  useEffect(() => {
    fetchInterviewMeta().then(setMeta).catch(console.error);
  }, []);

  useEffect(() => {
    fetchInterviewQuestions(
      company || undefined,
      pattern || undefined,
      difficulty || undefined,
    ).then(setQuestions).catch(console.error);
  }, [company, pattern, difficulty]);

  const handleCheck = async () => {
    if (!selected || !sql.trim()) return;
    setLoading(true);
    try {
      const res = await checkInterviewQuestion(selected.id, sql);
      setResult(res);
    } catch (err: any) {
      setResult({ correct: false, match_pct: 0, diff: null, actual: null, expected: null, error: err.message });
    } finally {
      setLoading(false);
    }
  };

  const handleFormat = async () => {
    try { setSql(await formatSQL(sql)); } catch {}
  };

  const selectQuestion = (q: InterviewQuestion) => {
    setSql(''); setResult(null); setShowHint(false); setShowSolution(false); setShowExplanation(false);
    fetchInterviewQuestion(q.id).then(setSelected).catch(() => setSelected(q));
  };

  if (selected) {
    return (
      <div className="p-4 space-y-4 max-w-5xl">
        <button onClick={() => { setSelected(null); setResult(null); setSql(''); setShowHint(false); setShowSolution(false); setShowExplanation(false); }}
          className="flex items-center gap-1 text-sm text-gray-400 hover:text-gray-200">
          <ArrowLeft className="w-4 h-4" /> Back to questions
        </button>

        <div>
          <div className="flex items-center gap-3 mb-2 flex-wrap">
            <h1 className="text-xl font-bold">{selected.title}</h1>
            <Badge text={selected.difficulty} />
            <span className="text-xs px-2 py-0.5 rounded-full bg-accent-blue/10 text-accent-blue">{selected.pattern}</span>
          </div>
          <p className="text-gray-400 dark:text-gray-400 text-gray-600 text-sm">{selected.description}</p>
          <div className="flex items-center gap-2 mt-1 flex-wrap">
            <span className="text-xs text-gray-600">Tables: {selected.tables.join(', ')}</span>
            <span className="text-xs text-gray-600">|</span>
            {selected.company_tags.map(c => (
              <span key={c} className="text-xs px-1.5 py-0.5 rounded bg-dark-surface dark:bg-dark-surface bg-gray-200 text-gray-400 dark:text-gray-400 text-gray-600">{c}</span>
            ))}
          </div>
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

        {result && selected.explanation && (
          <button onClick={() => setShowExplanation(!showExplanation)}
            className="flex items-center gap-1 px-3 py-1.5 text-xs bg-purple-900/20 hover:bg-purple-900/30 border border-purple-800/30 rounded-lg text-purple-400">
            <BookOpen className="w-3.5 h-3.5" /> {showExplanation ? 'Hide' : 'Show'} Explanation
          </button>
        )}
        {showExplanation && selected.explanation && (
          <div className="bg-purple-900/10 border border-purple-800/30 rounded-lg p-3 text-purple-300 text-sm whitespace-pre-line">{selected.explanation}</div>
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
        <div>
          <h1 className="text-xl font-bold">Top 50 Interview Questions</h1>
          <p className="text-sm text-gray-400 dark:text-gray-400 text-gray-600 mt-0.5">
            Curated SQL questions tagged by company and pattern
          </p>
        </div>
      </div>

      <div className="flex gap-3 flex-wrap">
        <select value={company} onChange={e => setCompany(e.target.value)}
          className="px-3 py-1.5 text-xs bg-dark-card dark:bg-dark-card bg-gray-100 border border-dark-border dark:border-dark-border border-gray-300 rounded-lg focus:outline-none focus:border-accent-blue">
          <option value="">All Companies</option>
          {meta && Object.keys(meta.companies).sort().map(c => (
            <option key={c} value={c}>{c} ({meta.companies[c]})</option>
          ))}
        </select>
        <select value={pattern} onChange={e => setPattern(e.target.value)}
          className="px-3 py-1.5 text-xs bg-dark-card dark:bg-dark-card bg-gray-100 border border-dark-border dark:border-dark-border border-gray-300 rounded-lg focus:outline-none focus:border-accent-blue">
          <option value="">All Patterns</option>
          {meta && Object.keys(meta.patterns).sort().map(p => (
            <option key={p} value={p}>{p} ({meta.patterns[p]})</option>
          ))}
        </select>
        <select value={difficulty} onChange={e => setDifficulty(e.target.value)}
          className="px-3 py-1.5 text-xs bg-dark-card dark:bg-dark-card bg-gray-100 border border-dark-border dark:border-dark-border border-gray-300 rounded-lg focus:outline-none focus:border-accent-blue">
          <option value="">All Difficulties</option>
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
          <option value="expert">Expert</option>
        </select>
      </div>

      <div className="grid gap-2">
        {questions.map(q => (
          <button
            key={q.id}
            onClick={() => selectQuestion(q)}
            className="w-full text-left bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-3 hover:border-accent-blue transition-colors"
          >
            <div className="flex items-center gap-2 mb-1 flex-wrap">
              <span className="font-medium text-sm">#{q.id}. {q.title}</span>
              <Badge text={q.difficulty} />
              <span className="text-xs px-2 py-0.5 rounded-full bg-accent-blue/10 text-accent-blue">{q.pattern}</span>
            </div>
            <p className="text-xs text-gray-400 dark:text-gray-400 text-gray-600 mb-1.5 line-clamp-2">{q.description}</p>
            <div className="flex gap-1.5 flex-wrap">
              {q.company_tags.map(c => (
                <span key={c} className="text-xs px-1.5 py-0.5 rounded bg-dark-surface dark:bg-dark-surface bg-gray-200 text-gray-400 dark:text-gray-400 text-gray-600">{c}</span>
              ))}
            </div>
          </button>
        ))}
      </div>

      {questions.length === 0 && <p className="text-gray-500 text-sm">No questions found.</p>}
    </div>
  );
}
