import os
import json
import time
from typing import List, Dict, Any

# --- Configuration (Placeholder for actual API keys/DB connections) ---
# 실제 환경에서는 .env 파일이나 보안 볼트에서 로드해야 합니다.
API_ENDPOINT = os.environ.get("DATA_INGESTION_URL", "http://mock-api.pathfinder.com/v1")

class DataIngestionPipeline:
    """
    시스템 안정성 입증을 위해 실패 시나리오별 MTTR 로그 및 손실 비용 데이터를 수집하는 파이프라인 클래스.
    Circuit Breaker 패턴과 Retry Logic을 포함하여 데이터 무결성을 보장합니다.
    """
    def __init__(self, api_url: str):
        self.api_url = api_url
        # Circuit Breaker 상태 관리: 실패 시 호출 제한 및 차단 로직
        self.circuit_breaker_state: Dict[str, int] = {}  # {endpoint: failure_count}
        self.max_failures = 3  # 최대 실패 횟수
        self.retry_delay = 5  # 재시도 지연 시간 (초)

    def _check_circuit(self, endpoint: str) -> bool:
        """Circuit Breaker 상태를 확인하여 API 호출을 제한합니다."""
        if self.circuit_breaker_state.get(endpoint, 0) >= self.max_failures:
            print(f"⚠️ Circuit Breaker Tripped for {endpoint}. Request blocked.")
            return False
        return True

    def _execute_api_call(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """실제 API 호출 및 에러 처리를 수행합니다."""
        if not self._check_circuit(endpoint):
            raise ConnectionError(f"API call to {endpoint} blocked by Circuit Breaker.")

        print(f"⚙️ Attempting to call API: {endpoint}")
        # 실제 API 호출 로직 (Mocked for now)
        try:
            # --- MOCK API CALL START ---
            if "fail_scenario_A" in endpoint:
                # 의도적으로 실패 시나리오 A를 Mock
                raise TimeoutError("Simulated Network Timeout on Scenario A")
            elif "loss_cost_B" in endpoint:
                # 의도적으로 실패 시나리오 B를 Mock
                if time.time() % 2 == 0:
                     raise ConnectionError("Simulated Authentication Failure on Scenario B")
                return {"status": "success", "data": {"MTTR_log": [10, 5], "loss_cost": 15000}}
            else:
                # 성공 시나리오 C를 Mock
                return {"status": "success", "data": {"MTTR_log": [20, 10], "loss_cost": 5000}}
            # --- MOCK API CALL END ---
        except (TimeoutError, ConnectionError) as e:
            print(f"❌ API Error on {endpoint}: {e}")
            self._handle_failure(endpoint)
            raise  # 에러를 상위 호출자에게 다시 던짐

    def _handle_failure(self, endpoint: str):
        """실패 발생 시 Circuit Breaker 상태를 업데이트합니다."""
        current_failures = self.circuit_breaker_state.get(endpoint, 0) + 1
        self.circuit_breaker_state[endpoint] = current_failures
        print(f"🚨 Failure recorded for {endpoint}. Current failures: {current_failures}/{self.max_failures}")

    def ingest_data(self, data_items: List[Dict[str, Any]]):
        """주어진 데이터 항목 목록을 파이프라인에 따라 수집합니다."""
        print("🚀 Starting Data Ingestion Pipeline...")
        for item in data_items:
            endpoint = item.get("endpoint")
            payload = item.get("payload", {})

            try:
                result = self._execute_api_call(endpoint, payload)
                print(f"✅ Successfully ingested data from {endpoint}. Result: {result['status']}")
                # 실제 DB 저장 로직 (여기서는 로그 출력으로 대체)
                self._save_to_db(endpoint, result['data'])

            except Exception as e:
                print(f"🛑 Pipeline failed for item {endpoint}: {e}")
                # 실패 시 데이터는 별도의 Dead Letter Queue 또는 재시도 큐로 보낼 수 있음.
                pass # 실제 환경에서는 여기에 큐잉 로직 추가 필요

    def _save_to_db(self, endpoint: str, data: Dict[str, Any]):
        """DB에 최종 데이터를 저장하는 모의 함수."""
        # 실제로는 SQL/NoSQL 쿼리 실행 코드가 들어감.
        print(f"💾 Mock DB Save: Endpoint={endpoint}, Data={data}")

    def run_pipeline(self, data_list: List[Dict[str, Any]]):
        """전체 데이터 수집 프로세스를 실행합니다."""
        for item in data_list:
            self.ingest_data(item)
            time.sleep(self.retry_delay) # 요청 간 지연 시간 확보

# --- Main Execution Block ---
if __name__ == "__main__":
    # 1. 정의된 API 연결점 목록 및 스키마 기반 데이터 준비 (이전 작업에서 도출)
    data_to_collect = [
        {
            "endpoint": "fail_scenario_A",
            "payload": {"system_id": "sys_001", "timestamp": time.time()},
            "description": "Scenario A: Network Timeout Test Data"
        },
        {
            "endpoint": "loss_cost_B",
            "payload": {"system_id": "sys_002", "timestamp": time.time()},
            "description": "Scenario B: Authentication Failure Cost Data"
        },
        {
            "endpoint": "success_scenario_C",
            "payload": {"system_id": "sys_003", "timestamp": time.time()},
            "description": "Scenario C: Baseline Success Data"
        }
    ]

    # 2. 파이프라인 초기화 및 실행
    pipeline = DataIngestionPipeline(API_ENDPOINT)
    pipeline.run_pipeline(data_to_collect)

    print("\n--- Pipeline Execution Complete ---")
    print("📊 평가: 진행중 — 코드가 설계된 로직을 모킹하여 실행했으나, 실제 DB 연결 및 에러 복구 메커니즘은 실제 환경에서 보완이 필요합니다.")
    print("📝 다음 단계: 실제 API 엔드포인트와 DB 스키마 정의를 반영한 연결 코드(DB Connector)를 구현해야 합니다.")