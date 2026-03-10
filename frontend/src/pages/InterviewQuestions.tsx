import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Play, Lightbulb, Eye, BookOpen, AlignLeft, CheckCircle, ChevronLeft, ChevronRight, Search, Table2, X } from 'lucide-react';
import SQLEditor from '../components/SQLEditor';
import ResultTable from '../components/ResultTable';
import DiffView from '../components/DiffView';
import Badge from '../components/Badge';
import useLocalStorage from '../hooks/useLocalStorage';
import {
  fetchInterviewQuestions, fetchInterviewMeta, fetchInterviewQuestion,
  checkInterviewQuestion, formatSQL, fetchTableSchema,
} from '../utils/api';
import type { InterviewQuestion, InterviewMeta, CheckResponse, ColumnInfo } from '../types';

export default function InterviewQuestions() {
  const navigate = useNavigate();
  const [questions, setQuestions] = useState<InterviewQuestion[]>([]);
  const [meta, setMeta] = useState<InterviewMeta | null>(null);
  const [selected, setSelected] = useState<InterviewQuestion | null>(null);
  const [sql, setSql] = useState('');
  const [result, setResult] = useState<CheckResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [company, setCompany] = useState('');
  const [pattern, setPattern] = useState('');
  const [difficulty, setDifficulty] = useState('');
  const [search, setSearch] = useState('');
  const [showHint, setShowHint] = useState(false);
  const [showSolution, setShowSolution] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);
  const [showSchema, setShowSchema] = useState(false);
  const [schemas, setSchemas] = useState<Record<string, ColumnInfo[]>>({});
  const [schemaLoading, setSchemaLoading] = useState(false);
  const [solvedIds, setSolvedIds] = useLocalStorage<number[]>('interview-solved', []);
  const [viewTransition, setViewTransition] = useState(false);

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

  const filtered = questions.filter(q =>
    !search || q.title.toLowerCase().includes(search.toLowerCase()) ||
    q.description.toLowerCase().includes(search.toLowerCase())
  );

  const filtersActive = !!(company || pattern || difficulty || search);

  const clearFilters = () => {
    setCompany(''); setPattern(''); setDifficulty(''); setSearch('');
  };

  const handleCheck = async () => {
    if (!selected || !sql.trim()) return;
    setLoading(true);
    try {
      const res = await checkInterviewQuestion(selected.id, sql);
      setResult(res);
      if (res.correct && !solvedIds.includes(selected.id)) {
        setSolvedIds(prev => [...prev, selected.id]);
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

  const selectQuestion = useCallback((q: InterviewQuestion) => {
    setViewTransition(true);
    setTimeout(() => {
      setSql(''); setResult(null); setShowHint(false); setShowSolution(false); setShowExplanation(false);
      setShowSchema(false); setSchemas({});
      fetchInterviewQuestion(q.id).then(setSelected).catch(() => setSelected(q));
      setTimeout(() => setViewTransition(false), 50);
    }, 150);
  }, []);

  const goBack = useCallback(() => {
    setViewTransition(true);
    setTimeout(() => {
      setSelected(null); setResult(null); setSql(''); setShowHint(false); setShowSolution(false); setShowExplanation(false);
      setShowSchema(false); setSchemas({});
      setTimeout(() => setViewTransition(false), 50);
    }, 150);
  }, []);

  const handleCompanyClick = (c: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setCompany(c);
    if (selected) goBack();
  };

  const loadSchemas = async () => {
    if (!selected) return;
    if (showSchema) { setShowSchema(false); return; }
    setSchemaLoading(true);
    try {
      const results = await Promise.all(selected.tables.map(t => fetchTableSchema(t)));
      const map: Record<string, ColumnInfo[]> = {};
      selected.tables.forEach((t, i) => { map[t] = results[i]; });
      setSchemas(map);
      setShowSchema(true);
    } catch (err) {
      console.error('Failed to load schemas', err);
    } finally {
      setSchemaLoading(false);
    }
  };

  // Prev/Next navigation
  const currentIndex = selected ? filtered.findIndex(q => q.id === selected.id) : -1;
  const hasPrev = currentIndex > 0;
  const hasNext = currentIndex >= 0 && currentIndex < filtered.length - 1;

  const goPrev = () => { if (hasPrev) selectQuestion(filtered[currentIndex - 1]); };
  const goNext = () => { if (hasNext) selectQuestion(filtered[currentIndex + 1]); };

  // Keyboard shortcuts
  useEffect(() => {
    if (!selected) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        goBack();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [selected, goBack]);

  const solvedCount = solvedIds.length;

  if (selected) {
    return (
      <div className={`p-4 space-y-4 max-w-5xl transition-opacity duration-200 ${viewTransition ? 'opacity-0' : 'opacity-100'}`}>
        <div className="flex items-center justify-between flex-wrap gap-2">
          <button onClick={goBack}
            className="flex items-center gap-1 text-sm text-gray-400 hover:text-gray-200 dark:text-gray-400 dark:hover:text-gray-200 hover:text-gray-800">
            <ArrowLeft className="w-4 h-4" /> Back to questions
          </button>
          <div className="flex items-center gap-2">
            <button onClick={goPrev} disabled={!hasPrev}
              className="flex items-center gap-1 px-2 py-1 text-xs rounded-lg border border-dark-border dark:border-dark-border border-gray-300 text-gray-400 hover:text-gray-200 dark:hover:text-gray-200 hover:text-gray-800 disabled:opacity-30 disabled:cursor-not-allowed transition-colors">
              <ChevronLeft className="w-3.5 h-3.5" /> Prev
            </button>
            <button onClick={goNext} disabled={!hasNext}
              className="flex items-center gap-1 px-2 py-1 text-xs rounded-lg border border-dark-border dark:border-dark-border border-gray-300 text-gray-400 hover:text-gray-200 dark:hover:text-gray-200 hover:text-gray-800 disabled:opacity-30 disabled:cursor-not-allowed transition-colors">
              Next <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <div>
          <div className="flex items-center gap-3 mb-2 flex-wrap">
            <h1 className="text-xl font-bold">{selected.title}</h1>
            <Badge text={selected.difficulty} />
            <span className="text-xs px-2 py-0.5 rounded-full bg-accent-blue/10 text-accent-blue">{selected.pattern}</span>
            {solvedIds.includes(selected.id) && (
              <span className="flex items-center gap-1 text-xs text-accent-green"><CheckCircle className="w-3.5 h-3.5" /> Solved</span>
            )}
          </div>
          <p className="text-gray-400 dark:text-gray-400 text-gray-600 text-sm">{selected.description}</p>
          <div className="flex items-center gap-2 mt-1 flex-wrap">
            <span className="text-xs text-gray-600 dark:text-gray-600 text-gray-500">Tables: {selected.tables.join(', ')}</span>
            <span className="text-xs text-gray-600">|</span>
            {selected.company_tags.map(c => (
              <button key={c} onClick={(e) => handleCompanyClick(c, e)}
                className="text-xs px-1.5 py-0.5 rounded bg-dark-surface dark:bg-dark-surface bg-gray-200 text-gray-400 dark:text-gray-400 text-gray-600 hover:bg-accent-blue/20 hover:text-accent-blue transition-colors cursor-pointer">
                {c}
              </button>
            ))}
          </div>
        </div>

        <div className="flex gap-2 flex-wrap">
          {selected.hint && (
            <button onClick={() => setShowHint(!showHint)}
              className="flex items-center gap-1 px-3 py-1.5 text-xs bg-dark-card dark:bg-dark-card bg-gray-100 hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-200 border border-dark-border dark:border-dark-border border-gray-300 rounded-lg text-yellow-400 dark:text-yellow-400 text-yellow-600">
              <Lightbulb className="w-3.5 h-3.5" /> {showHint ? 'Hide' : 'Show'} Hint
            </button>
          )}
          {selected.solution_sql && (
            <button onClick={() => setShowSolution(!showSolution)}
              className="flex items-center gap-1 px-3 py-1.5 text-xs bg-dark-card dark:bg-dark-card bg-gray-100 hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-200 border border-dark-border dark:border-dark-border border-gray-300 rounded-lg text-gray-400">
              <Eye className="w-3.5 h-3.5" /> {showSolution ? 'Hide' : 'Show'} Solution
            </button>
          )}
          <button onClick={loadSchemas} disabled={schemaLoading}
            className="flex items-center gap-1 px-3 py-1.5 text-xs bg-dark-card dark:bg-dark-card bg-gray-100 hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-200 border border-dark-border dark:border-dark-border border-gray-300 rounded-lg text-accent-blue disabled:opacity-50">
            <Table2 className="w-3.5 h-3.5" /> {schemaLoading ? 'Loading...' : showSchema ? 'Hide Schema' : 'Show Schema'}
          </button>
          <button onClick={handleFormat}
            className="flex items-center gap-1 px-3 py-1.5 text-xs bg-dark-card dark:bg-dark-card bg-gray-100 hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-200 border border-dark-border dark:border-dark-border border-gray-300 rounded-lg text-gray-400">
            <AlignLeft className="w-3.5 h-3.5" /> Format
          </button>
          <button onClick={() => navigate('/patterns')}
            className="flex items-center gap-1 px-3 py-1.5 text-xs rounded-full bg-accent-blue/10 text-accent-blue hover:bg-accent-blue/20 transition-colors">
            View {selected.pattern} pattern &rarr;
          </button>
        </div>

        {showHint && selected.hint && (
          <div className="bg-yellow-900/10 dark:bg-yellow-900/10 bg-yellow-50 border border-yellow-800/30 dark:border-yellow-800/30 border-yellow-300 rounded-lg p-3 text-yellow-400 dark:text-yellow-400 text-yellow-700 text-sm">{selected.hint}</div>
        )}
        {showSolution && selected.solution_sql && (
          <div className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-3 font-mono text-sm text-accent-blue">{selected.solution_sql}</div>
        )}

        {showSchema && Object.keys(schemas).length > 0 && (
          <div className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-3 space-y-3">
            <h3 className="text-sm font-medium text-gray-300 dark:text-gray-300 text-gray-700">Table Schemas</h3>
            {Object.entries(schemas).map(([table, cols]) => (
              <div key={table}>
                <h4 className="text-xs font-mono font-bold text-accent-blue mb-1">{table}</h4>
                <div className="overflow-x-auto">
                  <table className="w-full text-xs">
                    <thead>
                      <tr className="text-left text-gray-500">
                        <th className="pr-4 py-0.5 font-medium">Column</th>
                        <th className="pr-4 py-0.5 font-medium">Type</th>
                        <th className="pr-4 py-0.5 font-medium">Nullable</th>
                        <th className="py-0.5 font-medium">FK</th>
                      </tr>
                    </thead>
                    <tbody>
                      {cols.map(col => (
                        <tr key={col.name} className="border-t border-dark-border/30 dark:border-dark-border/30 border-gray-200">
                          <td className="pr-4 py-0.5 font-mono text-gray-300 dark:text-gray-300 text-gray-700">{col.name}</td>
                          <td className="pr-4 py-0.5 text-gray-400 dark:text-gray-400 text-gray-500">{col.type}</td>
                          <td className="pr-4 py-0.5 text-gray-500">{col.nullable ? 'YES' : 'NO'}</td>
                          <td className="py-0.5 text-accent-blue">{col.fk || ''}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ))}
          </div>
        )}

        {result && selected.explanation && (
          <button onClick={() => setShowExplanation(!showExplanation)}
            className="flex items-center gap-1 px-3 py-1.5 text-xs bg-purple-900/20 hover:bg-purple-900/30 border border-purple-800/30 rounded-lg text-purple-400">
            <BookOpen className="w-3.5 h-3.5" /> {showExplanation ? 'Hide' : 'Show'} Explanation
          </button>
        )}
        {showExplanation && selected.explanation && (
          <div className="bg-purple-900/10 border border-purple-800/30 rounded-lg p-3 text-purple-300 dark:text-purple-300 text-purple-700 text-sm whitespace-pre-line">{selected.explanation}</div>
        )}

        <SQLEditor value={sql} onChange={setSql} onRun={handleCheck} onFormat={handleFormat} height="180px" />

        <button onClick={handleCheck} disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-accent-green hover:bg-green-600 rounded-lg text-sm font-medium text-white transition-colors disabled:opacity-50">
          <Play className="w-4 h-4" /> {loading ? 'Checking...' : 'Check Solution'}
        </button>

        {result && (
          <div className="space-y-3">
            {result.correct && (
              <div className="flex items-center gap-2 bg-green-900/20 dark:bg-green-900/20 bg-green-50 border border-green-500/50 dark:border-green-500/50 border-green-400 rounded-lg p-3 text-accent-green animate-[slideIn_0.3s_ease-out]"
                style={{ animation: 'slideIn 0.3s ease-out' }}>
                <CheckCircle className="w-5 h-5 shrink-0" />
                <span className="text-sm font-medium">Correct! {result.match_pct}% match</span>
              </div>
            )}
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

        <style>{`
          @keyframes slideIn {
            from { opacity: 0; transform: translateY(-8px); }
            to { opacity: 1; transform: translateY(0); }
          }
        `}</style>
      </div>
    );
  }

  return (
    <div className={`p-4 space-y-4 transition-opacity duration-200 ${viewTransition ? 'opacity-0' : 'opacity-100'}`}>
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div>
          <h1 className="text-xl font-bold">Top 50 Interview Questions</h1>
          <p className="text-sm text-gray-400 dark:text-gray-400 text-gray-600 mt-0.5">
            Curated SQL questions tagged by company and pattern
            {solvedCount > 0 && (
              <span className="ml-2 text-accent-green">&middot; {solvedCount}/{meta?.total ?? 50} completed</span>
            )}
          </p>
        </div>
        {filtersActive && (
          <span className="text-xs text-gray-400">
            Showing {filtered.length} of {meta?.total ?? questions.length}
          </span>
        )}
      </div>

      <div className="sticky top-0 z-10 bg-white dark:bg-dark-bg pb-3 pt-1 border-b border-transparent dark:border-transparent"
        style={{ backdropFilter: 'blur(8px)' }}>
        <div className="flex gap-3 flex-wrap items-center">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-500 pointer-events-none" />
            <input
              type="text"
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search questions..."
              className="pl-8 pr-3 py-1.5 text-xs bg-dark-card dark:bg-dark-card bg-gray-100 border border-dark-border dark:border-dark-border border-gray-300 rounded-lg focus:outline-none focus:border-accent-blue w-48"
            />
          </div>
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
          {filtersActive && (
            <button onClick={clearFilters}
              className="flex items-center gap-1 px-2.5 py-1.5 text-xs text-gray-400 hover:text-red-400 transition-colors">
              <X className="w-3.5 h-3.5" /> Clear filters
            </button>
          )}
        </div>
      </div>

      <div className="grid gap-2">
        {filtered.map(q => (
          <button
            key={q.id}
            onClick={() => selectQuestion(q)}
            className="w-full text-left bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-3 hover:border-accent-blue transition-colors"
          >
            <div className="flex items-center gap-2 mb-1 flex-wrap">
              {solvedIds.includes(q.id) && (
                <CheckCircle className="w-4 h-4 text-accent-green shrink-0" />
              )}
              <span className="font-medium text-sm">#{q.id}. {q.title}</span>
              <Badge text={q.difficulty} />
              <span className="text-xs px-2 py-0.5 rounded-full bg-accent-blue/10 text-accent-blue">{q.pattern}</span>
            </div>
            <p className="text-xs text-gray-400 dark:text-gray-400 text-gray-600 mb-1.5 line-clamp-2">{q.description}</p>
            <div className="flex gap-1.5 flex-wrap">
              {q.company_tags.map(c => (
                <span key={c} onClick={(e) => handleCompanyClick(c, e)}
                  className="text-xs px-1.5 py-0.5 rounded bg-dark-surface dark:bg-dark-surface bg-gray-200 text-gray-400 dark:text-gray-400 text-gray-600 hover:bg-accent-blue/20 hover:text-accent-blue transition-colors cursor-pointer">
                  {c}
                </span>
              ))}
            </div>
          </button>
        ))}
      </div>

      {filtered.length === 0 && <p className="text-gray-500 text-sm">No questions found.</p>}
    </div>
  );
}
