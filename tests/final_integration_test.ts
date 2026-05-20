import { PricingService } from '../src/PricingService'; // 실제 경로에 맞게 수정 필요
import { DataPipelineSimulator } from '../src/DataPipelineSimulator'; // 실제 경로에 맞게 수정 필요

async function runFinalTest() {
    console.log("--- 🚀 최종 통합 테스트 시작: S 변화에 따른 SWRI 측정 ---");

    // 1. 환경 설정 및 초기 데이터 로드 (가정)
    const initialStability = 0.8; // 초기 시스템 안정성
    const initialSWRI = 15000;   // 초기 수익 지표 (예시 값)

    console.log(`[INFO] 초기 상태: S=${initialStability}, SWRI=${initialSWRI}`);

    // 2. 시나리오 1: 시스템 안정성 감소 (리스크 증가)
    const stabilityDecrease = 0.6; // 안정성 감소 시나리오
    await DataPipelineSimulator.simulateStabilityChange(stabilityDecrease);
    
    // 가격 조정 로직 실행 (이전 개발 파일 기반으로 가정)
    const adjustedSWRI_1 = await PricingService.adjustPrice(initialSWRI, stabilityDecrease);

    console.log(`[SCENARIO 1] S 감소 (${stabilityDecrease}) 후: SWRI=${adjustedSWRI_1}`);


    // 3. 시나리오 2: 시스템 안정성 증가 (안정성 확보)
    const stabilityIncrease = 0.95; // 안정성 증가 시나리오
    await DataPipelineSimulator.simulateStabilityChange(stabilityIncrease);

    // 가격 조정 로직 실행
    const adjustedSWRI_2 = await PricingService.adjustPrice(initialSWRI, stabilityIncrease);

    console.log(`[SCENARIO 2] S 증가 (${stabilityIncrease}) 후: SWRI=${adjustedSWRI_2}`);


    // 4. 결과 분석 및 검증
    console.log("\n--- ✅ 최종 결과 검증 ---");
    const swing = adjustedSWRI_2 - adjustedSWRI_1;
    const stabilityChange = stabilityIncrease - stabilityDecrease;

    console.log(`S 변화: ${stabilityChange}`);
    console.log(`SWRI 변화: ${swing}`);
    
    // 기대 결과 검증 (이 부분은 실제 로직에 따라 조정되어야 함)
    if (swing < 0) {
        console.log("⚠️ 경고: S 증가에도 불구하고 SWRI가 감소했습니다. 로직 재검토 필요.");
    } else {
        console.log("✅ 검증 통과: 안정성 증가는 수익 지표에 긍정적인 영향을 미쳤습니다 (또는 예상 범위 내에 있음).");
    }

    console.log("\n--- 테스트 완료 ---");
}

runFinalTest().catch(err => {
    console.error("❌ 최종 테스트 실행 중 치명적 오류 발생:", err);
});