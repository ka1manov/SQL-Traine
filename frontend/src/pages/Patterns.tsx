import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronDown, ChevronRight, Copy, Play, Link as LinkIcon } from 'lucide-react';
import { fetchPatterns, fetchPatternCategories } from '../utils/api';
import type { SQLPattern } from '../types';

export default function Patterns() {
  const [patterns, setPatterns] = useState<SQLPattern[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [expanded, setExpanded] = useState<Set<number>>(new Set());
  const [copied, setCopied] = useState<number | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchPatternCategories().then(setCategories).catch(console.error);
  }, []);

  useEffect(() => {
    fetchPatterns(selectedCategory || undefined).then(setPatterns).catch(console.error);
  }, [selectedCategory]);

  const toggleExpand = (id: number) => {
    setExpanded(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const copyTemplate = async (sql: string, id: number) => {
    try {
      await navigator.clipboard.writeText(sql);
      setCopied(id);
      setTimeout(() => setCopied(null), 2000);
    } catch {}
  };

  const tryInSandbox = (sql: string) => {
    navigate('/', { state: { prefillSQL: sql } });
  };

  return (
    <div className="p-4 space-y-4 max-w-4xl">
      <h1 className="text-xl font-bold">SQL Patterns Cheat Sheet</h1>
      <p className="text-sm text-gray-400 dark:text-gray-400 text-gray-600">
        Common SQL patterns with templates and runnable examples. Click any pattern to expand.
      </p>

      <div className="flex gap-2 flex-wrap">
        <button
          onClick={() => setSelectedCategory('')}
          className={`px-3 py-1.5 text-xs rounded-full border transition-colors ${
            !selectedCategory
              ? 'bg-accent-blue text-white border-accent-blue'
              : 'bg-dark-card dark:bg-dark-card bg-gray-100 text-gray-400 border-dark-border dark:border-dark-border border-gray-300 hover:border-accent-blue'
          }`}
        >
          All
        </button>
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-3 py-1.5 text-xs rounded-full border transition-colors ${
              selectedCategory === cat
                ? 'bg-accent-blue text-white border-accent-blue'
                : 'bg-dark-card dark:bg-dark-card bg-gray-100 text-gray-400 border-dark-border dark:border-dark-border border-gray-300 hover:border-accent-blue'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      <div className="space-y-2">
        {patterns.map(p => {
          const isExpanded = expanded.has(p.id);
          return (
            <div key={p.id} className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg overflow-hidden">
              <button
                onClick={() => toggleExpand(p.id)}
                className="w-full flex items-center gap-3 p-3 text-left hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-100 transition-colors"
              >
                {isExpanded ? <ChevronDown className="w-4 h-4 text-gray-500 shrink-0" /> : <ChevronRight className="w-4 h-4 text-gray-500 shrink-0" />}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-medium text-sm">{p.name}</span>
                    <span className="text-xs px-2 py-0.5 rounded-full bg-accent-blue/10 text-accent-blue">{p.category}</span>
                  </div>
                  <p className="text-xs text-gray-400 dark:text-gray-400 text-gray-600 mt-0.5 truncate">{p.description}</p>
                </div>
              </button>

              {isExpanded && (
                <div className="px-3 pb-3 space-y-3 border-t border-dark-border dark:border-dark-border border-gray-200">
                  <div className="mt-3">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-medium text-gray-400">Template</span>
                      <button
                        onClick={() => copyTemplate(p.template_sql, p.id)}
                        className="flex items-center gap-1 text-xs text-gray-500 hover:text-accent-blue"
                      >
                        <Copy className="w-3 h-3" /> {copied === p.id ? 'Copied!' : 'Copy'}
                      </button>
                    </div>
                    <pre className="bg-dark-bg dark:bg-dark-bg bg-gray-100 rounded p-2 text-xs font-mono text-gray-300 dark:text-gray-300 text-gray-700 overflow-x-auto whitespace-pre-wrap">{p.template_sql}</pre>
                  </div>

                  <div>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-medium text-gray-400">Example (runnable)</span>
                      <button
                        onClick={() => tryInSandbox(p.example_sql)}
                        className="flex items-center gap-1 text-xs text-accent-green hover:text-green-400"
                      >
                        <Play className="w-3 h-3" /> Try in Sandbox
                      </button>
                    </div>
                    <pre className="bg-dark-bg dark:bg-dark-bg bg-gray-100 rounded p-2 text-xs font-mono text-accent-blue overflow-x-auto whitespace-pre-wrap">{p.example_sql}</pre>
                  </div>

                  <div>
                    <span className="text-xs font-medium text-gray-400">Explanation</span>
                    <p className="text-sm text-gray-300 dark:text-gray-300 text-gray-700 mt-0.5">{p.explanation}</p>
                  </div>

                  <div>
                    <span className="text-xs font-medium text-gray-400">Use Cases</span>
                    <ul className="mt-0.5 space-y-0.5">
                      {p.use_cases.map((uc, i) => (
                        <li key={i} className="text-xs text-gray-400 dark:text-gray-400 text-gray-600 flex items-start gap-1.5">
                          <span className="text-accent-blue mt-0.5">-</span> {uc}
                        </li>
                      ))}
                    </ul>
                  </div>

                  {p.related_task_ids.length > 0 && (
                    <div>
                      <span className="text-xs font-medium text-gray-400">Related Tasks</span>
                      <div className="flex gap-1.5 mt-1 flex-wrap">
                        {p.related_task_ids.map(tid => (
                          <a
                            key={tid}
                            href={`/tasks`}
                            className="flex items-center gap-1 text-xs px-2 py-0.5 rounded bg-dark-bg dark:bg-dark-bg bg-gray-100 text-accent-blue hover:bg-accent-blue/10"
                          >
                            <LinkIcon className="w-3 h-3" /> Task #{tid}
                          </a>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {patterns.length === 0 && <p className="text-gray-500 text-sm">No patterns found.</p>}
    </div>
  );
}
