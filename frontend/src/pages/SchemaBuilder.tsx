import { useState, useMemo, useCallback, useRef } from 'react';
import { Plus, Download, Upload, Copy, CheckCircle, XCircle, Loader2 } from 'lucide-react';
import Editor from '@monaco-editor/react';
import useLocalStorage from '../hooks/useLocalStorage';
import { validateDDL } from '../utils/api';
import { generateDDL } from '../utils/ddlGenerator';
import Canvas from '../components/schema-builder/Canvas';
import ColumnEditor from '../components/schema-builder/ColumnEditor';
import TypeReference from '../components/schema-builder/TypeReference';
import type { SchemaState, SchemaColumn, ValidateDDLResponse } from '../types';

export default function SchemaBuilder() {
  const [schema, setSchema] = useLocalStorage<SchemaState>('schema-builder', { tables: [] });
  const [editingColumn, setEditingColumn] = useState<{ tableId: string; column: SchemaColumn | null } | null>(null);
  const [validation, setValidation] = useState<ValidateDDLResponse | null>(null);
  const [validating, setValidating] = useState(false);
  const [copied, setCopied] = useState(false);
  const importRef = useRef<HTMLInputElement>(null);

  const ddl = useMemo(() => generateDDL(schema), [schema]);

  const addTable = useCallback(() => {
    const existing = schema.tables.map(t => t.name);
    let name = 'new_table';
    let i = 1;
    while (existing.includes(name)) { name = `new_table_${i++}`; }
    const offset = schema.tables.length * 40;
    setSchema(prev => ({
      tables: [...prev.tables, {
        id: crypto.randomUUID(),
        name,
        columns: [],
        position: { x: 80 + offset, y: 80 + offset },
      }],
    }));
  }, [schema.tables, setSchema]);

  const deleteTable = useCallback((id: string) => {
    setSchema(prev => ({
      tables: prev.tables
        .filter(t => t.id !== id)
        .map(t => ({
          ...t,
          columns: t.columns.map(c =>
            c.foreignKey?.tableId === id ? { ...c, foreignKey: null } : c
          ),
        })),
    }));
  }, [setSchema]);

  const renameTable = useCallback((id: string, name: string) => {
    setSchema(prev => ({
      tables: prev.tables.map(t => t.id === id ? { ...t, name } : t),
    }));
  }, [setSchema]);

  const moveTable = useCallback((id: string, position: { x: number; y: number }) => {
    setSchema(prev => ({
      tables: prev.tables.map(t => t.id === id ? { ...t, position } : t),
    }));
  }, [setSchema]);

  const handleEditColumn = useCallback((tableId: string, column: SchemaColumn | null) => {
    setEditingColumn({ tableId, column });
  }, []);

  const saveColumn = useCallback((col: SchemaColumn) => {
    if (!editingColumn) return;
    const { tableId, column: existing } = editingColumn;
    setSchema(prev => ({
      tables: prev.tables.map(t => {
        if (t.id !== tableId) return t;
        if (existing) {
          return { ...t, columns: t.columns.map(c => c.id === existing.id ? col : c) };
        }
        return { ...t, columns: [...t.columns, col] };
      }),
    }));
    setEditingColumn(null);
    setValidation(null);
  }, [editingColumn, setSchema]);

  const deleteColumn = useCallback(() => {
    if (!editingColumn?.column) return;
    const { tableId, column } = editingColumn;
    setSchema(prev => ({
      tables: prev.tables.map(t => {
        if (t.id !== tableId) return t;
        return { ...t, columns: t.columns.filter(c => c.id !== column.id) };
      }).map(t => ({
        ...t,
        columns: t.columns.map(c =>
          c.foreignKey?.columnId === column.id && c.foreignKey.tableId === tableId
            ? { ...c, foreignKey: null } : c
        ),
      })),
    }));
    setEditingColumn(null);
    setValidation(null);
  }, [editingColumn, setSchema]);

  const handleValidate = async () => {
    setValidating(true);
    try {
      const result = await validateDDL(ddl);
      setValidation(result);
    } catch {
      setValidation({ valid: false, error: 'Network error', details: null });
    }
    setValidating(false);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(ddl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleExport = () => {
    const blob = new Blob([JSON.stringify(schema, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'schema.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      try {
        const parsed = JSON.parse(ev.target?.result as string);
        if (parsed.tables && Array.isArray(parsed.tables)) {
          setSchema(parsed);
          setValidation(null);
        }
      } catch { /* ignore invalid JSON */ }
    };
    reader.readAsText(file);
    e.target.value = '';
  };

  return (
    <div className="flex h-full overflow-hidden">
      {/* Sidebar */}
      <div className="w-56 shrink-0 border-r border-gray-200 dark:border-dark-border flex flex-col overflow-y-auto bg-white dark:bg-dark-surface">
        <div className="p-3 border-b border-gray-200 dark:border-dark-border">
          <h2 className="font-bold text-sm mb-2">Schema Builder</h2>
          <button onClick={addTable} className="w-full flex items-center justify-center gap-1.5 px-3 py-2 text-sm bg-accent-blue text-white rounded-lg hover:bg-blue-600 transition-colors">
            <Plus className="w-4 h-4" /> Add Table
          </button>
        </div>

        {/* Table list */}
        {schema.tables.length > 0 && (
          <div className="p-3 border-b border-gray-200 dark:border-dark-border">
            <h3 className="text-xs font-medium text-gray-500 dark:text-gray-400 mb-1.5">Tables ({schema.tables.length})</h3>
            <div className="space-y-1">
              {schema.tables.map(t => (
                <div key={t.id} className="flex items-center gap-2 px-2 py-1 text-xs rounded hover:bg-gray-100 dark:hover:bg-dark-hover">
                  <span className="w-2 h-2 rounded-full bg-accent-green shrink-0" />
                  <span className="truncate">{t.name}</span>
                  <span className="text-gray-400 ml-auto">{t.columns.length}c</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Reference Guide */}
        <div className="p-3 flex-1">
          <TypeReference />
        </div>

        {/* Export/Import */}
        <div className="p-3 border-t border-gray-200 dark:border-dark-border flex gap-2">
          <button onClick={handleExport} className="flex-1 flex items-center justify-center gap-1 px-2 py-1.5 text-xs border border-gray-300 dark:border-dark-border rounded-lg hover:bg-gray-50 dark:hover:bg-dark-hover transition-colors">
            <Download className="w-3.5 h-3.5" /> Export
          </button>
          <button onClick={() => importRef.current?.click()} className="flex-1 flex items-center justify-center gap-1 px-2 py-1.5 text-xs border border-gray-300 dark:border-dark-border rounded-lg hover:bg-gray-50 dark:hover:bg-dark-hover transition-colors">
            <Upload className="w-3.5 h-3.5" /> Import
          </button>
          <input ref={importRef} type="file" accept=".json" onChange={handleImport} className="hidden" />
        </div>
      </div>

      {/* Canvas */}
      <Canvas
        tables={schema.tables}
        onMove={moveTable}
        onRename={renameTable}
        onDelete={deleteTable}
        onEditColumn={handleEditColumn}
      />

      {/* DDL Preview */}
      <div className="w-80 shrink-0 border-l border-gray-200 dark:border-dark-border flex flex-col bg-white dark:bg-dark-surface">
        <div className="p-3 border-b border-gray-200 dark:border-dark-border">
          <h3 className="font-semibold text-sm">DDL Preview</h3>
        </div>
        <div className="flex-1 min-h-0">
          <Editor
            height="100%"
            language="sql"
            value={ddl}
            theme="vs-dark"
            options={{ readOnly: true, minimap: { enabled: false }, fontSize: 12, lineNumbers: 'off', scrollBeyondLastLine: false, wordWrap: 'on', padding: { top: 8 } }}
          />
        </div>
        <div className="p-3 border-t border-gray-200 dark:border-dark-border space-y-2">
          <div className="flex gap-2">
            <button onClick={handleCopy} className="flex-1 flex items-center justify-center gap-1.5 px-3 py-1.5 text-xs border border-gray-300 dark:border-dark-border rounded-lg hover:bg-gray-50 dark:hover:bg-dark-hover transition-colors">
              {copied ? <><CheckCircle className="w-3.5 h-3.5 text-accent-green" /> Copied!</> : <><Copy className="w-3.5 h-3.5" /> Copy</>}
            </button>
            <button
              onClick={handleValidate}
              disabled={validating || schema.tables.length === 0}
              className="flex-1 flex items-center justify-center gap-1.5 px-3 py-1.5 text-xs bg-accent-green text-white rounded-lg hover:bg-green-600 disabled:opacity-50 transition-colors"
            >
              {validating ? <><Loader2 className="w-3.5 h-3.5 animate-spin" /> Validating...</> : 'Validate'}
            </button>
          </div>
          {validation && (
            <div className={`flex items-start gap-2 p-2 rounded text-xs ${validation.valid ? 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400' : 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400'}`}>
              {validation.valid ? <CheckCircle className="w-4 h-4 shrink-0 mt-0.5" /> : <XCircle className="w-4 h-4 shrink-0 mt-0.5" />}
              <span>{validation.valid ? validation.details || 'Valid DDL' : validation.error}</span>
            </div>
          )}
        </div>
      </div>

      {/* Column Editor Modal */}
      {editingColumn && (
        <ColumnEditor
          column={editingColumn.column}
          tableId={editingColumn.tableId}
          tables={schema.tables}
          onSave={saveColumn}
          onDelete={editingColumn.column ? deleteColumn : undefined}
          onClose={() => setEditingColumn(null)}
        />
      )}
    </div>
  );
}
