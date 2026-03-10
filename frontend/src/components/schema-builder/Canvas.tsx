import { useMemo } from 'react';
import type { SchemaTable, SchemaColumn } from '../../types';
import TableNode from './TableNode';

interface Props {
  tables: SchemaTable[];
  onMove: (id: string, pos: { x: number; y: number }) => void;
  onRename: (id: string, name: string) => void;
  onDelete: (id: string) => void;
  onEditColumn: (tableId: string, column: SchemaColumn | null) => void;
}

interface Arrow {
  key: string;
  x1: number; y1: number;
  x2: number; y2: number;
}

function computeArrows(tables: SchemaTable[]): Arrow[] {
  const arrows: Arrow[] = [];
  const TABLE_W = 260;
  const ROW_H = 28;
  const HEADER_H = 36;

  for (const table of tables) {
    for (let ci = 0; ci < table.columns.length; ci++) {
      const col = table.columns[ci];
      if (!col.foreignKey) continue;
      const target = tables.find(t => t.id === col.foreignKey!.tableId);
      if (!target) continue;
      const targetColIdx = target.columns.findIndex(c => c.id === col.foreignKey!.columnId);
      if (targetColIdx === -1) continue;

      const srcY = table.position.y + HEADER_H + ci * ROW_H + ROW_H / 2;
      const tgtY = target.position.y + HEADER_H + targetColIdx * ROW_H + ROW_H / 2;

      // Determine which side to connect from
      const srcCenterX = table.position.x + TABLE_W / 2;
      const tgtCenterX = target.position.x + TABLE_W / 2;
      const x1 = srcCenterX < tgtCenterX ? table.position.x + TABLE_W : table.position.x;
      const x2 = srcCenterX < tgtCenterX ? target.position.x : target.position.x + TABLE_W;

      arrows.push({ key: `${table.id}-${col.id}`, x1, y1: srcY, x2, y2: tgtY });
    }
  }
  return arrows;
}

export default function Canvas({ tables, onMove, onRename, onDelete, onEditColumn }: Props) {
  const arrows = useMemo(() => computeArrows(tables), [tables]);

  const maxX = Math.max(2000, ...tables.map(t => t.position.x + 400));
  const maxY = Math.max(1500, ...tables.map(t => t.position.y + 300));

  return (
    <div
      id="schema-canvas"
      className="flex-1 overflow-auto relative"
      style={{
        backgroundImage: 'radial-gradient(circle, #d1d5db 1px, transparent 1px)',
        backgroundSize: '20px 20px',
      }}
    >
      <div className="dark:hidden absolute inset-0" style={{
        backgroundImage: 'radial-gradient(circle, #d1d5db 1px, transparent 1px)',
        backgroundSize: '20px 20px',
      }} />
      <div className="hidden dark:block absolute inset-0" style={{
        backgroundImage: 'radial-gradient(circle, #374151 1px, transparent 1px)',
        backgroundSize: '20px 20px',
      }} />

      <div style={{ width: maxX, height: maxY, position: 'relative' }}>
        {/* SVG arrows */}
        <svg
          className="absolute inset-0 pointer-events-none"
          width={maxX}
          height={maxY}
          style={{ zIndex: 1 }}
        >
          <defs>
            <marker id="arrowhead" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
              <polygon points="0 0, 8 3, 0 6" className="fill-accent-blue" />
            </marker>
          </defs>
          {arrows.map(a => {
            const dx = Math.abs(a.x2 - a.x1) * 0.5;
            const d = `M ${a.x1} ${a.y1} C ${a.x1 + (a.x1 < a.x2 ? dx : -dx)} ${a.y1}, ${a.x2 + (a.x1 < a.x2 ? -dx : dx)} ${a.y2}, ${a.x2} ${a.y2}`;
            return (
              <path
                key={a.key}
                d={d}
                fill="none"
                className="stroke-accent-blue"
                strokeWidth={2}
                markerEnd="url(#arrowhead)"
              />
            );
          })}
        </svg>

        {/* Table nodes */}
        {tables.map(t => (
          <TableNode
            key={t.id}
            table={t}
            onMove={onMove}
            onRename={onRename}
            onDelete={onDelete}
            onEditColumn={onEditColumn}
          />
        ))}

        {/* Empty state */}
        {tables.length === 0 && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="text-center text-gray-400 dark:text-gray-500">
              <p className="text-lg font-medium mb-1">No tables yet</p>
              <p className="text-sm">Click "+ Add Table" in the sidebar to get started</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
