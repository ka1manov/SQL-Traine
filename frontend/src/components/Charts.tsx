import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, ScatterChart, Scatter,
} from 'recharts';
import { useContext } from 'react';
import { ThemeContext } from '../contexts/ThemeContext';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];

function useChartTheme() {
  const { theme } = useContext(ThemeContext);
  const isDark = theme === 'dark';
  return {
    grid: isDark ? '#1e293b' : '#e2e8f0',
    axis: isDark ? '#64748b' : '#94a3b8',
    tooltip: {
      background: isDark ? '#151c2b' : '#ffffff',
      border: `1px solid ${isDark ? '#1e293b' : '#e2e8f0'}`,
      borderRadius: 8,
    },
  };
}

interface ChartProps {
  data: Record<string, unknown>[];
  xKey?: string;
  yKey?: string;
  yKeys?: string[];
  height?: number;
}

export function SimpleBarChart({ data, xKey = 'name', yKey = 'value', yKeys, height = 300 }: ChartProps) {
  const t = useChartTheme();
  const keys = yKeys || [yKey];
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke={t.grid} />
        <XAxis dataKey={xKey} stroke={t.axis} fontSize={12} />
        <YAxis stroke={t.axis} fontSize={12} />
        <Tooltip contentStyle={t.tooltip} />
        {keys.length > 1 && <Legend />}
        {keys.map((k, i) => (
          <Bar key={k} dataKey={k} fill={COLORS[i % COLORS.length]} radius={[4, 4, 0, 0]} />
        ))}
      </BarChart>
    </ResponsiveContainer>
  );
}

export function SimpleLineChart({ data, xKey = 'name', yKey = 'value', yKeys, height = 300 }: ChartProps) {
  const t = useChartTheme();
  const keys = yKeys || [yKey];
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke={t.grid} />
        <XAxis dataKey={xKey} stroke={t.axis} fontSize={12} />
        <YAxis stroke={t.axis} fontSize={12} />
        <Tooltip contentStyle={t.tooltip} />
        {keys.length > 1 && <Legend />}
        {keys.map((k, i) => (
          <Line key={k} type="monotone" dataKey={k} stroke={COLORS[i % COLORS.length]} strokeWidth={2} dot={{ fill: COLORS[i % COLORS.length] }} />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}

export function SimplePieChart({ data, height = 300 }: { data: { name: string; value: number }[]; height?: number }) {
  const t = useChartTheme();
  return (
    <ResponsiveContainer width="100%" height={height}>
      <PieChart>
        <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
          {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
        </Pie>
        <Tooltip contentStyle={t.tooltip} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}

export function SimpleRadarChart({ data, height = 300 }: { data: Record<string, unknown>[]; height?: number }) {
  const t = useChartTheme();
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RadarChart data={data}>
        <PolarGrid stroke={t.grid} />
        <PolarAngleAxis dataKey="category" stroke={t.axis} fontSize={11} />
        <PolarRadiusAxis stroke={t.axis} fontSize={10} />
        <Radar dataKey="value" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
        <Tooltip contentStyle={t.tooltip} />
      </RadarChart>
    </ResponsiveContainer>
  );
}

export function SimpleScatterChart({ data, xKey = 'x', yKey = 'y', height = 300 }: ChartProps) {
  const t = useChartTheme();
  return (
    <ResponsiveContainer width="100%" height={height}>
      <ScatterChart>
        <CartesianGrid strokeDasharray="3 3" stroke={t.grid} />
        <XAxis dataKey={xKey} stroke={t.axis} fontSize={12} name={xKey} />
        <YAxis dataKey={yKey} stroke={t.axis} fontSize={12} name={yKey} />
        <Tooltip contentStyle={t.tooltip} />
        <Scatter data={data} fill="#3b82f6" />
      </ScatterChart>
    </ResponsiveContainer>
  );
}
