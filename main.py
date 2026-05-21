from fastapi import FastAPI, HTTPException
from typing import Dict, Any
import time
import random

app = FastAPI(
    title="Pathfinder Resilience API",
    description="System Stability (S) and Revenue Index (SWRI) Data Backend"
)

# --- Mock Data Layer (실제 데이터 연동을 위한 목업) ---
def get_mock_stability_data() -> Dict[str, Any]:
    """시스템 안정성(S) 관련 데이터를 모킹합니다."""
    # 시스템 안정성(S)은 0.0에서 1.0 사이의 값으로 가정
    stability = round(random.uniform(0.85, 1.0), 2) # 현재는 높은 안정성을 유지한다고 가정
    status_details = {
        "system_health": "OK",
        "latency_ms": random.randint(10, 100),
        "circuit_breaker_status": "CLOSED" if stability > 0.9 else "HALF_OPEN"
    }
    return {"timestamp": int(time.time()), "stability_score": stability, "details": status_details}

def get_mock_revenue_data() -> Dict[str, Any]:
    """수익 지표(SWRI) 관련 데이터를 모킹합니다."""
    # 수익 지표(SWRI)는 0에서 100 사이의 값으로 가정
    swri = round(random.uniform(50.0, 95.0), 2) # 현재는 높은 수익성을 유지한다고 가정
    revenue_details = {
        "total_revenue_usd": round(random.uniform(5000.0, 15000.0), 2),
        "tier_performance": {"Standard": round(random.uniform(1000.0, 3000.0), 2), "Premium": round(4000.0, 2)},
        "trend_7d": "UP" if swri > 55 else ("DOWN" if swri < 45 else "FLAT")
    }
    return {"timestamp": int(time.time()), "swri_score": swri, "details": revenue_details}

def get_correlation_data() -> Dict[str, Any]:
    """S와 SWRI 간의 상관관계를 모킹합니다."""
    # 안정성과 수익 지표는 양의 상관관계가 높다고 가정
    stability = random.uniform(0.85, 1.0)
    swri = random.uniform(50.0, 95.0)
    correlation = round(stability * (swri / 100) * 1.2 + random.uniform(-0.1, 0.1), 3) # 약간의 노이즈 추가
    return {
        "timestamp": int(time.time()),
        "system_stability": stability,
        "revenue_index": swri,
        "correlation_score": round(correlation, 3),
        "analysis": "High correlation observed. Stability directly impacts revenue potential."
    }

# --- API Endpoints ---

@app.get("/api/v1/system_status", response_model=Dict[str, Any])
def get_system_status():
    """시스템 안정성(S) 관련 실시간 상태 정보를 제공합니다."""
    data = get_mock_stability_data()
    return data

@app.get("/api/v1/revenue_metrics", response_model=Dict[str, Any])
def get_revenue_metrics():
    """수익 지표(SWRI) 및 세부 매출 데이터를 제공합니다."""
    data = get_mock_revenue_data()
    return data

@app.get("/api/v1/stability_revenue_correlation", response_model=Dict[str, Any])
def get_correlation():
    """시스템 안정성과 수익 지표 간의 상관관계를 제공합니다."""
    data = get_correlation_data()
    return data

@app.get("/")
def read_root():
    """API 서버 상태 확인용 루트 엔드포인트."""
    return {"message": "Pathfinder Resilience API is running. Check /docs for endpoints."}