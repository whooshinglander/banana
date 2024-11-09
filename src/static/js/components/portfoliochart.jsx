import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const PortfolioChart = () => {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    fetch('/portfolio_values')
      .then(response => response.json())
      .then(data => {
        const formattedData = data.dates.map((date, index) => ({
          date,
          portfolioValue: Number(data.values[index].toFixed(2)),
          costBasis: Number(data.costs[index].toFixed(2))
        }));
        setChartData(formattedData);
      });
  }, []);

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 border rounded shadow">
          <p className="text-sm font-medium">{label}</p>
          <p className="text-sm text-blue-600">
            Value: ${payload[0].value.toLocaleString()}
          </p>
          <p className="text-sm text-green-600">
            Cost: ${payload[1].value.toLocaleString()}
          </p>
          <p className="text-sm text-purple-600">
            Gain/Loss: ${(payload[0].value - payload[1].value).toLocaleString()}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-2xl font-bold mb-4">Portfolio Performance</h2>
      <div className="h-96 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={chartData}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="date"
              tick={{ fontSize: 12 }}
              tickFormatter={(date) => new Date(date).toLocaleDateString()}
            />
            <YAxis
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => `$${value.toLocaleString()}`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend />
            <Line
              type="monotone"
              dataKey="portfolioValue"
              name="Portfolio Value"
              stroke="#2563eb"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 8 }}
            />
            <Line
              type="monotone"
              dataKey="costBasis"
              name="Cost Basis"
              stroke="#16a34a"
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 8 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default PortfolioChart;