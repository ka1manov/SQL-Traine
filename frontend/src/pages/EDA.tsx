import { useState } from 'react';
import { BarChart3, Play, AlignLeft } from 'lucide-react';
import SQLEditor from '../components/SQLEditor';
import ResultTable from '../components/ResultTable';
import { SimpleBarChart, SimpleLineChart, SimplePieChart, SimpleScatterChart } from '../components/Charts';
import { executeSQL, formatSQL } from '../utils/api';
import type { ExecuteResponse } from '../types';

type ChartType = 'bar' | 'line' | 'pie' | 'scatter' | 'auto';

function detectChartData(result: ExecuteResponse): { data: any[]; xKey: string; yKeys: string[]; suggestedType: ChartType } | null {
  if (!result || result.columns.length < 2 || result.rows.length === 0) return null;

  const numericCols: number[] = [];
  const stringCols: number[] = [];

  result.columns.forEach((_, i) => {
    const isNumeric = result.rows.every(row => row[i] === null || !isNaN(Number(row[i])));
    if (isNumeric) numericCols.push(i);
    else stringCols.push(i);
  });

  if (numericCols.length === 0) return null;

  const labelIdx = stringCols.length > 0 ? stringCols[0] : 0;
  const valueCols = numericCols.filter(i => i !== labelIdx);
  if (valueCols.length === 0) return null;

  const data = result.rows.map(row => {
    const entry: any = { name: String(row[labelIdx]) };
    valueCols.forEach(i => { entry[result.columns[i]] = Number(row[i]); });
    return entry;
  });

  const yKeys = valueCols.map(i => result.columns[i]);

  // Auto-detect chart type
  let suggestedType: ChartType = 'bar';
  if (result.rows.length <= 6 && yKeys.length === 1) suggestedType = 'pie';
  else if (result.rows.length > 10) suggestedType = 'line';
  if (numericCols.length >= 2 && stringCols.length === 0) suggestedType = 'scatter';

  return { data, xKey: 'name', yKeys, suggestedType };
}

export default function EDA() {
  const [sql, setSql] = useState("SELECT genre, COUNT(*) AS count, ROUND(AVG(duration_sec)) AS avg_duration FROM streams GROUP BY genre ORDER BY count DESC;");
  const [result, setResult] = useState<ExecuteResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [chartType, setChartType] = useState<ChartType>('auto');

  const runQuery = async () => {
    if (!sql.trim()) return;
    setLoading(true);
    try {
      const res = await executeSQL(sql);
      setResult(res);
    } catch (err: any) {
      setResult({ columns: [], rows: [], row_count: 0, error: err.message, execution_time_ms: 0 });
    } finally {
      setLoading(false);
    }
  };

  const handleFormat = async () => {
    try { setSql(await formatSQL(sql)); } catch {}
  };

  const chartData = result ? detectChartData(result) : null;
  const effectiveType = chartType === 'auto' ? (chartData?.suggestedType || 'bar') : chartType;

  return (
    <div className="p-4 space-y-4 max-w-5xl">
      <div className="flex items-center gap-2">
        <BarChart3 className="w-6 h-6 text-accent-green" />
        <h1 className="text-xl font-bold">Exploratory Data Analysis</h1>
      </div>
      <p className="text-sm text-gray-400">Write a query with multiple numeric columns for multi-series charts.</p>

      <SQLEditor value={sql} onChange={setSql} onRun={runQuery} onFormat={handleFormat} height="160px" />

      <div className="flex gap-2 flex-wrap">
        <button onClick={runQuery} disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-accent-green hover:bg-green-600 rounded-lg text-sm font-medium text-white disabled:opacity-50">
          <Play className="w-4 h-4" /> {loading ? 'Running...' : 'Run & Visualize'}
        </button>
        <button onClick={handleFormat}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-dark-card border border-dark-border rounded-lg text-xs text-gray-400 hover:bg-dark-hover">
          <AlignLeft className="w-3.5 h-3.5" /> Format
        </button>
        <select value={chartType} onChange={e => setChartType(e.target.value as ChartType)}
          className="bg-dark-card border border-dark-border rounded-lg px-3 py-1.5 text-sm text-gray-300">
          <option value="auto">Auto Detect</option>
          <option value="bar">Bar Chart</option>
          <option value="line">Line Chart</option>
          <option value="pie">Pie Chart</option>
          <option value="scatter">Scatter Plot</option>
        </select>
        {chartData && <span className="text-xs text-gray-500 self-center">{chartData.yKeys.length} series detected</span>}
      </div>

      {chartData && (
        <div className="bg-dark-card dark:bg-dark-card bg-gray-50 border border-dark-border rounded-lg p-4">
          {effectiveType === 'bar' && <SimpleBarChart data={chartData.data} yKeys={chartData.yKeys} />}
          {effectiveType === 'line' && <SimpleLineChart data={chartData.data} yKeys={chartData.yKeys} />}
          {effectiveType === 'pie' && <SimplePieChart data={chartData.data.map(d => ({ name: d.name, value: d[chartData.yKeys[0]] }))} />}
          {effectiveType === 'scatter' && <SimpleScatterChart data={chartData.data} xKey={chartData.yKeys[0]} yKey={chartData.yKeys[1] || chartData.yKeys[0]} />}
        </div>
      )}

      <ResultTable result={result} maxHeight="300px" />
    </div>
  );
}
