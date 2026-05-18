# 🎨 Final Visual System Protocol

## 1. T2A CR 기반 색상 대비 변수 매핑 (Figma Mapping)
핵심 목표는 행동 로그의 긴장감 레벨(T2A CR)에 따라 딥 블루와 크림슨 레드의 대비 강도를 동적으로 변화시키는 것입니다.

**🎨 팔레트 정의:**
*   **Primary Color (Deep Blue, 안정성/신뢰):** `#0A183B` (Hex)
*   **Accent Color (Crimson Red, 행동 유도/긴장감):** `#C82D49` (Hex)

**📊 변수 매핑 규칙:**
T2A CR 값(0.0 ~ 1.0)을 기반으로 두 색상의 대비 강도를 조절합니다.

| T2A CR 레벨 | 시각적 긴장감 레벨 | Primary Color (Deep Blue) 적용 | Accent Color (Crimson Red) 적용 | 대비 강도 목표 |
| :---: | :---: | :--- | :--- | :---: |
| **0.1 - 0.3** | Low Tension (안정/정보 제공) | `#0A183B` (95% 채도 유지) | `#C82D49` (70% 명도 증가, 부드러운 대비) | Medium-Low |
| **0.4 - 0.7** | Medium Tension (분석/인지) | `#0A183B` (85% 채도 유지) | `#C82D49` (100% 명도, 표준 대비) | Medium |
| **0.8 - 1.0** | High Tension (행동 유도/위험 인지) | `#0A183B` (75% 채도 감소, 깊이 강조) | `#C82D49` (최대 명도 대비, 강한 시각적 충돌) | High |

**💡 Figma 적용 규칙:**
모든 디자인 컴포넌트는 다음과 같은 **변수 그룹(Color Variables)**을 정의해야 합니다.

1.  **`Tension_Level` (Number):** 0.0에서 1.0 사이의 동적 값. (데이터 파이프라인으로부터 입력)
2.  **`Primary_Color_Luminance` (Number):** T2A CR에 따라 Primary Color의 명도 변화율을 제어합니다. (예: $1 - (\text{Tension\_Level} \times 0.15)$)
3.  **`Accent_Contrast_Ratio` (Number):** Accent Color와 Primary Color 간의 실제 대비 비율을 동적으로 계산하여 적용합니다.

## 2. 디자인 실행 시 필수 메타데이터 포함 규칙 (Metadata Protocol)

모든 최종 산출물은 다음 필드를 반드시 포함해야 합니다. 이 메타데이터는 데이터 파이프라인의 정확성($\text{T2A CR}$)과 시각적 전략($\text{Blueprint}$)을 추적하는 데 사용됩니다.

**📝 필수 메타데이터 구조:**
모든 디자인 파일(JSON 또는 별도 `.md` 파일)은 다음 필드를 포함해야 합니다.

1.  **`Design_ID` (String):** 해당 디자인의 고유 식별자. (예: `thumb_v1`, `lp_hero_section`)
2.  **`Tension_Value` (Number):** 이 디자인이 기반한 행동 로그의 T2A CR 값. (0.0 ~ 1.0)
3.  **`Design_Phase` (String):** 현재 단계 구분. (예: `Concept`, `Draft`, `Final`)
4.  **`Visual_Strategy` (String):** 적용된 핵심 프레임워크. (예: `Blueprint_Focus`, `Resilience_Emphasis`)
5.  **`Color_Mapping_Applied` (String):** 적용된 색상 변수 규칙. (예: `Tension_High_Mode`)
6.  **`Action_Flow_Link` (String/URL):** 해당 디자인이 연결되는 행동 로그의 경로. (코다리 시스템과의 연동 증명)