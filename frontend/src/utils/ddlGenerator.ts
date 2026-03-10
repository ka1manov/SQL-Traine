import type { SchemaState, SchemaTable, SchemaColumn } from '../types';

const RESERVED = new Set([
  'USER', 'ORDER', 'TABLE', 'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE',
  'DROP', 'ALTER', 'INDEX', 'GROUP', 'CHECK', 'DEFAULT', 'PRIMARY', 'FOREIGN',
  'KEY', 'REFERENCES', 'CONSTRAINT', 'CASCADE', 'SET', 'NULL', 'NOT', 'AND',
  'OR', 'IN', 'FROM', 'WHERE', 'JOIN', 'ON', 'AS', 'BY', 'TO', 'WITH',
  'ROLE', 'GRANT', 'REVOKE', 'LIMIT', 'OFFSET', 'HAVING', 'UNION', 'ALL',
]);

function escapeIdent(name: string): string {
  if (!name) return '""';
  if (RESERVED.has(name.toUpperCase()) || /[A-Z\s\-]/.test(name)) {
    return `"${name}"`;
  }
  return name;
}

function formatDataType(col: SchemaColumn): string {
  const t = col.dataType;
  if (t === 'VARCHAR' && col.length) return `VARCHAR(${col.length})`;
  if (t === 'NUMERIC' && col.precision != null) {
    return col.scale != null ? `NUMERIC(${col.precision},${col.scale})` : `NUMERIC(${col.precision})`;
  }
  return t;
}

function topologicalSort(tables: SchemaTable[]): SchemaTable[] {
  const idToTable = new Map(tables.map(t => [t.id, t]));
  const inDegree = new Map(tables.map(t => [t.id, 0]));
  const adj = new Map<string, string[]>(tables.map(t => [t.id, []]));

  for (const table of tables) {
    for (const col of table.columns) {
      if (col.foreignKey && idToTable.has(col.foreignKey.tableId) && col.foreignKey.tableId !== table.id) {
        adj.get(col.foreignKey.tableId)!.push(table.id);
        inDegree.set(table.id, (inDegree.get(table.id) || 0) + 1);
      }
    }
  }

  const queue: string[] = [];
  for (const [id, deg] of inDegree) {
    if (deg === 0) queue.push(id);
  }

  const sorted: SchemaTable[] = [];
  while (queue.length > 0) {
    const id = queue.shift()!;
    sorted.push(idToTable.get(id)!);
    for (const next of adj.get(id) || []) {
      const d = inDegree.get(next)! - 1;
      inDegree.set(next, d);
      if (d === 0) queue.push(next);
    }
  }

  // If cycle detected, append remaining tables in original order
  if (sorted.length < tables.length) {
    const sortedIds = new Set(sorted.map(t => t.id));
    for (const t of tables) {
      if (!sortedIds.has(t.id)) sorted.push(t);
    }
  }

  return sorted;
}

function generateTableDDL(table: SchemaTable, allTables: SchemaTable[]): string {
  if (table.columns.length === 0) {
    return `-- Table: ${table.name}\nCREATE TABLE ${escapeIdent(table.name)} ();`;
  }

  const lines: string[] = [];
  for (const col of table.columns) {
    let line = `  ${escapeIdent(col.name)} ${formatDataType(col)}`;
    if (col.isPrimaryKey) line += ' PRIMARY KEY';
    if (col.isNotNull && !col.isPrimaryKey) line += ' NOT NULL';
    if (col.isUnique && !col.isPrimaryKey) line += ' UNIQUE';
    if (col.defaultValue) line += ` DEFAULT ${col.defaultValue}`;
    if (col.checkConstraint) line += ` CHECK (${col.checkConstraint})`;
    if (col.foreignKey) {
      const refTable = allTables.find(t => t.id === col.foreignKey!.tableId);
      const refCol = refTable?.columns.find(c => c.id === col.foreignKey!.columnId);
      if (refTable && refCol) {
        line += ` REFERENCES ${escapeIdent(refTable.name)}(${escapeIdent(refCol.name)})`;
      }
    }
    lines.push(line);
  }

  return `-- Table: ${table.name}\nCREATE TABLE ${escapeIdent(table.name)} (\n${lines.join(',\n')}\n);`;
}

export function generateDDL(state: SchemaState): string {
  if (state.tables.length === 0) return '-- No tables defined yet';
  const sorted = topologicalSort(state.tables);
  return sorted.map(t => generateTableDDL(t, state.tables)).join('\n\n');
}
