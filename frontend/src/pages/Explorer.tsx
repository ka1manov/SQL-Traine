import { useState, useEffect } from 'react';
import { Table2, ChevronLeft, ChevronRight, Key, Link2 } from 'lucide-react';
import ResultTable from '../components/ResultTable';
import { fetchTables, fetchTableData, fetchTableSchema } from '../utils/api';
import type { ExecuteResponse, ColumnInfo } from '../types';

export default function Explorer() {
  const [tables, setTables] = useState<string[]>([]);
  const [selected, setSelected] = useState('');
  const [data, setData] = useState<ExecuteResponse | null>(null);
  const [schema, setSchema] = useState<ColumnInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(0);
  const pageSize = 50;

  useEffect(() => {
    fetchTables().then(t => {
      setTables(t);
      if (t.length > 0) loadTable(t[0], 0);
    }).catch(console.error);
  }, []);

  const loadTable = async (name: string, pg: number) => {
    setSelected(name);
    setPage(pg);
    setLoading(true);
    try {
      const [res, cols] = await Promise.all([
        fetchTableData(name, pageSize, pg * pageSize),
        fetchTableSchema(name),
      ]);
      setData(res);
      setSchema(cols);
    } catch (err) {
      console.error('Failed to load table:', err);
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  const totalRows = data?.total_rows ?? 0;
  const totalPages = Math.ceil(totalRows / pageSize);

  return (
    <div className="p-4 space-y-4">
      <div className="flex items-center gap-2">
        <Table2 className="w-6 h-6 text-accent-blue" />
        <h1 className="text-xl font-bold">Table Explorer</h1>
      </div>

      <div className="flex gap-2 flex-wrap">
        {tables.map(t => (
          <button key={t} onClick={() => loadTable(t, 0)}
            className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
              selected === t ? 'bg-accent-blue text-white' : 'bg-dark-card dark:bg-dark-card bg-gray-100 border border-dark-border text-gray-400 hover:bg-dark-hover'
            }`}>{t}</button>
        ))}
      </div>

      {schema.length > 0 && (
        <div className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg p-3">
          <h3 className="text-xs font-medium text-gray-500 mb-2">Schema: {selected}</h3>
          <div className="flex flex-wrap gap-x-4 gap-y-1">
            {schema.map(col => (
              <div key={col.name} className="flex items-center gap-1.5 text-xs">
                {col.fk ? <Link2 className="w-3 h-3 text-accent-yellow" /> : col.name === 'id' ? <Key className="w-3 h-3 text-accent-purple" /> : null}
                <span className="font-medium text-gray-300 dark:text-gray-300 text-gray-700">{col.name}</span>
                <span className="text-gray-500">{col.type}</span>
                {!col.nullable && <span className="text-[10px] text-accent-red">NOT NULL</span>}
                {col.fk && <span className="text-[10px] text-accent-yellow">→{col.fk}</span>}
              </div>
            ))}
          </div>
        </div>
      )}

      {loading && <div className="text-gray-500 text-sm">Loading...</div>}

      {data && (
        <>
          <div className="text-sm text-gray-500">
            {selected} — Showing {page * pageSize + 1}-{Math.min((page + 1) * pageSize, totalRows)} of {totalRows} rows
          </div>
          <ResultTable result={data} maxHeight="500px" />
          {totalPages > 1 && (
            <div className="flex items-center gap-3 justify-center">
              <button onClick={() => loadTable(selected, page - 1)} disabled={page === 0}
                className="p-1.5 bg-dark-card border border-dark-border rounded-lg disabled:opacity-30 hover:bg-dark-hover">
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span className="text-sm text-gray-500">Page {page + 1} / {totalPages}</span>
              <button onClick={() => loadTable(selected, page + 1)} disabled={page >= totalPages - 1}
                className="p-1.5 bg-dark-card border border-dark-border rounded-lg disabled:opacity-30 hover:bg-dark-hover">
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
