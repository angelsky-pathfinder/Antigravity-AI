from typing import Dict, Any
import time
import random

# --- Configuration Constants (실제 환경에서는 DB에서 로드) ---
S_MIN_THRESHOLD = 0.75  # 안정성 최소 임계값
RHO_MAX_THRESHOLD = 0.50 # 상관관계 최대 허용치
RECOVERY_S_THRESHOLD = 0.80
RECOVERY_RHO_THRESHOLD = 0.65

class MetricsService:
    """시스템 안정성과 수익 지표를 관리하고 실시간 상관관계를 계산하는 서비스 클래스."""

    def __init__(self):
        # 실제 환경에서는 DB 연결 및 캐시 초기화 로직이 여기에 들어갑니다.
        pass

    def _fetch_realtime_data(self, time_window: str) -> Dict[str, float]:
        """
        실시간 시스템 안정성(S)과 수익 지표(SWRI) 데이터를 조회하는 Mock 함수.
        실제 구현 시 DB나 스트리밍 소스에서 데이터를 가져옵니다.
        """
        # 실제 데이터는 외부 시스템에 의존하므로 랜덤 값으로 시뮬레이션합니다.
        if time_window == '1h':
            S = random.uniform(0.6, 0.9)
            SWRI = S * random.uniform(1.0, 1.5) # 상호 연관성 시뮬레이션
        elif time_window == '24h':
            S = random.uniform(0.5, 0.95)
            SWRI = S * random.8 + random.uniform(0.5, 1.5)
        else:
            raise ValueError("지원하지 않는 시간 범위입니다.")

        return {"S": S, "SWRI": SWRI}

    def _calculate_correlation(self, data_points: list[Dict[str, float]]) -> float:
        """
        주어진 데이터 포인트들의 시계열 간의 상관관계를 계산합니다. (간소화된 피어슨 상관계수)
        """
        if len(data_points) < 2:
            return 0.0

        S_values = [d['S'] for d in data_points]
        SWRI_values = [d['SWRI'] for d in data_points]

        # 실제 상관계수 계산 로직 (numpy 또는 scipy 사용 권장)
        # 여기서는 단순화를 위해 임시 계산을 가정합니다.
        # 실제 구현에서는 numpy.corrcoef를 사용하여 정확히 계산해야 합니다.
        correlation = sum((S_values[i] - mean(S_values)) * (SWRI_values[i] - mean(SWRI_values)) for i in range(len(S_values))) / \
                       (sqrt(sum((S_values[i] - mean(S_values))**2 for i in range(len(S_values)))) * 
                        sqrt(sum((SWRI_values[i] - mean(SWRI_values))**2 for i in range(len(SWRI_values))))
        
        return correlation

    def _check_circuit_breaker(self, current_s: float, correlation: float) -> Dict[str, str]:
        """
        S와 SWRI를 기반으로 Circuit Breaker 상태를 판단하고 업데이트합니다.
        """
        stability_breaker = "CLOSED"
        profitability_breaker = "CLOSED"

        # 1. 안정성 브레이커 체크
        if current_s < S_MIN_THRESHOLD:
            stability_breaker = "OPEN"
        elif stability_breaker == "OPEN" and current_s >= RECOVERY_S_THRESHOLD:
            stability_breaker = "HALF-OPEN" # 복구 시도

        # 2. 수익성 브레이커 체크 (상관관계 기반)
        if correlation < RHO_MAX_THRESHOLD:
            profitability_breaker = "OPEN"
        elif profitability_breaker == "OPEN" and correlation >= RECOVERY_RHO_THRESHOLD:
            profitability_breaker = "HALF-OPEN" # 복구 시도

        return {
            "stability_breaker": stability_breaker,
            "profitability_breaker": profitability_breaker
        }


    def get_realtime_metrics(self, time_window: str) -> Dict[str, Any]:
        """
        최종 API 요청을 처리하는 메인 로직.
        """
        print(f"🚀 Realtime Metrics 요청 수신: 시간 범위={time_window}")
        
        try:
            # 1. 데이터 조회 (Mock)
            raw_data = self._fetch_realtime_data(time_window)
            
            # 2. 상관관계 계산을 위한 충분한 데이터 확보 (실제로는 DB에서 N개 데이터를 가져와야 함)
            # 여기서는 Mock 데이터를 기반으로 임시로 3개의 포인트 생성하여 상관계수를 계산합니다.
            mock_history = [
                {"S": raw_data["S"], "SWRI": raw_data["SWRI"]},
                {"S": random.uniform(0.5, 1.0), "SWRI": random.uniform(0.8, 2.0)},
                {"S": random.uniform(0.5, 1.0), "SWRI": random.uniform(0.8, 2.0)}
            ]
            correlation = self._calculate_correlation(mock_history)

            # 3. Circuit Breaker 상태 확인 및 업데이트
            cb_status = self._check_circuit_breaker(raw_data["S"], correlation)

            # 4. 최종 응답 구성
            response = {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "system_status": raw_data,
                "circuit_breaker_status": cb_status,
                "correlation_score": round(correlation, 3),
                "risk_assessment": {
                    "severity": "LOW",
                    "reason": "모든 지표가 정상 범위 내에 있습니다." if cb_status["stability_breaker"] == "CLOSED" and cb_status["profitability_breaker"] == "CLOSED" else f"경고: 안정성 브레이커 상태는 {cb_status['stability_breaker']}입니다."
                },
                "data_source": "API_V1.2"
            }
            return response

        except ValueError as e:
            # 시간 범위 오류 등 입력 검증 실패 시 400 에러 처리 (실제 API에서는 HTTP 응답으로 매핑)
            raise Exception(f"입력 데이터 오류: {e}")
        except Exception as e:
            # 모든 예상치 못한 시스템 오류는 500 에러로 보고합니다.
            print(f"🚨 Critical Error during metric calculation: {e}")
            raise Exception("시스템 내부 오류 발생. 데이터 조회에 실패했습니다.")

# --- FastAPI Endpoint Simulation ---
# 이 부분은 실제 FastAPI 환경에서 route 함수로 대체됩니다.
if __name__ == '__main__':
    service = MetricsService()
    print("\n--- Realtime API Simulation Start ---")
    
    try:
        result_24h = service.get_realtime_metrics("24h")
        print("\n✅ 24시간 데이터 결과:")
        import json
        print(json.dumps(result_24h, indent=2, ensure_ascii=False))

        print("\n--- Realtime API Simulation End ---")
    except Exception as e:
        print(f"\n❌ 최종 실행 실패: {e}")
        
# 이 코드는 실제 API 서버 환경에서 사용될 핵심 로직을 담고 있습니다.