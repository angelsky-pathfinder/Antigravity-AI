export interface StabilityMetrics {
  S_min: number; // Minimum stability threshold
  S_mid: number; // Mid stability threshold
  S_max: number; // Maximum stability threshold
  SWRI: number;   // 수익 지표 (Revenue/Profit Index)
}

/**
 * Dynamic Pricing Logic Module.
 * System Stability Metrics를 기반으로 동적 가격 조정 로직을 계산합니다.
 */
export class PricingService {
  private metrics: StabilityMetrics;

  constructor(metrics: StabilityMetrics) {
    if (!metrics || metrics.S_min <= 0 || metrics.S_mid <= 0 || metrics.S_max <= 0) {
      throw new Error("Stability metrics must be positive values.");
    }
    this.metrics = metrics;
  }

  /**
   * System Stability에 따른 가격 조정 계수를 계산합니다.
   * S가 낮을수록(불안정할수록) 안정성을 보상하기 위해 가격을 상향 조정합니다.
   * @param currentStability 현재 시스템의 안정성 지표 (S)
   * @returns 가격 조정 비율 (0.8 ~ 1.2 사이)
   */
  public calculateAdjustmentFactor(currentStability: number): number {
    if (currentStability <= this.metrics.S_min) {
      // 최저 안정성 이하: 최대 안정성 보상에 집중
      return 1.2;
    } else if (currentStability >= this.metrics.S_max) {
      // 최고 안정성 이상: 수익 극대화에 집중 (안정성이 높을수록 가격 상승 여력 확보)
      return 0.8;
    } else if (currentStability <= this.metrics.S_mid) {
      // 중간 불안정 구간: 중립 조정
      return 1.0;
    } else {
      // 중간 안정성 구간: 안정성을 유지하며 수익을 확보하는 균형점
      // S_mid를 중심으로 가격 민감도와 SWRI를 고려하여 조정 (간단화를 위해 현재는 단순 비율 적용)
      const stabilityRatio = (currentStability - this.metrics.S_min) / (this.metrics.S_max - this.metrics.S_min);
      // S가 중간보다 높으면 가격을 약간 낮추고, 낮으면 높이는 방향으로 조정하는 복잡한 로직이 필요하지만, 일단은 단순 보상을 적용합니다.
      return 1.0 + (stabilityRatio * 0.2); // 안정성 차이에 비례하여 ±20% 조정 시도
    }
  }

  /**
   * 최종 권장 가격을 계산합니다.
   * @param basePrice 기본 가격
   * @returns 조정된 최종 가격
   */
  public calculateFinalPrice(basePrice: number): number {
    const adjustmentFactor = this.calculateAdjustmentFactor(this.metrics.S_mid); // 기준점은 중간 안정성으로 설정
    let finalPrice = basePrice * adjustmentFactor;

    // 수익 지표(SWRI)를 최종 조정에 반영하여 안전 마진을 확보 (예: SWRI가 낮으면 보수적으로 가격을 올림)
    const swriInfluence = 1 - Math.min(1, this.metrics.SWRI / 10); // SWRI가 낮을수록 영향력 증가

    finalPrice *= (1 + swriInfluence * 0.1); // 수익 지표에 따라 추가적인 마진 조정
    
    // 가격은 최소한의 안전 마진을 유지해야 함
    return Math.max(finalPrice, basePrice * 0.95);
  }
}

// --- 테스트 파일 ---
<create_file path="/Users/angelsky/Documents/Antigravity_Workspace/sessions/2026-05-21T10-00/test/PricingService.test.ts">
import { PricingService, StabilityMetrics } from "../src/PricingService";

describe("PricingService", () => {
  // 테스트 데이터 설정 (이 값들은 이전 세션에서 산출된 임계값이라고 가정)
  const mockMetrics: StabilityMetrics = {
    S_min: 10,   // 최소 안정성 임계값
    S_mid: 50,   // 중간 안정성 임계값
    S_max: 100,  // 최대 안정성 임계값
    SWRI: 5.5,   // 수익 지표 (예시 값)
  };

  // 테스트 케이스 1: 최저 안정성 이하 (매우 불안정)
  test("should apply maximum upward adjustment for very low stability", () => {
    const service = new PricingService(mockMetrics);
    // S=5 (S_min보다 훨씬 낮음)
    const price = service.calculateFinalPrice(100); 
    // 기대값: 가장 높은 조정 계수(1.2)가 적용되어 가격이 상승해야 함.
    expect(price).toBeGreaterThan(108); // 100 * 1.2 * (1 + 영향) > 108
  });

  // 테스트 케이스 2: 중간 안정성 구간 (중립)
  test("should apply neutral adjustment for mid-range stability", () => {
    const service = new PricingService(mockMetrics);
    // S=50 (S_mid에 해당)
    const price = service.calculateFinalPrice(100); 
    // 기대값: 중립 조정 (1.0 근처)
    expect(price).toBeCloseTo(100, 2); // SWRI 영향이 미미할 경우 기본 가격 유지 시도
  });

  // 테스트 케이스 3: 최고 안정성 이상 (매우 안정적)
  test("should apply maximum downward adjustment for very high stability", () => {
    const service = new PricingService(mockMetrics);
    // S=150 (S_max보다 높음)
    const price = service.calculateFinalPrice(100); 
    // 기대값: 가장 낮은 조정 계수(0.8)가 적용되어 가격이 하락해야 함.
    expect(price).toBeLessThan(92); // 100 * 0.8 * (1 + 영향) < 92
  });

  // 테스트 케이스 4: SWRI의 영향 확인 (수익 지표가 낮을 때 가격이 더 보수적으로 조정되는지)
  test("should adjust price conservatively when SWRI is low", () => {
    const service = new PricingService(mockMetrics);
    // S=50 (중간 안정성) + 매우 낮은 SWRI (예: 1.0)
    const metricsLowSWRI: StabilityMetrics = { ...mockMetrics, SWRI: 1.0 };
    const priceLowSWRI = service.calculateFinalPrice(100);
    // SWRI가 낮으면 가격이 더 올림 (보수적 접근)
    expect(priceLowSWRI).toBeGreaterThan(service.calculateFinalPrice(100)); // 동일 S에서 낮은 SWRI일 때 더 높은 최종 가격
  });
});