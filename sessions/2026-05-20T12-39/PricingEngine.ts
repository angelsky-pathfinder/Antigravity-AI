import { StabilityTieredPricingTable } from './DataModel';

/**
 * PricingEngine 클래스는 안정성 지표를 기반으로 동적 가격을 계산하고 전환을 제안한다.
 */
export class PricingEngine {
    private pricingTable: StabilityTieredPricingTable;

    constructor(pricingTable: StabilityTieredPricingTable) {
        this.pricingTable = pricingTable;
    }

    /**
     * 안정성 및 시장 데이터를 기반으로 권장 가격을 계산한다.
     * @param stabilityScore 시스템 안정성 점수 (S)
     * @param swri 수익 가중치 지표 (SWRI)
     * @param marketData 시장 프리미엄 데이터 (PA, PB)
     * @returns 권장 가격과 전환 추천 정보 객체
     */
    public calculatePrice(stabilityScore: number, swri: number, marketData: { PA: number, PB: number }): { recommendedPrice: number, transitionRecommendation: string, stabilityDelta: number } {
        if (!this.pricingTable) {
            throw new Error("Pricing table is not initialized.");
        }

        // 1. 현재 안정성 티어 식별 (실제 구현 시 복잡한 매핑 로직 필요)
        const currentTier = this.determineTier(stabilityScore);

        if (!currentTier) {
            throw new Error(`Stability score ${stabilityScore} does not map to any defined tier.`);
        }

        // 2. FR2.3 기반 가격 계산 (예시 로직)
        // 실제 FR2.3 공식은 데이터 모델에 따라 복잡하게 정의되어야 함. 여기서는 예시로 단순화.
        let basePrice = this.calculateBasePrice(currentTier, swri);

        // 3. 시장 프리미엄 적용
        const marketAdjustment = (marketData.PA + marketData.PB) / 2;
        let recommendedPrice = basePrice * (1 + marketAdjustment * 0.1); // 10% 조정 예시

        // 4. 자동 상향 전환 시나리오 검증
        let transitionRecommendation = "No immediate change recommended.";
        let stabilityDelta = stabilityScore - this.getTargetStability();

        if (stabilityScore > this.getTargetStability()) {
            const alpha = this.calculateAlpha(stabilityScore, this.getTargetStability());
            if (swri < 0.9) { // SWRI가 목표치에 미달할 경우 상향을 권장
                transitionRecommendation = `Stability improved. Recommended price increase by ${alpha * 100}%.`;
            } else {
                 transitionRecommendation = "Stability improved, but revenue targets are met.";
            }
        }

        return {
            recommendedPrice: parseFloat(recommendedPrice.toFixed(2)),
            transitionRecommendation: transitionRecommendation,
            stabilityDelta: parseFloat(stabilityDelta.toFixed(2))
        };
    }

    /**
     * 내부적으로 안정성 점수를 기반으로 티어를 결정한다 (Placeholder).
     */
    private determineTier(score: number): string | null {
        if (score >= 85) return 'Gold';
        if (score >= 60) return 'Silver';
        return 'Bronze';
    }

    /**
     * 가격 결정의 기본 기준을 계산한다 (Placeholder).
     */
    private calculateBasePrice(tier: string, swri: number): number {
        // 실제로는 Tier별로 다른 기본 로직 적용
        if (tier === 'Gold') return 1000;
        if (tier === 'Silver') return 650;
        return 300;
    }

    /**
     * 목표 안정성 점수를 반환한다.
     */
    private getTargetStability(): number {
        // 이 값은 외부 설정 또는 데이터에서 로드되어야 함.
        return 80; // 임시 목표치 설정
    }

    /**
     * 자동 상향 전환에 사용될 알파 값을 계산한다 (Placeholder).
     */
    private calculateAlpha(current: number, target: number): number {
        // 안정성 개선 정도에 따라 동적으로 조정.
        return Math.min(0.2, (current - target) / 100); // 최대 20% 상향 제한
    }
}

// --- 테스트 코드 ---
async function runTest() {
    console.log("--- Pricing Engine Test Running ---");

    // 1. Data Model 로드 (Mocking for test)
    const mockTable = {
        tables: [{
            id: 'mock-uuid', S: 85, SWRI: 0.95, PA: 1.2, PB: 1.1, Tier: 'Gold', Target_Price_Range: [1000, 1500], Transition_Logic: '{"threshold": 85, "increase_pct": 0.15}'
        }]
    };

    // 2. 엔진 초기화
    const engine = new PricingEngine(mockTable.tables[0]);

    // 3. 입력 데이터
    const stabilityScore = 90; // 안정성 높음
    const swri = 0.85;         // 수익 지표가 목표치 미달 (상향 유도 필요)
    const marketData = { PA: 1.3, PB: 1.2 };

    console.log(`Input: S=${stabilityScore}, SWRI=${swri}, Market_PA=${marketData.PA}`);

    try {
        // 4. 가격 계산 실행
        const result = engine.calculatePrice(stabilityScore, swri, marketData);

        console.log("\n✅ Calculation Result:");
        console.log(`Recommended Price: $${result.recommendedPrice}`);
        console.log(`Transition Recommendation: ${result.transitionRecommendation}`);
        console.log(`Stability Delta (S - Target): ${result.stabilityDelta}`);

    } catch (error) {
        console.error("❌ Calculation Error:", error.message);
    }
}

runTest();