# A/B 테스트 결과 계산 로직 명세 (T2A CR 기반)

## 1. 목표 및 입력 정의
**목표:** T2A CR 신뢰도 변화 시나리오(High, Medium, Low)에 따른 실제 썸네일 A/B 테스트 결과를 예측하고 최적 가격을 산출하는 로직 개발 착수 준비.
**핵심 입력 변수:**
1.  $T_{CR}$: 현재 T2A CR 신뢰도 (High, Medium, Low 중 하나)
2.  $R$: 가격 민감도 맵의 수평 좌표축 값 (0~100 범위 가정)
3.  $S$: 가격 민감도 맵의 수직 좌표축 값 (0~100 범위 가정)
4.  $\text{Baseline Data}$: 기준이 되는 영상/릴스 초기 반응 데이터 (클릭률, 전환율 등)

## 2. T2A CR 시나리오별 가중치 매핑 (Designer Input)
T2A CR의 신뢰도 변화에 따라 가격 민감도를 해석하는 가중치를 정의합니다. 이 값들은 $R$과 $S$를 변환하여 최종 위험 점수 및 승률 계산에 사용됩니다.

| T2A CR 시나리오 | 가격 민감도 해석 (Mapping Rule) | 위험 감수 수준 ($W_{Risk}$) | 최적 가격 조정 계수 ($\alpha$) |
| :--- | :--- | :--- | :--- |
| **High** | 높은 신뢰도. 안정적인 수익 추구. | $W_{Risk} = 0.2$ (낮음) | $\alpha = 1.0$ (기준 가격 유지) |
| **Medium** | 중간 신뢰도. 균형 잡힌 접근. | $W_{Risk} = 0.5$ (중간) | $\alpha = 1.2$ (약간의 공격적 조정) |
| **Low** | 낮은 신뢰도. 리스크 회피 중시. | $W_{Risk} = 0.8$ (높음) | $\alpha = 1.5$ (보수적 가격 책정) |

## 3. A/B 테스트 결과 산출 로직 (Algorithm Blueprint)
최종 A/B 테스트 결과($\text{Result}$)는 다음 공식을 기반으로 계산됩니다.

$$\text{Risk Score} = (\text{Baseline Loss Rate}) \times W_{Risk} + (R \times S \times \alpha)$$

1.  **$\text{Loss Rate}$ 산출:** $\text{Loss Rate} = f(\text{Baseline Data}, T_{CR})$
    *   $T_{CR}=\text{High}$: $\text{Loss Rate} = \text{Baseline Loss Rate} \times 0.5$
    *   $T_{CR}=\text{Medium}$: $\text{Loss Rate} = \text{Baseline Loss Rate}$
    *   $T_{CR}=\text{Low}$: $\text{Loss Rate} = \text{Baseline Loss Rate} \times 1.5$

2.  **최적 가격 ($\mathbf{P_{opt}}$) 산출:** $P_{opt}$는 위험 점수($\text{Risk Score}$)를 최소화하는 지점을 찾습니다.
    $$P_{opt} = P_{current} - (\beta \times \text{Risk Score})$$
    *   $\beta$: 가격 민감도에 따른 민감도 상수 (Designer가 최종 설정)

3.  **A/B 테스트 승률 예측:** $T_{CR}$ 상태에 따라 $\text{Loss Rate}$를 보정하여 최종 예상 전환율을 산출합니다.
    $$\text{Predicted Conversion} = \text{Baseline Conversion} - (\text{Risk Score} \times \gamma)$$
    *   $\gamma$: 위험 감수 계수 ($\gamma$는 $W_{Risk}$와 연동)

## 4. 디자인 및 구현 지침 (Designer Implementation Notes)
*   **색상 매핑 규칙 적용:** $\alpha$ 값($1.0, 1.2, 1.5$)에 따라 시각화된 가격 민감도 맵의 색상 분포를 동적으로 조정해야 합니다. 예를 들어, $T_{CR}=\text{Low}$일 때는 $R \times S$ 값이 동일하더라도 더 높은 위험 점수로 표시되어야 합니다.
*   **데이터 흐름:** 입력($R, S, T_{CR}$) $\rightarrow$ 가중치 적용 ($W_{Risk}, \alpha$) $\rightarrow$ 위험 점수 계산 $\rightarrow$ 최적 가격 및 승률 예측 결과 산출의 논리적 순서를 엄격히 따릅니다.
*   **최종 목표:** 코다리는 위 명세에 따라 실제 데이터 입력 시뮬레이션 및 로직 구현을 시작해야 합니다.