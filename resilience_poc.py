# resilience_poc.py

import time
from typing import Callable, Any

# --- 시스템 상태 및 전역 카운터 ---
# 시뮬레이션을 위해 실패 횟수를 추적합니다.
FAILURE_THRESHOLD = 3  # 이 횟수만큼 실패하면 회로가 끊어집니다 (Circuit Breaker)
MAX_RETRIES = 3       # 최대 재시도 횟수

failure_count = 0
circuit_open = False


class DataTransferError(Exception):
    """데이터 전송 중 발생하는 시뮬레이션된 오류."""
    pass


def simulate_api_call(attempt: int) -> str:
    """
    [CORE FUNCTION] 데이터를 외부 API로 전송하는 것을 시뮬레이션합니다.
    실패 횟수를 추적하여 의도적으로 실패를 발생시킵니다.
    """
    global failure_count, circuit_open

    print(f"\n[{'='*10} Attempt {attempt} Start {'='*10}]")

    if circuit_open:
        # 회로가 열렸다면 API 호출은 불가능해야 합니다.
        raise ConnectionError("CIRCUIT OPEN: 시스템 과부하 감지. 외부 호출 차단.")

    try:
        # 시뮬레이션 로직: 3회 이내 실패, 4번째에 성공 (혹은 그 이후)
        if attempt <= FAILURE_THRESHOLD and failure_count < FAILURE_THRESHOLD * 2:
            failure_count += 1
            print(f"⚠️ [FAILURE SIMULATION] 데이터 전송 실패! (현재 실패 카운트: {failure_count}/{FAILURE_THRESHOLD*2})")
            # 일시적인 네트워크 오류나 서버 에러를 흉내냅니다.
            raise DataTransferError("서버 연결 시간 초과 또는 인증 토큰 만료.")
        else:
            # 성공 조건에 도달했습니다!
            print(f"✅ [SUCCESS] 데이터 전송 성공! (데이터 무사히 전파됨.)")
            failure_count = 0 # 성공하면 실패 카운트 초기화
            return "Data Payload Successfully Processed."

    except DataTransferError as e:
        # 예외가 발생했을 때, Circuit Breaker 상태를 업데이트합니다.
        global circuit_open
        if failure_count >= FAILURE_THRESHOLD and not circuit_open:
             print(f"\n🚨 [CIRCUIT BREAKER TRIP] 연속 {FAILURE_THRESHOLD}회 실패 감지! 회로를 열고 외부 호출을 차단합니다.")
             circuit_open = True
        raise e


def retry_with_retry_logic(func: Callable, *args, max_retries: int) -> Any:
    """
    [PATTERN 1] 일시적 장애에 대비하여 함수를 재시도하는 로직 (Retry Logic).
    """
    for attempt in range(max_retries):
        try:
            print(f"\n--- [RETRY LOGIC 실행 중] 시도 {attempt + 1} ---")
            result = func(*args, attempt=attempt + 1)
            return result # 성공하면 즉시 반환
        except DataTransferError as e:
            if attempt < max_retries - 1:
                print(f"❌ 재시도 필요: {e} -> 잠시 대기 후 재시도합니다.")
                time.sleep(0.5) # 백오프 전략 (Backoff strategy) 시뮬레이션
            else:
                # 모든 재시도가 실패했을 경우, 최종 예외를 발생시키고 Circuit Breaker가 개입하도록 유도합니다.
                raise e


def circuit_breaker_wrapper(func: Callable, *args, failure_threshold: int):
    """
    [PATTERN 2] 시스템 장애 확산을 막기 위해 API 호출 자체를 차단하는 로직 (Circuit Breaker).
    이 함수는 retry_with_retry_logic의 최상위 계층에 위치해야 합니다.
    """
    global circuit_open, failure_count

    print("\n===================================================")
    print("🚀 [CIRCUIT BREAKER AUDIT] 시스템 진단 시작")
    print(f"🎯 목표: {failure_threshold}회 연속 실패 시 호출을 차단하여 안정성 확보.")
    print("===================================================\n")

    try:
        # 1. Retry Logic으로 감싸서 실행
        result = retry_with_retry_logic(func, *args, max_retries=MAX_RETRIES)
        return result

    except ConnectionError as e:
        # Circuit Breaker에 의해 차단된 경우 (가장 심각한 상태)
        print("\n===================================================")
        print("🛑 [최종 실패] 시스템 과부하로 인한 서비스 중단을 선언합니다.")
        print(f"원인: {e}")
        print("조치: 운영팀에 알림을 보내고, 재시도 로직을 우회하여 전체 파이프라인 실행을 멈춥니다.")
        return None

    except DataTransferError as e:
        # Retry Logic에서 모든 시도가 실패하고 Circuit Breaker가 개입할 준비가 되었거나,
        # 혹은 단순히 최종적으로 처리되지 않은 오류인 경우입니다.
        print("\n===================================================")
        print(f"🛑 [최종 실패] 파이프라인 전체 프로세스 중단.")
        print("모든 재시도 시도가 실패했습니다. 외부 상태를 확인하고 수동 개입이 필요합니다.")
        return None


if __name__ == "__main__":
    # 1단계: PoC 실행 (실패 유발 -> 복구)
    print("\n\n===================================================")
    print(">>> [CASE 1] 정상적인 실패와 복구를 시도하는 과정 <<<")
    print("===================================================\n")

    final_result = circuit_breaker_wrapper(
        simulate_api_call, args=(None,), failure_threshold=FAILURE_THRESHOLD
    )

    if final_result:
        print(f"\n✅ [FINAL STATUS] PoC 성공. 최종 결과: {final_result}")
    else:
        print("\n❌ [FINAL STATUS] PoC 실패. 시스템이 복구 가능한 상태가 아닙니다.")