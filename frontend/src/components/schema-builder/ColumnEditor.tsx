import { useState, useEffect } from 'react';
import type { SchemaColumn, SchemaTable, ColumnDataType } from '../../types';

const ALL_TYPES: ColumnDataType[] = [
  'SERIAL', 'BIGSERIAL', 'INTEGER', 'BIGINT', 'SMALLINT',
  'VARCHAR', 'TEXT', 'BOOLEAN', 'DATE', 'TIMESTAMP', 'TIMESTAMPTZ',
  'NUMERIC', 'REAL', 'DOUBLE PRECISION', 'JSONB', 'JSON', 'UUID',
];

interface Props {
  column: SchemaColumn | null; // null = new column
  tableId: string;
  tables: SchemaTable[];
  onSave: (col: SchemaColumn) => void;
  onDelete?: () => void;
  onClose: () => void;
}

export default function ColumnEditor({ column, tableId, tables, onSave, onDelete, onClose }: Props) {
  const [name, setName] = useState(column?.name || '');
  const [dataType, setDataType] = useState<ColumnDataType>(column?.dataType || 'INTEGER');
  const [length, setLength] = useState<string>(column?.length?.toString() || '');
  const [precision, setPrecision] = useState<string>(column?.precision?.toString() || '');
  const [scale, setScale] = useState<string>(column?.scale?.toString() || '');
  const [isPrimaryKey, setIsPrimaryKey] = useState(column?.isPrimaryKey || false);
  const [isNotNull, setIsNotNull] = useState(column?.isNotNull || false);
  const [isUnique, setIsUnique] = useState(column?.isUnique || false);
  const [defaultValue, setDefaultValue] = useState(column?.defaultValue || '');
  const [checkConstraint, setCheckConstraint] = useState(column?.checkConstraint || '');
  const [fkTableId, setFkTableId] = useState(column?.foreignKey?.tableId || '');
  const [fkColumnId, setFkColumnId] = useState(column?.foreignKey?.columnId || '');

  const fkTargetTable = tables.find(t => t.id === fkTableId);
  const otherTables = tables.filter(t => t.id !== tableId);

  useEffect(() => {
    if (fkTableId && fkTargetTable) {
      const colExists = fkTargetTable.columns.some(c => c.id === fkColumnId);
      if (!colExists) setFkColumnId(fkTargetTable.columns[0]?.id || '');
    }
  }, [fkTableId]);

  const handleSave = () => {
    if (!name.trim()) return;
    onSave({
      id: column?.id || crypto.randomUUID(),
      name: name.trim(),
      dataType,
      length: dataType === 'VARCHAR' && length ? parseInt(length) : null,
      precision: dataType === 'NUMERIC' && precision ? parseInt(precision) : null,
      scale: dataType === 'NUMERIC' && scale ? parseInt(scale) : null,
      isPrimaryKey,
      isNotNull: isPrimaryKey || isNotNull,
      isUnique,
      defaultValue: defaultValue.trim() || null,
      checkConstraint: checkConstraint.trim() || null,
      foreignKey: fkTableId && fkColumnId ? { tableId: fkTableId, columnId: fkColumnId } : null,
    });
  };

  const inputCls = 'w-full px-2 py-1.5 rounded border border-gray-300 dark:border-dark-border bg-white dark:bg-dark-bg text-sm focus:outline-none focus:border-accent-blue';
  const toggleCls = (active: boolean) =>
    `px-3 py-1.5 rounded text-xs font-medium transition-colors ${active ? 'bg-accent-blue text-white' : 'bg-gray-100 dark:bg-dark-surface text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-dark-hover'}`;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={onClose}>
      <div className="bg-white dark:bg-dark-card rounded-xl shadow-2xl w-full max-w-md mx-4 max-h-[90vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
        <div className="px-5 py-4 border-b border-gray-200 dark:border-dark-border flex items-center justify-between">
          <h3 className="font-semibold">{column ? 'Edit Column' : 'New Column'}</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 text-lg">&times;</button>
        </div>

        <div className="p-5 space-y-4">
          <div>
            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Column Name</label>
            <input autoFocus value={name} onChange={e => setName(e.target.value)} placeholder="column_name" className={inputCls} />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Data Type</label>
            <select value={dataType} onChange={e => setDataType(e.target.value as ColumnDataType)} className={inputCls}>
              {ALL_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>

          {dataType === 'VARCHAR' && (
            <div>
              <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Length</label>
              <input type="number" value={length} onChange={e => setLength(e.target.value)} placeholder="255" className={inputCls} />
            </div>
          )}

          {dataType === 'NUMERIC' && (
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Precision</label>
                <input type="number" value={precision} onChange={e => setPrecision(e.target.value)} placeholder="10" className={inputCls} />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Scale</label>
                <input type="number" value={scale} onChange={e => setScale(e.target.value)} placeholder="2" className={inputCls} />
              </div>
            </div>
          )}

          <div>
            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Constraints</label>
            <div className="flex flex-wrap gap-2">
              <button type="button" onClick={() => setIsPrimaryKey(!isPrimaryKey)} className={toggleCls(isPrimaryKey)}>PRIMARY KEY</button>
              <button type="button" onClick={() => setIsNotNull(!isNotNull)} className={toggleCls(isNotNull || isPrimaryKey)} disabled={isPrimaryKey}>NOT NULL</button>
              <button type="button" onClick={() => setIsUnique(!isUnique)} className={toggleCls(isUnique)}>UNIQUE</button>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Default Value</label>
            <input value={defaultValue} onChange={e => setDefaultValue(e.target.value)} placeholder="NOW(), 0, 'active'" className={inputCls} />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">CHECK Constraint</label>
            <input value={checkConstraint} onChange={e => setCheckConstraint(e.target.value)} placeholder="age > 0" className={inputCls} />
          </div>

          {otherTables.length > 0 && (
            <div className="border-t border-gray-200 dark:border-dark-border pt-4">
              <label className="block text-xs font-medium text-gray-500 dark:text-gray-400 mb-1">Foreign Key</label>
              <div className="grid grid-cols-2 gap-3">
                <select value={fkTableId} onChange={e => setFkTableId(e.target.value)} className={inputCls}>
                  <option value="">No FK</option>
                  {otherTables.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
                </select>
                {fkTableId && fkTargetTable && (
                  <select value={fkColumnId} onChange={e => setFkColumnId(e.target.value)} className={inputCls}>
                    {fkTargetTable.columns.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                  </select>
                )}
              </div>
              {fkTableId && (
                <button onClick={() => { setFkTableId(''); setFkColumnId(''); }} className="text-xs text-accent-red hover:underline mt-1">Remove FK</button>
              )}
            </div>
          )}
        </div>

        <div className="px-5 py-3 border-t border-gray-200 dark:border-dark-border flex items-center justify-between">
          <div>
            {column && onDelete && (
              <button onClick={onDelete} className="text-xs text-accent-red hover:underline">Delete Column</button>
            )}
          </div>
          <div className="flex gap-2">
            <button onClick={onClose} className="px-4 py-1.5 text-sm rounded-lg border border-gray-300 dark:border-dark-border hover:bg-gray-50 dark:hover:bg-dark-hover">Cancel</button>
            <button onClick={handleSave} disabled={!name.trim()} className="px-4 py-1.5 text-sm rounded-lg bg-accent-blue text-white hover:bg-blue-600 disabled:opacity-50">Save</button>
          </div>
        </div>
      </div>
    </div>
  );
}
