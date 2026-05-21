# 백엔드 API 명세 보완: $S$와 $SWRI$ 후크 전략 반영 (최종)

## 1. 데이터 모델 수정
기존 `SystemMetricsResponse`를 확장하여 안정성과 수익 간의 연관성을 명시합니다.

```python
class StatusData(BaseModel):
    stability: float  # S: System Stability (0.0 ~ 1.0)
    revenue_index: float # SWRI: Revenue Index
    stability_impact_factor: float # S가 SWRI에 미치는 영향력 계수 (0.0 ~ 1.0)
    risk_adjusted_revenue: float # S를 반영한 실질 위험 조정 수익 지표

class SystemMetricsResponse(BaseModel):
    status: str
    metrics: StatusData
```

## 2. 비즈니스 로직 정의 (핵심 후크)
$S$와 $SWRI$의 관계는 다음 공식으로 정의됩니다. 이 공식은 시스템 안정성이 낮을 때 수익 잠재력이 얼마나 보정되어야 하는지를 결정합니다.

$$ SWRI_{\text{adj}} = SWRI \times (1 - \alpha \cdot (1 - S)) $$
*   **변수 설명:**
    *   $SWRI$: 기본 수익 지표.
    *   $S$: 시스템 안정성 ($0 \le S \le 1$).
    *   $\alpha$: 비즈니스 민감도 계수. 이는 운영 환경에 따라 설정되며, **최소값은 0.1, 최대값은 1.0**으로 제한합니다. (예: $\alpha = 0.5$)

## 3. API 엔드포인트 구현 지침
`get_system_metrics()` 함수는 실제 데이터(PostgreSQL/Redis)에서 $S$와 $SWRI$를 가져온 후, 위 공식에 따라 `risk_adjusted_revenue`를 계산하여 반환해야 합니다. 이 계산 결과가 최종 비즈니스 의사결정의 핵심 지표가 됩니다.