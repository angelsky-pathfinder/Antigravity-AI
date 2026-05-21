<content>
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import random
import time
import numpy as np # 상관관계 계산을 위해 numpy 추가

# --- System Stability (S) 및 Revenue Metrics (SWRI) Mock Data Setup ---

class Metrics(BaseModel):
    system_stability: float  # S: 0.0 to 1.0
    revenue_metrics: float   # SWRI: Monetary value

# Global state for simulation/tracking
SYSTEM_STABILITY = 0.85 # 초기 안정성 레벨 (S)
REVENUE_METRICS = 15000.0 # 초기 수익 지표 (SWRI)

app = FastAPI()

# --- API Endpoints ---

@app.get("/api/v1/system_status")
async def get_system_status():
    """시스템 안정성(S) 정보를 제공합니다."""
    global SYSTEM_STABILITY
    # 실제 환경에서는 DB나 외부 모니터링 시스템에서 데이터를 가져와야 함.
    return {"status": "OK", "system_stability": round(SYSTEM_STABILITY, 4), "timestamp": time.time()}

@app.get("/api/v1/revenue_metrics")
async def get_revenue_metrics():
    """수익 지표(SWRI) 정보를 제공합니다."""
    global REVENUE_METRICS
    # 실제 환경에서는 DB나 외부 매출 시스템에서 데이터를 가져와야 함.
    return {"status": "OK", "revenue_metrics": round(REVENUE_METRICS, 2), "timestamp": time.time()}

@app.post("/api/v1/simulate_correlation")
async def simulate_correlation():
    """S와 SWRI 간의 상관관계를 계산하고 결과를 반환합니다."""
    global SYSTEM_STABILITY, REVENUE_METRICS
    
    # 1. 데이터 준비 (시뮬레이션 또는 실제 데이터 로드)
    # 여기서는 현재 상태를 기반으로 임의의 시계열 데이터를 생성하여 상관관계를 계산하는 로직을 구현합니다.
    
    N = 50 # 데이터 포인트 수
    stability_data = []
    revenue_data = []

    # 시스템 안정성(S)에 따라 수익 지표(SWRI)가 어떻게 변하는지 시뮬레이션 (상관관계 유도)
    for i in range(N):
        # S 값이 높으면 SWRI가 높아지는 경향을 가정. 노이즈 추가.
        stability = SYSTEM_STABILITY + np.random.uniform(-0.1, 0.1)
        revenue = REVENUE_METRICS * (1 + stability * 0.5) + np.random.uniform(-500, 500)
        
        stability_data.append(stability)
        revenue_data.append(revenue)

    # 2. 상관관계 계산
    if len(stability_data) < 2:
        return {"error": "데이터 포인트가 부족합니다. 최소 2개 이상 필요."}, 400

    correlation = np.corrcoef(stability_data, revenue_data)[0, 1]
    
    # 3. 결과 반환
    result = {
        "status": "Success",
        "correlation_s_swri": round(correlation, 4),
        "message": f"S와 SWRI의 상관관계 계산 완료. 계수: {round(correlation, 4)}"
    }
    return result