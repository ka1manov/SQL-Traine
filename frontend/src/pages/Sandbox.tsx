import { useState, useCallback, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Play, Trash2, AlignLeft } from 'lucide-react';
import SQLEditor from '../components/SQLEditor';
import ResultTable from '../components/ResultTable';
import TableSidebar from '../components/TableSidebar';
import QueryTemplates from '../components/QueryTemplates';
import { executeSQL, formatSQL } from '../utils/api';
import type { ExecuteResponse } from '../types';

export default function Sandbox() {
  const [sql, setSql] = useState('SELECT * FROM employees LIMIT 10;');
  const [result, setResult] = useState<ExecuteResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const location = useLocation();

  useEffect(() => {
    if (location.state?.prefillSQL) {
      setSql(location.state.prefillSQL);
      window.history.replaceState({}, '');
    }
  }, []);

  const runQuery = useCallback(async () => {
    if (!sql.trim()) return;
    setLoading(true);
    try {
      const res = await executeSQL(sql);
      setResult(res);
    } catch (err: any) {
      setResult({ columns: [], rows: [], row_count: 0, error: err.message || 'Request failed', execution_time_ms: 0 });
    } finally {
      setLoading(false);
    }
  }, [sql]);

  const handleFormat = useCallback(async () => {
    try {
      const formatted = await formatSQL(sql);
      setSql(formatted);
    } catch {}
  }, [sql]);

  return (
    <div className="flex h-full flex-col lg:flex-row">
      <div className="flex-1 flex flex-col p-4 gap-4 overflow-y-auto">
        <div className="flex items-center justify-between flex-wrap gap-2">
          <h1 className="text-xl font-bold">SQL Sandbox</h1>
          <div className="flex gap-2 flex-wrap">
            <QueryTemplates onSelect={setSql} />
            <button onClick={handleFormat}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-dark-card dark:bg-dark-card bg-gray-100 hover:bg-dark-hover border border-dark-border rounded-lg text-xs text-gray-400 transition-colors">
              <AlignLeft className="w-3.5 h-3.5" /> Format
            </button>
            <button onClick={runQuery} disabled={loading}
              className="flex items-center gap-2 px-4 py-2 bg-accent-blue hover:bg-blue-600 rounded-lg text-sm font-medium text-white transition-colors disabled:opacity-50">
              <Play className="w-4 h-4" />
              {loading ? 'Running...' : 'Run'}
            </button>
            <button onClick={() => { setSql(''); setResult(null); }}
              className="flex items-center gap-2 px-3 py-2 bg-dark-card dark:bg-dark-card bg-gray-100 hover:bg-dark-hover rounded-lg text-sm text-gray-400 transition-colors">
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>

        <SQLEditor value={sql} onChange={setSql} onRun={runQuery} onFormat={handleFormat} height="200px" />
        <ResultTable result={result} maxHeight="400px" />
      </div>

      <div className="w-full lg:w-56 p-4 border-t lg:border-t-0 lg:border-l border-dark-border dark:border-dark-border border-gray-200 shrink-0 overflow-y-auto">
        <TableSidebar />
      </div>
    </div>
  );
}
