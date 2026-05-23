import math
from typing import Dict, Any

# --- 하이퍼파라미터 설정 (이 값들은 데이터 분석 결과에 따라 조정되어야 함) ---
K_S = 0.5  # 시스템 리스크 민감도 계수 (k_s)
S_MIN = 0.85 # 최소 시스템 안정성 임계값

def calculate_stability_factor(S: float) -> float:
    """시스템 안정성에 기반한 리스크 보정 계수를 계산합니다."""
    if S < 0:
        raise ValueError("Stability (S) cannot be negative.")
    # C_stability = (1/S) * (1 - S) 형태의 변형을 사용하여 극단적인 리스크 반영 유도
    return (1 / S) * (1 - S)

def calculate_price_sensitivity(EI: float, stability_factor: float) -> float:
    """참여 효율과 안정성 기반으로 가격 민감도를 계산합니다."""
    # EI가 높을수록 민감도가 커지지만, 안정성이 낮으면 그 민감도는 보수적으로 조정됨.
    return EI * (1 + K_S * stability_factor)

def determine_revenue_stream(SWRI: float, price_sensitivity: float, EI: float, S: float) -> Dict[str, Any]:
    """S, EI, SWRI를 통합하여 최적의 매출 구조를 제안합니다."""
    results = {
        "Optimal_Strategy": "Unknown",
        "Recommended_Pricing_Model": "Standard Linear Pricing",
        "Revenue_Stream_Proposal": "Base Model",
        "Risk_Assessment": f"S={S:.2f}, EI={EI:.2f}"
    }

    if S < S_MIN:
        results["Risk_Assessment"] += " - **CRITICAL RISK** (S below threshold)"
        # 시스템 안정성이 낮을 경우, 리스크 회피 우선 전략으로 전환
        results["Optimal_Strategy"] = "Risk Aversion & Stability Focus"
        results["Recommended_Pricing_Model"] = "Tiered Subscription with Low Entry Barrier"
        results["Revenue_Stream_Proposal"] = "Segmented SaaS/Subscription"
    elif price_sensitivity > 1.5 and EI > 0.7:
        # 가격 민감도가 높고 참여 효율이 높을 경우, 공격적 수익 극대화 전략
        results["Optimal_Strategy"] = "Aggressive Profit Maximization"
        results["Recommended_Pricing_Model"] = "Premium Value-Based Pricing"
        results["Revenue_Stream_Proposal"] = "High-Tier Service Bundle"
    else:
        # 표준 운영 모드
        results["Optimal_Strategy"] = "Balanced Growth & Stability"
        results["Recommended_Pricing_Model"] = "Value-Based Tiered Pricing"
        results["Revenue_Stream_Proposal"] = "Hybrid Model (Ads/Subscription)"

    return results

if __name__ == "__main__":
    # --- 테스트 시나리오 1: 이상적인 경우 (High S, High EI) ---
    print("--- 시나리오 1: 안정적이고 효율적인 환경 ---")
    S_good = 0.95
    EI_good = 0.85
    SWRI_base = 100000 # 기준 수익 잠재력

    stability = calculate_stability_factor(S_good)
    sensitivity = calculate_price_sensitivity(EI_good, stability)
    stream_good = determine_revenue_stream(SWRI_base, sensitivity, EI_good, S_good)
    print(f"시스템 안정성 보정 계수: {stability:.4f}")
    print(f"가격 민감도: {sensitivity:.4f}")
    print("최종 매출 구조 제안:")
    import json
    print(json.dumps(stream_good, indent=2, ensure_ascii=False))

    print("\n" + "="*50 + "\n")

    # --- 테스트 시나리오 2: 불안정한 환경 (Low S, High EI) ---
    print("--- 시나리오 2: 시스템 안정성 리스크가 있는 환경 ---")
    S_bad = 0.60 # 임계값(0.85) 미달
    EI_high = 0.90
    SWRI_base = 100000

    stability = calculate_stability_factor(S_bad)
    sensitivity = calculate_price_sensitivity(EI_high, stability)
    stream_bad = determine_revenue_stream(SWRI_base, sensitivity, EI_high, S_bad)
    print(f"시스템 안정성 보정 계수: {stability:.4f}")
    print(f"가격 민감도: {sensitivity:.4f}")
    print("최종 매출 구조 제안:")
    print(json.dumps(stream_bad, indent=2, ensure_ascii=False))