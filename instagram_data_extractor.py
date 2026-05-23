<![
import time
import json
import random
from datetime import datetime
import os

# --- Configuration & Constants ---
S_MIN = os.getenv("S_MIN", 0.8)  # 시스템 안정성 최소 임계값 (예: 0.8)
EI_TARGET = os.getenv("EI_TARGET", 0.75) # 참여 효율 지수 목표치

def record_action_log(data):
    """행동 로그 데이터를 기록하는 함수."""
    timestamp = datetime.utcnow().isoformat() + "Z"
    # 실제 환경에서는 이 데이터를 DB 또는 별도 파일에 기록해야 함
    log_entry = {
        "timestamp": timestamp,
        "action_type": data.get("type"),
        "target_entity": data.get("entity"),
        "api_endpoint": data.get("endpoint"),
        "status_code": data.get("status", 200),
        "error_message": data.get("error", None),
        "latency_ms": data.get("latency", 0),
        "system_load_snapshot": {
            "cpu_usage": round(random.uniform(10, 80), 2), # Mock Data
            "memory_mb": round(random.uniform(50, 4096), 2)  # Mock Data
        }
    }
    # 실제로는 파일이나 DB에 기록 (여기서는 예시로 출력)
    print(f"LOGGED: {json.dumps(log_entry)}\n")
    return log_entry

def check_system_stability(all_logs):
    """수집된 로그를 기반으로 시스템 안정성(S)을 계산하는 핵심 로직."""
    if not all_logs:
        return 1.0 # 데이터가 없으면 일단 최대 안정성으로 가정 (또는 대기)

    total_calls = len(all_logs)
    failed_calls = sum(1 for log in all_logs if log["status_code"] >= 400 or log["error_message"])
    avg_latency = sum(log["latency_ms"] for log in all_logs) / total_calls

    # 단순화된 S 계산 로직 (실제 구현에서는 더 복잡한 가중치 필요)
    failure_rate = failed_calls / total_calls
    stability_score = 1.0 - (failure_rate * 0.5) - (avg_latency / 1000)

    # S 값을 0에서 1 사이로 정규화
    system_stability = max(0.0, min(1.0, stability_score))

    print(f"--- System Stability Check ---")
    print(f"Total Calls: {total_calls}, Failed Calls: {failed_calls}")
    print(f"Failure Rate: {failure_rate:.2%}")
    print(f"Avg Latency: {avg_latency:.2f}ms")
    print(f"Calculated System Stability (S): {system_stability:.4f} (Target S_MIN: {S_MIN})")

    return system_stability

def extract_data_with_validation(api_endpoint, mock_data=None):
    """데이터 추출 및 안정성 검증을 통합하는 메인 함수."""
    all_logs = []
    current_s = 1.0

    print(f"Starting extraction for endpoint: {api_endpoint}")

    for i in range(3): # 최대 3번의 재시도 시도
        try:
            # --- Step 1: Pre-flight Check (Mocked) ---
            # 실제로는 여기서 API 연결 안정성 체크 로직이 들어감.

            # --- Step 2: Execution & Logging ---
            mock_response = mock_data if mock_data else {"status": 200, "latency": random.randint(100, 500), "error": None}
            log = record_action_log(mock_response)
            all_logs.append(log)

            # --- Step 3: Post-flight Validation (Real Check Simulation) ---
            current_s = check_system_stability(all_logs)

            if current_s >= S_MIN:
                print("✅ Stability check passed for this run.")
                return True, all_logs
            else:
                print("❌ System stability dropped below threshold. Retrying...")
                time.sleep(2) # 재시도 대기

        except Exception as e:
            # LLM 호출 실패 등 예외 처리
            error_log = record_action_log({"type": "FATAL_ERROR", "endpoint": api_endpoint, "error": str(e), "status": 500})
            all_logs.append(error_log)
            print(f"🛑 Critical Error during extraction: {e}. Retrying in 2 seconds...")
            time.sleep(2)

    if not all_logs:
        return False, []

    final_s = check_system_stability(all_logs)
    print(f"\n--- Extraction Finished. Final Stability: {final_s:.4f} ---")
    return final_s >= S_MIN, all_logs

# --- Main Execution Example ---
if __name__ == "__main__":
    # Mock Data Simulation for testing the logging mechanism
    mock_data_set = [
        {"type": "poll_view", "entity": "post_123", "endpoint": "/v1/polls", "status": 200, "latency": 350},
        {"type": "post_load", "entity": "post_123", "endpoint": "/v1/posts", "status": 200, "latency": 400},
        {"type": "api_call_fail", "entity": "user_data", "endpoint": "/v1/users", "status": 503, "error": "Service Unavailable", "latency": 100}
    ]

    print("--- Running End-to-End Stability Test ---")
    success, logs = extract_data_with_validation("/api/instagram/test", mock_data=mock_data_set)

    if success:
        print("\n✅ END-TO-END TEST SUCCESSFUL. Data and Stability Logged.")
    else:
        print("\n❌ END-TO-END TEST FAILED. System stability requirement not met.")
<create_file path="requirements.txt"><![
# 필요한 라이브러리 정의
requests
# 기타 시스템 모니터링을 위한 패키지 (실제 구현 시 추가)
# psutil # 리소스 모니터링용
]]>