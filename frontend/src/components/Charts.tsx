import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, ScatterChart, Scatter,
} from 'recharts';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];

interface ChartProps {
  data: any[];
  xKey?: string;
  yKey?: string;
  yKeys?: string[];
  height?: number;
}

export function SimpleBarChart({ data, xKey = 'name', yKey = 'value', yKeys, height = 300 }: ChartProps) {
  const keys = yKeys || [yKey];
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
        <XAxis dataKey={xKey} stroke="#64748b" fontSize={12} />
        <YAxis stroke="#64748b" fontSize={12} />
        <Tooltip contentStyle={{ background: '#151c2b', border: '1px solid #1e293b', borderRadius: 8 }} />
        {keys.length > 1 && <Legend />}
        {keys.map((k, i) => (
          <Bar key={k} dataKey={k} fill={COLORS[i % COLORS.length]} radius={[4, 4, 0, 0]} />
        ))}
      </BarChart>
    </ResponsiveContainer>
  );
}

export function SimpleLineChart({ data, xKey = 'name', yKey = 'value', yKeys, height = 300 }: ChartProps) {
  const keys = yKeys || [yKey];
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
        <XAxis dataKey={xKey} stroke="#64748b" fontSize={12} />
        <YAxis stroke="#64748b" fontSize={12} />
        <Tooltip contentStyle={{ background: '#151c2b', border: '1px solid #1e293b', borderRadius: 8 }} />
        {keys.length > 1 && <Legend />}
        {keys.map((k, i) => (
          <Line key={k} type="monotone" dataKey={k} stroke={COLORS[i % COLORS.length]} strokeWidth={2} dot={{ fill: COLORS[i % COLORS.length] }} />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}

export function SimplePieChart({ data, height = 300 }: { data: { name: string; value: number }[]; height?: number }) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <PieChart>
        <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label>
          {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
        </Pie>
        <Tooltip contentStyle={{ background: '#151c2b', border: '1px solid #1e293b', borderRadius: 8 }} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}

export function SimpleRadarChart({ data, height = 300 }: { data: any[]; categories?: string[]; height?: number }) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RadarChart data={data}>
        <PolarGrid stroke="#1e293b" />
        <PolarAngleAxis dataKey="category" stroke="#64748b" fontSize={11} />
        <PolarRadiusAxis stroke="#64748b" fontSize={10} />
        <Radar dataKey="value" stroke="#3b82f6" fill="#3b82f6" fillOpacity={0.3} />
        <Tooltip contentStyle={{ background: '#151c2b', border: '1px solid #1e293b', borderRadius: 8 }} />
      </RadarChart>
    </ResponsiveContainer>
  );
}

export function SimpleScatterChart({ data, xKey = 'x', yKey = 'y', height = 300 }: ChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <ScatterChart>
        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
        <XAxis dataKey={xKey} stroke="#64748b" fontSize={12} name={xKey} />
        <YAxis dataKey={yKey} stroke="#64748b" fontSize={12} name={yKey} />
        <Tooltip contentStyle={{ background: '#151c2b', border: '1px solid #1e293b', borderRadius: 8 }} />
        <Scatter data={data} fill="#3b82f6" />
      </ScatterChart>
    </ResponsiveContainer>
  );
}
