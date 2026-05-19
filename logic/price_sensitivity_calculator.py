<content>import math
from typing import Dict

# --- Configuration based on Designer's Rules ---
# Dynamic Color Mapping Rules (Assumed from documentation/system_blueprint_and_manual.md)
COLOR_MAP = {
    "High": {"R_factor": 1.5, "S_factor": 0.8},  # High CR: More emphasis on R (Red)
    "Medium": {"R_factor": 1.2, "S_factor": 1.0}, # Medium CR: Balanced
    "Low": {"R_factor": 0.9, "S_factor": 1.3}   # Low CR: More emphasis on S (Blue)
}

def calculate_base_ratio(R: float, S: float) -> Dict[str, float]:
    """
    기본 가격 민감도 비율을 계산합니다. (기존 로직 가정)
    실제 구현에서는 이 함수가 기존의 좌표축 R, S를 기반으로 색상 비율을 결정해야 합니다.
    임시로 기본값 설정. 실제 값은 시스템 설계에 따라 정의되어야 함.
    """
    # Placeholder for actual base ratio calculation based on R and S coordinates
    base_r = R / (R + S) if (R + S) != 0 else 0.5
    base_s = S / (R + S) if (R + S) != 0 else 0.5
    return {"R": base_r, "S": base_s}

def get_reliability_factor(reliability: float) -> Dict[str, float]:
    """
    T2A CR 신뢰도에 따른 동적 색상 매핑 규칙을 반환합니다.
    """
    if reliability > 0.8:
        return COLOR_MAP["High"]
    elif reliability > 0.5:
        return COLOR_MAP["Medium"]
    else:
        return COLOR_MAP["Low"]

def calculate_ab_test_results(R: float, S: float, cr_reliability: float) -> Dict[str, float]:
    """
    실시간으로 색상 비율을 적용하고 신뢰도 변화에 따른 A/B 테스트 결과를 계산합니다.
    R, S: 가격 민감도 맵 좌표 (Designer 확정 규칙)
    cr_reliability: T2A CR 신뢰도 시나리오 (High, Medium, Low)
    """
    base_r_s = calculate_base_ratio(R, S)
    reliability_factors = get_reliability_factor(cr_reliability)

    # 최종 색상 비율 계산
    final_r = base_r_s["R"] * reliability_factors["R_factor"]
    final_s = base_r_s["S"] * reliability_factors["S_factor"]

    return {
        "Result_R": final_r,
        "Result_S": final_s,
        "Applied_Reliability": cr_reliability,
        "Color_Map_Used": list(COLOR_MAP.keys())[list(COLOR_MAP.values()).index(reliability_factors)]
    }

# --- Test Cases for Verification (Self-Verification Loop) ---
def run_test_cases():
    print("--- Running A/B Test Result Calculation Tests ---")
    
    # Test Case 1: High Reliability Scenario
    R1, S1 = 0.7, 0.3 # Example coordinates
    cr_high = 0.95
    result_high = calculate_ab_test_results(R1, S1, cr_high)
    print(f"Test Case 1 (High Reliability={cr_high}): {result_high}")

    # Test Case 2: Medium Reliability Scenario
    R2, S2 = 0.5, 0.5
    cr_medium = 0.70
    result_medium = calculate_ab_test_results(R2, S2, cr_medium)
    print(f"Test Case 2 (Medium Reliability={cr_medium}): {result_medium}")

    # Test Case 3: Low Reliability Scenario
    R3, S3 = 0.8, 0.2
    cr_low = 0.40
    result_low = calculate_ab_test_results(R3, S3, cr_low)
    print(f"Test Case 3 (Low Reliability={cr_low}): {result_low}")

if __name__ == "__main__":
    run_test_cases()