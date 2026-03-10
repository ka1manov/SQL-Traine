import { Clock } from 'lucide-react';
import type { ExecuteResponse } from '../types';

interface Props {
  result: ExecuteResponse | null;
  maxHeight?: string;
}

export default function ResultTable({ result, maxHeight = '300px' }: Props) {
  if (!result) return null;

  if (result.error) {
    return (
      <div className="bg-red-900/20 dark:bg-red-900/20 bg-red-50 border border-red-800 dark:border-red-800 border-red-200 rounded-lg p-4 text-red-400 dark:text-red-400 text-red-600 text-sm font-mono">
        {result.error}
      </div>
    );
  }

  if (result.columns.length === 0) {
    return (
      <div className="text-gray-500 text-sm p-4">Query executed successfully. No rows returned.</div>
    );
  }

  return (
    <div className="border border-dark-border dark:border-dark-border border-gray-200 rounded-lg overflow-hidden">
      <div className="overflow-auto" style={{ maxHeight }}>
        <table className="w-full text-sm">
          <thead className="bg-dark-surface dark:bg-dark-surface bg-gray-50 sticky top-0">
            <tr>
              {result.columns.map((col, i) => (
                <th key={i} className="px-3 py-2 text-left text-gray-400 dark:text-gray-400 text-gray-600 font-medium border-b border-dark-border dark:border-dark-border border-gray-200 whitespace-nowrap">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {result.rows.map((row, ri) => (
              <tr key={ri} className="hover:bg-dark-hover dark:hover:bg-dark-hover hover:bg-gray-50 border-b border-dark-border/50 dark:border-dark-border/50 border-gray-100">
                {row.map((cell, ci) => (
                  <td key={ci} className="px-3 py-1.5 whitespace-nowrap text-gray-300 dark:text-gray-300 text-gray-700">
                    {cell === null ? <span className="text-gray-600 dark:text-gray-600 text-gray-400 italic">NULL</span> : String(cell)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="px-3 py-1.5 bg-dark-surface dark:bg-dark-surface bg-gray-50 text-gray-500 text-xs border-t border-dark-border dark:border-dark-border border-gray-200 flex items-center justify-between">
        <span>{result.row_count} row{result.row_count !== 1 ? 's' : ''}{result.total_rows ? ` of ${result.total_rows}` : ''}</span>
        {result.execution_time_ms > 0 && (
          <span className="flex items-center gap-1 text-gray-600">
            <Clock className="w-3 h-3" />
            {result.execution_time_ms}ms
          </span>
        )}
      </div>
    </div>
  );
}
