# Transition_Logic: Dynamic Pricing Adjustment Logic

/**
 * 시스템 안정성 지표($S$)를 기반으로 가격 등급을 조정하는 로직입니다.
 * @param stabilityScore 현재 시스템 안정성 지표 (S)
 * @param minThreshold 최소 안정성 임계값 (S_min)
 * @param midThreshold 중간 안정성 임계값 (S_mid)
 * @param maxThreshold 최대 안정성 임계값 (S_max)
 * @returns 조정된 가격 등급 (Tier)
 */
function calculatePricingTier(stabilityScore: number, minThreshold: number, midThreshold: number, maxThreshold: number): string {
    if (stabilityScore >= maxThreshold) {
        return "Tier_Max"; // 최고 안정성 구간
    } else if (stabilityScore >= midThreshold) {
        return "Tier_Mid"; // 중간 안정성 구간
    } else if (stabilityScore >= minThreshold) {
        return "Tier_Min"; // 최소 안정성 구간
    } else {
        return "Tier_Risk"; // 위험 구간 (최소치 미달)
    }
}

/**
 * 가격 조정 시나리오 정의 (안정성을 유도하는 방향으로 상향 전환 시나리오 포함)
 * @param stabilityScore 현재 안정성 지표 S
 * @returns 가격 조정에 필요한 액션 (Action)
 */
function determinePriceAction(stabilityScore: number, minThreshold: number, midThreshold: number, maxThreshold: number): string {
    if (stabilityScore < minThreshold) {
        // 시스템이 위험 구간일 때, 안정성을 확보하도록 유도하는 상향 전환 시나리오 정의
        return "ACTION_INCREASE_PRICING"; // 안정성 목표 달성을 위해 가격 상향 권고
    } else if (stabilityScore >= maxThreshold) {
        return "ACTION_MAINTAIN_OR_REDUCE"; // 최고 안정성 달성, 유지 또는 마진 확보를 위한 조정
    } else if (stabilityScore < midThreshold) {
        // 중간 구간에서 위험으로 하락할 때의 선제적 대응
        return "ACTION_INCREASE_PRICING"; 
    } else {
        return "ACTION_MAINTAIN"; // 정상 범위 내 안정성 유지
    }
}

export { calculatePricingTier, determinePriceAction };