<![CDATA[
// PricingEngine.ts - Stability Tiered Pricing Model Implementation

interface PricingContext {
  basePrice: number;
  stabilityScore: number; // S 지표 (0~100)
  marketPremium: number; // P_Market
}

const TIER_CONFIG = {
  'Tier 1: Foundation': { minS: 0, maxS: 39.99, marketPremium: 'P_A', swriTarget: 'LTV 최소치 보장 및 CR 극대화.' },
  'Tier 2: Growth': { minS: 40, maxS: 69.99, marketPremium: 'P_B', swriTarget: 'SWRI 목표 달성 및 LTV 증대.' },
  'Tier 3: Premium': { minS: 70, maxS: 100, marketPremium: 'P_A + P_B', swriTarget: '마진 극대화 및 안정성($S$)에 대한 직접적인 보상 반영.' },
};

/**
 * Stability Tiered Pricing Model 로직을 기반으로 가격과 등급을 계산합니다.
 * @param context - 현재 시스템 데이터와 시장 프리미엄 정보
 * @returns {object} - 계산된 가격, 현재 Tier, 목표 수익화 지표
 */
export function calculatePricing(context: PricingContext): { price: number; tier: string; swriTarget: string } {
  let determinedTier: string;

  // 1. Tier 결정 로직 실행
  if (context.stabilityScore >= TIER_CONFIG['Tier 3: Premium'].minS) {
    determinedTier = 'Tier 3: Premium';
  } else if (context.stabilityScore >= TIER_CONFIG['Tier 2: Growth'].minS) {
    determinedTier = 'Tier 2: Growth';
  } else if (context.stabilityScore >= TIER_CONFIG['Tier 1: Foundation'].minS) {
    determinedTier = 'Tier 1: Foundation';
  } else {
    // 안정성 기준 미달 시 에러 또는 최소 Tier 적용
    determinedTier = 'Error/Suspension';
  }

  const tierConfig = TIER_CONFIG[determinedTier];

  // 2. 가격 계산 (FR2.3 재정비 기반)
  const f = (s: number) => {
    if (s >= 100) return 0.5; // 최고 안정성 시 보정 계수 최대화
    if (s >= 70) return 0.2;
    if (s >= 40) return 0.1;
    return 0.0;
  };

  const finalPrice = (context.basePrice * (1 + f(context.stabilityScore))) * context.marketPremium;

  // 3. 수익화 목표 설정
  const swriTarget = tierConfig.swriTarget;

  return {
    price: parseFloat(finalPrice.toFixed(2)),
    tier: determinedTier,
    swriTarget: swriTarget,
  };
}

/**
 * API 연동을 위한 Tier 자동 전환 로직 (외부 호출용)
 * @param stabilityScore - 현재 시스템 안정성 지표 (S)
 * @returns {object} - 업데이트 결과 및 권장 사항
 */
export function transitionStabilityTier(stabilityScore: number): { success: boolean; newTier: string; recommendedPrice: number } {
  let determinedTier: string;

  // Tier 결정 로직 재사용
  if (stabilityScore >= TIER_CONFIG['Tier 3: Premium'].minS) {
    determinedTier = 'Tier 3: Premium';
  } else if (stabilityScore >= TIER_CONFIG['Tier 2: Growth'].minS) {
    determinedTier = 'Tier 2: Growth';
  } else if (stabilityScore >= TIER_CONFIG['Tier 1: Foundation'].minS) {
    determinedTier = 'Tier 1: Foundation';
  } else {
    return { success: false, newTier: 'Error/Suspension', recommendedPrice: 0 };
  }

  // 가격 재계산 (이때 basePrice와 marketPremium은 외부에서 주입되어야 함. 여기서는 예시로 임의값 사용)
  const mockContext: PricingContext = { basePrice: 100, stabilityScore: stabilityScore, marketPremium: 'P_A' };
  const result = calculatePricing(mockContext);

  return {
    success: true,
    newTier: determinedTier,
    recommendedPrice: result.price,
  };
}
]]>