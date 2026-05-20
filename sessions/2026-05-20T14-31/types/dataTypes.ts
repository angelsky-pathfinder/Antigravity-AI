<![CDATA[
export interface CorrelationPoint {
  stability: number; // S 지표 (0-100%)
  profit: number;     // SWRI 지표
  status: 'optimal' | 'warning' | 'critical'; // 현재 상태 기반 색상 결정
}

export interface CorrelationResult extends CorrelationPoint {
  calculatedStatus: 'optimal' | 'warning' | 'critical';
  color: string; // 적용된 최종 색상 코드
}
]]>