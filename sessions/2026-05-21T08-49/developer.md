/**
 * Pathfinder: 시스템 안정성 기반 최적 가격 결정 및 리스크 관리 모듈
 * 목표: 시스템 안정성(S)과 수익 지표(SWRI)를 통합하여 최종 단일 가격(P_min)을 계산하고,
 * 시스템 안정성을 보장하기 위한 Retry/Circuit Breaker 패턴을 적용한다.
 */

// --- Constants & Derived Values (이 값들은 이전 세션에서 도출되었다고 가정합니다) ---
const SYSTEM_STABILITY_S: number = 0.95; // 예시 값, 실제 계산 결과로 대체 필요
const SWRI_TARGET: number = 1.5;      // 목표 수익 지표
const S_THRESHOLD: number = 0.80;     // 안정성 임계값 (CEO 승인 기준)
const P_MIN_BASE: number = 7.89;       // 이전 시뮬레이션에서 도출된 기본 최소 가격

/**
 * 시스템 안정성을 기반으로 최종 가격 전략을 계산하는 핵심 로직
 * @param S 시스템 안정성 지표 (0 ~ 1)
 * @param SWRI 수익 지표
 * @returns 최적의 단일 가격 P_min
 */
function calculateOptimalPrice(S: number, SWRI: number): number {
    if (S < S_THRESHOLD) {
        // 안정성 임계값 미달 시, 보수적인 가격 책정 또는 리스크 회피 모드 진입
        console.warn(`[Risk Alert] System Stability (S=${S}) is below threshold (${S_THRESHOLD}). Applying conservative pricing.`);
        return P_MIN_BASE * 1.05; // 안정성 확보를 위해 약간 상향 조정
    }

    // 시스템이 안정적일 경우, 수익 목표에 맞추어 가격을 설정
    if (SWRI >= SWRI_TARGET) {
        // 수익 목표 달성 시 기본 가격 적용
        return P_MIN_BASE;
    } else {
        // 수익 목표 미달 시, 가격을 조정하여 수익성을 확보
        return P_MIN_BASE * (1 + (SWRI_TARGET - SWRI) / 2); // 차이에 비례하여 가격 조정
    }
}

/**
 * API 호출에 대한 Retry Logic 및 Circuit Breaker 패턴 구현
 * @param apiCall 함수 실행 로직 (실제 외부 API 호출을 모킹)
 * @returns 성공 여부와 로그 정보
 */
function executeWithResilience(apiCall: () => Promise<any>): { success: boolean, log: string } {
    const MAX_RETRIES = 3;
    let attempt = 0;
    let breakerState = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN

    while (attempt < MAX_RETRIES) {
        if (breakerState === 'OPEN') {
            // Circuit Breaker가 열려있으면 즉시 실패 처리
            return { success: false, log: `[Circuit Breaker] Call blocked. State is ${breakerState}.` };
        }

        try {
            console.log(`[Attempt ${attempt + 1}/${MAX_RETRIES}] Executing API call...`);
            const result = await apiCall();
            
            // 성공 시, Circuit Breaker를 닫음 (만약 열려있었다면)
            if (breakerState === 'OPEN') {
                console.log("[Circuit Breaker] Call succeeded. State closing to CLOSED.");
                breakerState = 'CLOSED';
            }
            return { success: true, log: `API call successful on attempt ${attempt + 1}.` };

        } catch (error) {
            attempt++;
            console.error(`[Error] API call failed on attempt ${attempt}:`, error);

            if (attempt === MAX_RETRIES) {
                // 최대 재시도 실패 시, Circuit Breaker를 열어 차단
                breakerState = 'OPEN';
                return { success: false, log: `[Circuit Breaker] Max retries failed. State opened to OPEN.` };
            }
        }
    }
    // 이 부분은 이론상 도달하지 않아야 하지만 안전장치
    return { success: false, log: "Unknown failure state reached." };
}

// --- Main Execution Flow ---
async function runPriceSimulationAndTest() {
    console.log("--- Starting Price Simulation and Resilience Test ---");

    const S = SYSTEM_STABILITY_S;
    const SWRI = 1.2; // 테스트를 위해 임의로 설정
    const P_min = calculateOptimalPrice(S, SWRI);

    console.log(`[Calculation Result] Calculated Optimal Price (P_min): ${P_min}`);
    console.log(`[System Check] System Stability (S): ${S}, Target: ${S_THRESHOLD}. Risk Level: ${S < S_THRESHOLD ? 'High' : 'Low'}`);

    // 1. 가격 전략 적용 시뮬레이션
    console.log("\n--- Applying Price Strategy ---");
    if (P_min > P_MIN_BASE) {
        console.log(`[Action] Applying risk-adjusted price: ${P_min}`);
    } else {
        console.log(`[Action] Applying base price: ${P_min}`);
    }

    // 2. 리스크 관리 로직 테스트 (Mock API Call)
    console.log("\n--- Testing Resilience Pattern ---");
    
    // Mock 함수: 성공할 때까지 실패하도록 설정하여 Circuit Breaker를 테스트
    let mockApiCallCount = 0;
    const mockApiCall = async () => {
        mockApiCallCount++;
        if (mockApiCallCount < 2) {
            throw new Error("Mock Network Timeout/Failure");
        }
        return { status: "success", data: "Mocked API Response" };
    };

    const resilienceResult = executeWithResilience(mockApiCall);
    console.log(`[Resilience Test Result] Success: ${resilienceResult.success}, Log: ${resilienceResult.log}`);

    // 3. 최종 결과 보고
    console.log("\n=============================================");
    console.log("✅ Final Integration & Test Complete.");
    console.log(`Final Price Determined: ${P_min}`);
    console.log(`Resilience Test Status: ${resilienceResult.success}`);
    console.log("=============================================");

}

runPriceSimulationAndTest();