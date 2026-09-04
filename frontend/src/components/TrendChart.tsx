import { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts';
import { getTrends } from '../api';
import type { TrendWeek } from '../types';

function formatWeek(dateStr: string) {
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-US', { month: 'short', year: '2-digit' });
}

export default function TrendChart() {
  const [data, setData] = useState<TrendWeek[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let ignore = false;

    getTrends()
      .then((res) => {
        if (!ignore) setData(res.trend);
      })
      .catch((err) => {
        if (!ignore) setError(err instanceof Error ? err.message : 'Failed to load trends');
      });

    return () => {
      ignore = true;
    };
  }, []);

  return (
    <div className="rounded-lg border border-[#8A8578]/20 p-6">
      <h2 className="text-lg font-semibold text-[#EDEAE2] mb-1">Weekly Threat Trends</h2>
      <p className="font-mono text-xs text-[#8A8578] mb-4">OTX data is sparse (5 of 1700 threats) — most weeks show CISA KEV only</p>

      {error && (
        <p className="font-mono text-xs text-red-400">error: {error}</p>
      )}

      {!error && !data && (
        <p className="font-mono text-xs text-[#8A8578]">loading trends...</p>
      )}

      {!error && data && data.length === 0 && (
        <p className="font-mono text-xs text-[#8A8578]">no trend data available</p>
      )}

      {!error && data && data.length > 0 && (
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={data}>
            <CartesianGrid stroke="#8A8578" strokeOpacity={0.15} vertical={false} />
            <XAxis
              dataKey="week_start"
              tickFormatter={formatWeek}
              interval="preserveStartEnd"
              minTickGap={40}
              angle={-35}
              textAnchor="end"
              height={50}
              tick={{ fill: '#8A8578', fontSize: 10, fontFamily: 'monospace' }}
              axisLine={{ stroke: '#8A8578', strokeOpacity: 0.3 }}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: '#8A8578', fontSize: 11, fontFamily: 'monospace' }}
              axisLine={{ stroke: '#8A8578', strokeOpacity: 0.3 }}
              tickLine={false}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#1A1815',
                border: '1px solid rgba(138,133,120,0.3)',
                borderRadius: 6,
                fontSize: 12,
                fontFamily: 'monospace',
                color: '#EDEAE2',
              }}
            />
            <Legend wrapperStyle={{ fontSize: 11, fontFamily: 'monospace', color: '#8A8578' }} />
            <Bar dataKey="otx"
 stackId="threats" fill="#5B8FB9" name="OTX" />
            <Bar dataKey="kev" stackId="threats" fill="#C97064" name="CISA KEV" />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  );
}
