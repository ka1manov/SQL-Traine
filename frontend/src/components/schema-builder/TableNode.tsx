import { useState, useRef, useCallback, useEffect } from 'react';
import { Trash2, Key, Link, Fingerprint, Plus } from 'lucide-react';
import type { SchemaTable, SchemaColumn } from '../../types';

interface Props {
  table: SchemaTable;
  onMove: (id: string, pos: { x: number; y: number }) => void;
  onRename: (id: string, name: string) => void;
  onDelete: (id: string) => void;
  onEditColumn: (tableId: string, column: SchemaColumn | null) => void;
}

function typeBadge(col: SchemaColumn) {
  let t = col.dataType;
  if (t === 'VARCHAR' && col.length) t = `VARCHAR(${col.length})` as any;
  if (t === 'NUMERIC' && col.precision != null) t = `NUM(${col.precision}${col.scale != null ? `,${col.scale}` : ''})` as any;
  return t;
}

export default function TableNode({ table, onMove, onRename, onDelete, onEditColumn }: Props) {
  const [editing, setEditing] = useState(false);
  const [editName, setEditName] = useState(table.name);
  const dragRef = useRef<{ startX: number; startY: number; originX: number; originY: number } | null>(null);
  const nodeRef = useRef<HTMLDivElement>(null);

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    if ((e.target as HTMLElement).closest('button, input')) return;
    e.preventDefault();
    const canvas = document.getElementById('schema-canvas');
    const scrollLeft = canvas?.scrollLeft || 0;
    const scrollTop = canvas?.scrollTop || 0;
    dragRef.current = {
      startX: e.clientX + scrollLeft,
      startY: e.clientY + scrollTop,
      originX: table.position.x,
      originY: table.position.y,
    };

    const handleMove = (ev: MouseEvent) => {
      if (!dragRef.current) return;
      const sl = canvas?.scrollLeft || 0;
      const st = canvas?.scrollTop || 0;
      const dx = (ev.clientX + sl) - dragRef.current.startX;
      const dy = (ev.clientY + st) - dragRef.current.startY;
      onMove(table.id, {
        x: Math.max(0, dragRef.current.originX + dx),
        y: Math.max(0, dragRef.current.originY + dy),
      });
    };

    const handleUp = () => {
      dragRef.current = null;
      window.removeEventListener('mousemove', handleMove);
      window.removeEventListener('mouseup', handleUp);
    };

    window.addEventListener('mousemove', handleMove);
    window.addEventListener('mouseup', handleUp);
  }, [table.id, table.position, onMove]);

  const finishRename = () => {
    setEditing(false);
    if (editName.trim() && editName.trim() !== table.name) {
      onRename(table.id, editName.trim());
    } else {
      setEditName(table.name);
    }
  };

  useEffect(() => { setEditName(table.name); }, [table.name]);

  return (
    <div
      ref={nodeRef}
      data-table-id={table.id}
      className="absolute w-[260px] bg-white dark:bg-dark-card border border-gray-200 dark:border-dark-border rounded-lg shadow-lg select-none"
      style={{ left: table.position.x, top: table.position.y }}
    >
      {/* Header */}
      <div
        className="flex items-center justify-between px-3 py-2 bg-gray-50 dark:bg-dark-surface rounded-t-lg border-b border-gray-200 dark:border-dark-border cursor-grab active:cursor-grabbing"
        onMouseDown={handleMouseDown}
      >
        {editing ? (
          <input
            autoFocus
            value={editName}
            onChange={e => setEditName(e.target.value)}
            onBlur={finishRename}
            onKeyDown={e => { if (e.key === 'Enter') finishRename(); if (e.key === 'Escape') { setEditName(table.name); setEditing(false); } }}
            className="flex-1 px-1 py-0 text-sm font-semibold bg-white dark:bg-dark-bg border border-accent-blue rounded outline-none"
          />
        ) : (
          <span className="text-sm font-semibold truncate" onDoubleClick={() => setEditing(true)}>{table.name}</span>
        )}
        <button onClick={() => onDelete(table.id)} className="p-1 text-gray-400 hover:text-accent-red transition-colors ml-1" title="Delete table">
          <Trash2 className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Columns */}
      <div className="divide-y divide-gray-100 dark:divide-dark-border">
        {table.columns.map(col => (
          <div
            key={col.id}
            data-column-id={col.id}
            onClick={() => onEditColumn(table.id, col)}
            className="flex items-center gap-2 px-3 py-1.5 text-xs hover:bg-gray-50 dark:hover:bg-dark-hover cursor-pointer transition-colors"
          >
            <span className="w-4 shrink-0 text-gray-400">
              {col.isPrimaryKey ? <Key className="w-3.5 h-3.5 text-accent-yellow" /> :
               col.foreignKey ? <Link className="w-3.5 h-3.5 text-accent-blue" /> :
               col.isUnique ? <Fingerprint className="w-3.5 h-3.5 text-accent-purple" /> : null}
            </span>
            <span className="flex-1 truncate font-medium">{col.name}</span>
            <span className="text-[10px] font-mono text-gray-400 dark:text-gray-500 bg-gray-100 dark:bg-dark-surface px-1.5 py-0.5 rounded">{typeBadge(col)}</span>
          </div>
        ))}
      </div>

      {/* Add Column */}
      <button
        onClick={() => onEditColumn(table.id, null)}
        className="w-full flex items-center gap-1.5 px-3 py-2 text-xs text-gray-400 hover:text-accent-blue hover:bg-gray-50 dark:hover:bg-dark-hover rounded-b-lg transition-colors"
      >
        <Plus className="w-3.5 h-3.5" />
        Add Column
      </button>
    </div>
  );
}
