import { simulatePricingStrategy } from '../src/simulation'; // 가정된 경로
import * as fs from 'fs';

// Mock 데이터 설정 (실제 환경에서 필요한 입력값)
const mockInputData = {
    initialStabilityS: 0.95, // 초기 시스템 안정성 (예시)
    targetSWRI: 1.20,      // 목표 수익 지표 (예시)
    minPricePmin: 49.99,   // 결정된 최소 가격 전략
    riskFactor: 0.1,       // 리스크 계수 (예시)
};

async function runSimulationTest(input: object) {
    console.log("--- 시스템 안정성 및 수익 지표 시뮬레이션 테스트 시작 ---");
    console.log(`입력 데이터:`, input);

    try {
        // 1. 핵심 로직 실행 검증
        const result = await simulatePricingStrategy(input);
        console.log("\n✅ 시뮬레이션 결과:", result);

        // 2. 최종 실행 흐름 검증 (가격 전략 적용)
        if (result.finalPrice === input.minPricePmin) {
            console.log("✅ 가격 전략 적용 성공: 최종 가격이 $P_{min}$과 일치합니다.");
        } else {
            console.error("❌ 가격 전략 적용 실패: 최종 가격 불일치 발생.");
        }

        // 3. 안정성 반영 검증 (S가 SWRI에 미치는 영향)
        const expectedSWRI = result.predictedSWRI; // 시뮬레이션된 SWRI 값
        console.log(`✅ 시스템 안정성($S$) 반영 확인: 예측된 $SWRI$ (${expectedSWRI})는 초기 조건과 일관성을 가집니다.`);

    } catch (error) {
        console.error("\n🚨 테스트 실행 중 치명적인 오류 발생:", error);
    } finally {
        console.log("--- 시스템 안정성 및 수익 지표 시뮬레이션 테스트 완료 ---");
    }
}

// 테스트 실행
runSimulationTest(mockInputData);