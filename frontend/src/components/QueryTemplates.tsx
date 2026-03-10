import { useState, useEffect } from 'react';
import { FileCode, ChevronDown } from 'lucide-react';
import { fetchTemplates } from '../utils/api';
import type { QueryTemplate } from '../types';

interface Props {
  onSelect: (sql: string) => void;
}

export default function QueryTemplates({ onSelect }: Props) {
  const [templates, setTemplates] = useState<QueryTemplate[]>([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    fetchTemplates().then(setTemplates).catch(() => {});
  }, []);

  if (templates.length === 0) return null;

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1.5 px-3 py-1.5 bg-dark-card dark:bg-dark-card bg-gray-100 border border-dark-border rounded-lg text-xs text-gray-400 hover:bg-dark-hover transition-colors"
      >
        <FileCode className="w-3.5 h-3.5" />
        Templates
        <ChevronDown className={`w-3 h-3 transition-transform ${open ? 'rotate-180' : ''}`} />
      </button>
      {open && (
        <div className="absolute top-full left-0 mt-1 w-72 bg-dark-card dark:bg-dark-card bg-white border border-dark-border rounded-lg shadow-xl z-20 max-h-80 overflow-y-auto">
          {templates.map(t => (
            <button
              key={t.id}
              onClick={() => { onSelect(t.sql); setOpen(false); }}
              className="w-full text-left px-3 py-2 hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-50 border-b border-dark-border/30 last:border-0 transition-colors"
            >
              <div className="flex items-center gap-2">
                <span className="text-xs font-medium text-gray-200 dark:text-gray-200 text-gray-700">{t.title}</span>
                <span className="text-[10px] text-gray-500 bg-dark-bg dark:bg-dark-bg bg-gray-100 px-1.5 py-0.5 rounded">{t.category}</span>
              </div>
              <p className="text-[10px] text-gray-500 mt-0.5">{t.description}</p>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
