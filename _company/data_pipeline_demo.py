import time
import random
from typing import Any, Dict, Optional

# --- 1. 커스텀 예외 정의 (Exception Handling) ---
class APIError(Exception):
    """API 호출 중 발생하는 일반적인 에러."""
    pass

class TransientAPIError(APIError):
    """일시적 오류 (네트워크 불안정 등), 재시도 가능."""
    def __init__(self, message: str = "Transient connection issue"):
        super().__init__(message)

class CriticalAPIError(Exception):
    """치명적 오류 (인증 실패, 서버 다운 등), 즉시 중단 필요."""
    pass

# --- 2. Mock API Wrapper (실제 외부 시스템 모킹) ---
def mock_external_api_call(endpoint: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    외부 엔터프라이즈 시스템 또는 PayPal API 호출을 시뮬레이션합니다.
    다양한 실패 케이스를 의도적으로 유발합니다.
    """
    print(f"\n[{'='*5} Calling Mock API: {endpoint} {'='*5}]")
    time.sleep(random.uniform(0.1, 0.3)) # 네트워크 지연 시뮬레이션

    # 1. 치명적 실패 케이스 (Critical Failure)
    if "auth_fail" in endpoint:
        raise CriticalAPIError("Authentication failed. Check API keys or credentials.")
    
    # 2. 일시적 실패 케이스 (Transient/Retryable Error)
    if random.random() < 0.15: # 15% 확률로 일시적 에러 발생
        print(f"⚠️ [MOCK] Transient network failure detected on {endpoint}.")
        raise TransientAPIError("Service temporarily unavailable or timeout.")

    # 3. 사일런트 실패 케이스 (Silent Failure)
    if random.random() < 0.1: # 10% 확률로 사일런트 에러 발생
        print(f"🚨 [MOCK] SUCCESS STATUS, but data integrity check will fail.")
        # 성공적인 HTTP 응답 코드를 받았으나, 데이터 구조가 깨짐
        return {"status": "success", "data": None, "raw_payload": payload}

    # 4. 정상 성공 케이스 (Success)
    if random.random() < 0.1: # 가끔 완전히 실패하는 경우도 대비
         raise APIError(f"Unknown service error on {endpoint}.")


    print("[MOCK] ✅ Connection successful.")
    return {"status": "success", "data": payload, "raw_payload": payload}

# --- 3. Resilience Patterns Implementation ---

class CircuitBreaker:
    """시스템 과부하 방지를 위한 회로 차단기 패턴."""
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 5):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = time.monotonic()
        self._state = "CLOSED" # CLOSED, OPEN, HALF-OPEN

    def __call__(self, func, *args, **kwargs):
        current_time = time.monotonic()
        
        if self._state == "OPEN":
            if current_time - self.last_failure_time > self.recovery_timeout:
                print("\n[🛡️ CIRCUIT BREAKER] Time elapsed. Moving to HALF-OPEN state...")
                self._state = "HALF-OPEN"
            else:
                raise CriticalAPIError("Circuit is OPEN. Too many failures recently. Wait until cooldown.")

        try:
            result = func(*args, **kwargs)
            if self._state != "CLOSED": # 성공하면 상태 리셋
                print("[🛡️ CIRCUIT BREAKER] Success detected. Resetting to CLOSED state.")
                self._state = "CLOSED"
                self.failure_count = 0
            return result
        except (APIError, CriticalAPIError) as e:
            self.failure_count += 1
            if self._state == "HALF-OPEN" or self.failure_count >= self.failure_threshold:
                print(f"\n[🔥 CIRCUIT BREAKER] Failure count reached ({self.failure_count}/{self.failure_threshold}). OPENING circuit.")
                self._state = "OPEN"
                self.last_failure_time = current_time
            raise e

def execute_with_retry(func, max_retries: int = 3):
    """일시적 오류에 대비한 재시도 로직."""
    for attempt in range(max_retries):
        try:
            return func()
        except TransientAPIError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt # 지수 백오프 (Exponential Backoff)
                print(f"⏳ [RETRY] Attempt {attempt + 1} failed due to transient error. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"\n❌ [CRITICAL FAILURE] Max retries reached for Transient Error.")
                raise e # 최종적으로 재시도 실패 시 예외를 전파

# --- 4. 핵심 데이터 파이프라인 로직 (The Core Business Logic) ---

def validate_data_integrity(data: Optional[Dict[str, Any]]) -> bool:
    """
    사일런트 실패 감지 로직: API는 성공했다고 보고했으나, 실제 비즈니스 로직에 필요한 데이터가 누락되었는지 검증.
    """
    if data is None or 'status' not in data:
        print("❌ [VALIDATION FAIL] Received payload structure is invalid.")
        return False
    
    # 핵심 필드 유무 체크 (예시)
    required_fields = ['transaction_id', 'amount']
    for field in required_fields:
        if field not in data.get('raw_payload', {}):
            print(f"⚠️ [VALIDATION FAIL] Required field '{field}' missing or empty.")
            return False
            
    # 비즈니스 규칙 검증 (예시)
    if data['raw_payload'].get('amount') is None or float(data['raw_payload']['amount']) < 0:
        print("⚠️ [VALIDATION FAIL] Amount must be positive and defined.")
        return False

    return True


def run_resilient_pipeline(api_endpoint: str, payload: Dict[str, Any]):
    """
    전체 파이프라인 흐름을 관리하며 Resilience Pattern들을 적용하는 메인 함수.
    """
    print("\n" + "="*80)
    print("🚀 STARTING COMMERCIAL DATA PIPELINE AUDIT DEMO 🚀")
    print(f"  Target Endpoint: {api_endpoint}")
    print("="*80)

    # Circuit Breaker를 API 호출 함수에 적용
    circuit = CircuitBreaker()
    @circuit
    def api_call():
        # Retry Logic을 API 호출 함수에 감싸서 적용
        @execute_with_retry
        def guarded_api_call():
            return mock_external_api_call(api_endpoint, payload)

        return guarded_api_call()

    try:
        # 1. 외부 시스템과의 연결 시도 (Circuit Breaker + Retry 적용)
        raw_data = api_call()

        if raw_data is None:
            raise CriticalAPIError("Failed to retrieve any data after all retries.")

        print("\n[✅ STEP 2] Data Validation Check Running...")
        # 2. 데이터 무결성 검증 (Silent Failure Detection)
        if validate_data_integrity(raw_data):
            processed_amount = float(raw_data['raw_payload']['amount'])
            print(f"\n🎉 [SUCCESS] Pipeline completed successfully! Processed Amount: ${processed_amount:.2f}")
            return True
        else:
            # 사일런트 실패가 감지되면, 이 단계에서 비즈니스 흐름을 멈추고 알림/롤백 플로우를 시작해야 함.
            print("\n🚨 [ROLLBACK] Data integrity failure detected. Triggering manual review or compensating transaction...")
            return False

    except CriticalAPIError as e:
        print(f"\n🛑 [FAILURE FLOW] CRITICAL SYSTEM FAILURE DETECTED: {e}")
        print("   ACTION REQUIRED: System administrators must manually intervene.")
        return False
    except Exception as e:
        # 모든 예외 처리의 최종 안전망
        print(f"\n💣 [FAILURE FLOW] UNHANDLED EXCEPTION: An unexpected error occurred: {type(e).__name__}: {str(e)}")
        return False


if __name__ == "__main__":
    # --- 시나리오 1: 정상 작동 및 복구력 테스트 (Retry/Success) ---
    print("\n" + "#"*20 + " SCENARIO 1: Normal Operation & Resilience Test " + "#"*20)
    run_resilient_pipeline(
        api_endpoint="paypal/v3/transactions",
        payload={"transaction_id": "TX-1001", "amount": "150.75"}
    )

    # --- 시나리오 2: 치명적 실패 테스트 (Critical Failure / Circuit Breaker Test) ---
    print("\n\n" + "#"*20 + " SCENARIO 2: Critical API Failure & Circuit Breaker Test " + "#"*20)
    try:
        run_resilient_pipeline(
            api_endpoint="paypal/v3/auth_fail", # 이 엔드포인트는 항상 실패하도록 Mocking 함
            payload={"transaction_id": "TX-FAIL"}
        )
    except CriticalAPIError as e:
         print(f"\n[Demo Result] 성공적으로 Circuit Breaker가 작동하여 시스템을 보호했습니다. 에러 메시지: {e}")

    # --- 시나리오 3: 사일런트 실패 테스트 (Silent Failure / Validation Check Test) ---
    print("\n\n" + "#"*20 + " SCENARIO 3: Silent Failure Detection & Rollback Test " + "#"*20)
    # 이 경우 Mock API가 데이터는 주지만, validate_data_integrity에서 실패하도록 유도해야 함.
    # 테스트를 위해 임시로 payload의 amount 필드를 제거하거나 잘못된 값을 넣어 시뮬레이션할 수 있습니다.
    print("--- (주의: 이 시나리오는 무작위성에 의존하여 실행됩니다. 재실행 필요) ---")
    run_resilient_pipeline(
        api_endpoint="internal/db/sync",
        payload={"transaction_id": "TX-2003", "amount": None} # amount 필드를 None으로 설정하여 실패 유도
    )