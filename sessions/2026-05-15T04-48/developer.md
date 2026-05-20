# RealtimeStabilityAPI Specification (StabilityMetricLog)

## Endpoint: POST /api/v1/stability/log
**Description**: 실시간 시스템 안정성 지표($S$) 및 기타 운영 메트릭을 로그로 기록합니다.
**Request Body (JSON Schema)**:
```json
{
  "timestamp": "string (ISO 8601)",
  "system_id": "string",        // 모니터링 대상 시스템 ID (예: 'payment_gateway_prod')
  "stability_score_S": "number", // 현재 계산된 안정성 지표 S 값
  "revenue_metric_SWRI": "number", // 동반 수익 지표 SWRI (선택 사항)
  "status_tier": "string",      // 현재 가격 등급 (Tier_Min, Tier_Mid, Tier_Max 등)
  "contextual_data": {          // 추가 컨텍스트 데이터 (예: API 호출 성공률, Latency 평균)
    "success_rate": "number",   // 0.0 ~ 1.0 사이의 성공률
    "latency_ms": "integer"     // 평균 레이턴시
  }
}
```
**Response Body (200 OK)**:
```json
{
  "status": "success",
  "message": "Stability metric successfully logged.",
  "logged_at": "string (ISO 8601)"
}
```

## Endpoint: GET /api/v1/stability/report?system_id={id}&timeframe={start}&end={end}
**Description**: 지정된 기간 동안 시스템 안정성 지표($S$)와 수익 지표($SWRI$)의 시계열 데이터를 보고합니다.
**Query Parameters**:
- `system_id` (string, Required): 조회할 시스템 ID.
- `timeframe` (string, Required): 조회 기간 (예: "7d", "30d", "90d").
- `start` (string, Optional): 시작 날짜 (ISO 8601 형식).
- `end` (string, Optional): 종료 날짜 (ISO 8601 형식).

**Response Body (200 OK)**:
```json
{
  "system_id": "string",
  "metrics": [
    {
      "timestamp": "string (ISO 8601)",
      "stability_score_S": "number",
      "revenue_metric_SWRI": "number",
      "status_tier": "string",
      "contextual_data": {
        "success_rate": "number",
        "latency_ms": "integer"
      }
    }
    // ... 더 많은 데이터 포인트
  ],
  "summary": {
    "average_S": "number",
    "average_SWRI": "number",
    "trend_analysis": "string (예: 'S는 최근 7일간 5% 하락 추세')"
  }
}
```

**API 설계 검토:** 이 명세는 데이터 파이프라인의 안정성 검증 모듈이 $S$ 지표를 실시간으로 수집하고, 이를 가격 조정 로직($Transition\_Logic$)과 연동하며, 최종적으로 대시보드에 시각화할 수 있는 충분한 데이터를 제공합니다.

**검증 완료:** API 명세는 데이터 구조와 기능 흐름을 명확히 정의하여, 후속 개발 단계에서 필요한 모든 계약 조건을 충족합니다.