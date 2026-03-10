import { AlertTriangle } from 'lucide-react';
import type { DiffResult } from '../types';

interface Props {
  diff: DiffResult;
}

export default function DiffView({ diff }: Props) {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-4 text-sm">
        <span className="text-gray-400">Match:</span>
        <div className="flex-1 bg-dark-card dark:bg-dark-card bg-gray-200 rounded-full h-3 overflow-hidden">
          <div
            className={`h-full rounded-full transition-all ${
              diff.match_pct === 100 ? 'bg-accent-green' : diff.match_pct >= 50 ? 'bg-accent-yellow' : 'bg-accent-red'
            }`}
            style={{ width: `${diff.match_pct}%` }}
          />
        </div>
        <span className={`font-bold ${
          diff.match_pct === 100 ? 'text-accent-green' : diff.match_pct >= 50 ? 'text-accent-yellow' : 'text-accent-red'
        }`}>
          {diff.match_pct}%
        </span>
      </div>

      {/* Warnings */}
      {diff.match_pct === 100 && !diff.order_correct && (
        <div className="flex items-center gap-2 bg-yellow-900/10 dark:bg-yellow-900/10 bg-yellow-50 border border-yellow-800/30 dark:border-yellow-800/30 border-yellow-200 rounded-lg p-2.5 text-yellow-400 dark:text-yellow-400 text-yellow-600 text-xs">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          Row ordering differs from expected. Check your ORDER BY clause.
        </div>
      )}
      {!diff.column_order_match && (
        <div className="flex items-center gap-2 bg-blue-900/10 dark:bg-blue-900/10 bg-blue-50 border border-blue-800/30 dark:border-blue-800/30 border-blue-200 rounded-lg p-2.5 text-blue-400 dark:text-blue-400 text-blue-600 text-xs">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          Column order differs. Expected: {diff.expected_columns.join(', ')}
        </div>
      )}

      {diff.missing_rows.length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-red-400 mb-1">Missing Rows ({diff.missing_rows.length})</h4>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr>{diff.expected_columns.map((c, i) => <th key={i} className="px-2 py-1 text-left text-gray-500 bg-red-900/10">{c}</th>)}</tr>
              </thead>
              <tbody>
                {diff.missing_rows.slice(0, 10).map((row, ri) => (
                  <tr key={ri} className="bg-red-900/5 border-b border-dark-border/30">
                    {row.map((cell, ci) => <td key={ci} className="px-2 py-1 text-red-300 whitespace-nowrap">{cell === null ? 'NULL' : String(cell)}</td>)}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {diff.extra_rows.length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-yellow-400 mb-1">Extra Rows ({diff.extra_rows.length})</h4>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr>{diff.actual_columns.map((c, i) => <th key={i} className="px-2 py-1 text-left text-gray-500 bg-yellow-900/10">{c}</th>)}</tr>
              </thead>
              <tbody>
                {diff.extra_rows.slice(0, 10).map((row, ri) => (
                  <tr key={ri} className="bg-yellow-900/5 border-b border-dark-border/30">
                    {row.map((cell, ci) => <td key={ci} className="px-2 py-1 text-yellow-300 whitespace-nowrap">{cell === null ? 'NULL' : String(cell)}</td>)}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {diff.matching_rows.length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-green-400 mb-1">Matching Rows ({diff.matching_rows.length})</h4>
          <div className="overflow-x-auto">
            <table className="w-full text-xs">
              <thead>
                <tr>{diff.actual_columns.map((c, i) => <th key={i} className="px-2 py-1 text-left text-gray-500 bg-green-900/10">{c}</th>)}</tr>
              </thead>
              <tbody>
                {diff.matching_rows.slice(0, 5).map((row, ri) => (
                  <tr key={ri} className="bg-green-900/5 border-b border-dark-border/30">
                    {row.map((cell, ci) => <td key={ci} className="px-2 py-1 text-green-300 whitespace-nowrap">{cell === null ? 'NULL' : String(cell)}</td>)}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
