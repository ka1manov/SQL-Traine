import { useState, useEffect } from 'react';
import { ChevronRight, Table2, Key, Link2 } from 'lucide-react';
import { fetchTables, fetchTableSchema } from '../utils/api';
import type { ColumnInfo } from '../types';

export default function TableSidebar() {
  const [tables, setTables] = useState<string[]>([]);
  const [expanded, setExpanded] = useState<string | null>(null);
  const [schemas, setSchemas] = useState<Record<string, ColumnInfo[]>>({});

  useEffect(() => {
    fetchTables().then(setTables).catch(console.error);
  }, []);

  const toggleTable = async (name: string) => {
    if (expanded === name) { setExpanded(null); return; }
    setExpanded(name);
    if (!schemas[name]) {
      try {
        const cols = await fetchTableSchema(name);
        setSchemas(prev => ({ ...prev, [name]: cols }));
      } catch (err) { console.error('Failed to load schema:', err); }
    }
  };

  return (
    <div className="bg-dark-surface dark:bg-dark-surface bg-gray-50 border border-dark-border dark:border-dark-border border-gray-200 rounded-lg overflow-hidden">
      <div className="px-3 py-2 border-b border-dark-border dark:border-dark-border border-gray-200 text-sm font-medium text-gray-400">
        Tables
      </div>
      <div className="max-h-80 overflow-y-auto">
        {tables.map(t => (
          <div key={t}>
            <button
              onClick={() => toggleTable(t)}
              className="w-full flex items-center gap-2 px-3 py-1.5 text-sm text-gray-300 dark:text-gray-300 text-gray-700 hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-100 transition-colors"
            >
              <ChevronRight className={`w-3 h-3 transition-transform ${expanded === t ? 'rotate-90' : ''}`} />
              <Table2 className="w-3.5 h-3.5 text-accent-blue" />
              {t}
            </button>
            {expanded === t && schemas[t] && (
              <div className="pl-7 pb-1 space-y-0.5">
                {schemas[t].map(col => (
                  <div key={col.name} className="flex items-center gap-1.5 text-xs py-0.5">
                    {col.fk ? <Link2 className="w-2.5 h-2.5 text-accent-yellow" /> : col.name === 'id' ? <Key className="w-2.5 h-2.5 text-accent-purple" /> : <span className="w-2.5" />}
                    <span className="text-gray-400 dark:text-gray-400 text-gray-600">{col.name}</span>
                    <span className="text-gray-600 dark:text-gray-600 text-gray-400 text-[10px]">{col.type}</span>
                    {col.fk && <span className="text-[10px] text-accent-yellow">→{col.fk}</span>}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
