<![CDATA[
import React from 'react';
import { ScatterPlotData, CorrelationResult } from '../types/dataTypes'; // 타입 정의는 추후 생성 예정

// 🎨 Designer가 확정한 색상 팔레트 정의
const COLORS = {
  stability: '#0A3D62',      // Deep Blue (안정성)
  risk: '#C11B1B',           // Crimson Red (위험/기회)
  neutral: '#F5F5F5',        // Light Gray (배경)
  success: '#4CAF50',        // Green (최적 상태)
};

interface CorrelationPoint {
  stability: number; // S 지표 (0-100%)
  profit: number;     // SWRI 지표
  status: 'optimal' | 'warning' | 'critical'; // 현재 상태 기반 색상 결정
}

interface DashboardVisualizationProps {
  data: CorrelationPoint[];
  title: string;
  stabilityThresholds: { minS: number; midS: number; maxS: number };
}

const DashboardVisualization: React.FC<DashboardVisualizationProps> = ({ data, title, stabilityThresholds }) => {

  // 📊 핵심 상관관계 계산 로직 (실제 구현은 다음 단계에서 데이터 파이프라인에 의존)
  const calculateCorrelation = (point: CorrelationPoint): CorrelationResult => {
    let status: 'optimal' | 'warning' | 'critical';
    if (point.stability >= stabilityThresholds.midS && point.profit > 0) {
      status = 'optimal';
    } else if (point.stability < stabilityThresholds.minS || point.stability > stabilityThresholds.maxS) {
      status = 'critical'; // 임계값 이탈 시 위험
    } else if (point.profit < 0 && point.stability > stabilityThresholds.midS) {
      status = 'warning'; // 안정적이지만 수익이 낮은 상태
    } else {
      status = 'optimal';
    }

    return {
      ...point,
      calculatedStatus: status,
      color: COLORS[status === 'optimal' ? 'success' : status === 'warning' ? 'risk' : 'risk'],
    };
  };

  const processedData = data.map(calculateCorrelation);

  // 🎨 시각화 요소 반환 (실제 차트 라이브러리 연동 지점)
  return (
    <div className="dashboard-visualization">
      <h1>{title} - S vs SWRI 상관관계</h1>
      <p>기준: $S_{\min}={stabilityThresholds.minS}$, $S_{\text{mid}}={stabilityThresholds.midS}$, $S_{\max}={stabilityThresholds.maxS}$</p>

      <div className="chart-container">
        {/* 📈 Scatter Plot Placeholder */}
        <div className="scatter-plot" style={{ backgroundColor: COLORS.neutral, border: `1px solid ${COLORS.stability}` }}>
          {processedData.map((point, index) => (
            <div
              key={index}
              style={{
                position: 'absolute',
                left: `${(point.stability / 100) * 100}%`,
                top: `${(100 - (point.profit / 50))}%`, // Y축 반전 예시
                width: '10px',
                height: '10px',
                backgroundColor: point.color,
                border: `2px solid ${point.color === COLORS.risk ? '#FFF' : COLORS.stability}`,
                borderRadius: '50%',
              }}
              title={`S: ${point.stability.toFixed(1)}%, SWRI: ${point.profit.toFixed(2)} (${point.calculatedStatus})`}
            />
          ))}
        </div>

        {/* 🎯 핵심 지표 요약 카드 */}
        <div className="summary-cards">
          <div style={{ border: `2px solid ${COLORS.stability}`, padding: '15px', margin: '10px', backgroundColor: COLORS.stability }}>
            <h2>시스템 안정성 평균</h2>
            <p>평균 $S$: {data.reduce((sum, p) => sum + p.stability, 0) / data.length.toFixed(2)}%</p>
          </div>
          <div style={{ border: `2px solid ${COLORS.risk}`, padding: '15px', margin: '10px', backgroundColor: COLORS.risk }}>
            <h2>수익 평균</h2>
            <p>평균 $SWRI$: {data.reduce((sum, p) => sum + p.profit, 0) / data.length.toFixed(2)}</p>
          </div>
        </div>

      </div>
    </div>
  );
};

export default DashboardVisualization;
]]>