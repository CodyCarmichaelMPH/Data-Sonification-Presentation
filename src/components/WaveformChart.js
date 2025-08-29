import React from 'react';
import Plot from 'react-plotly.js';
import styled from 'styled-components';

const ChartContainer = styled.div`
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
`;

const WaveformChart = ({ 
  data, 
  title, 
  height = 300, 
  showGrid = true, 
  yAxisTitle = 'Amplitude',
  yAxisRange,
  yAxisTicks,
  yAxisTickLabels,
  showMarkers = false
}) => {
  if (!data || !data.x || !data.y) {
    return (
      <ChartContainer>
        <div style={{ textAlign: 'center', color: '#64748b', padding: '40px' }}>
          No data available
        </div>
      </ChartContainer>
    );
  }

  const plotData = [
    {
      x: data.x,
      y: data.y,
      type: 'scatter',
      mode: showMarkers ? 'lines+markers' : 'lines',
      line: {
        color: '#3b82f6',
        width: 2
      },
      marker: showMarkers ? {
        size: 6,
        color: '#3b82f6'
      } : undefined,
      fill: showMarkers ? undefined : 'tonexty',
      fillcolor: showMarkers ? undefined : 'rgba(59, 130, 246, 0.1)',
      name: 'Waveform'
    }
  ];

  const layout = {
    title: {
      text: title,
      font: {
        size: 16,
        color: '#1e293b'
      },
      x: 0.5,
      xanchor: 'center'
    },
    height: height,
    margin: {
      l: 50,
      r: 20,
      t: 50,
      b: 50
    },
    plot_bgcolor: 'white',
    paper_bgcolor: 'white',
    showlegend: false,
    xaxis: {
      title: 'Time (s)',
      showgrid: showGrid,
      gridcolor: '#f1f5f9',
      zeroline: showMarkers,
      zerolinecolor: showMarkers ? '#e2e8f0' : undefined,
      color: '#64748b'
    },
    yaxis: {
      title: yAxisTitle,
      showgrid: showGrid,
      gridcolor: '#f1f5f9',
      zeroline: showMarkers,
      zerolinecolor: showMarkers ? '#e2e8f0' : undefined,
      color: '#64748b',
      ...(yAxisRange && { range: yAxisRange }),
      ...(yAxisTicks && { tickvals: yAxisTicks }),
      ...(yAxisTickLabels && { ticktext: yAxisTickLabels })
    },
    hovermode: 'closest'
  };

  const config = {
    displayModeBar: false,
    responsive: true
  };

  return (
    <ChartContainer>
      <Plot
        data={plotData}
        layout={layout}
        config={config}
        style={{ width: '100%', height: '100%' }}
        useResizeHandler={true}
      />
    </ChartContainer>
  );
};

export default WaveformChart;
