import { PricingService } from '../src/PricingService';

// Mocking the external data pipeline connection for testing purposes
const mockDataPipeline = {
    // Simulates the actual relationship based on $S$ change
    simulateImpact: (stabilityChange: number) => {
        if (stabilityChange > 0.1) { // System stability increases
            return { deltaSWRI: -0.05, message: "Increased stability leads to slight profit margin adjustment." };
        } else if (stabilityChange < -0.1) { // System stability decreases
            return { deltaSWRI: 0.10, message: "Decreased stability triggers higher price adjustment to compensate risk." };
        } else { // Stability is stable
            return { deltaSWRI: 0.00, message: "Stability unchanged, no direct profit impact." };
        }
    },
    // Simulates the actual data input for testing
    getPipelineData: (stability: number) => ({
        S: stability,
        SWRI_actual: 1500 + (stability * 100), // Mock relationship based on S
        B_log_avg: 5.2 // Baseline behavior log
    })
};

describe('PricingService Integration Test', () => {
    let pricingService: PricingService;

    beforeEach(() => {
        pricingService = new PricingService();
    });

    it('should correctly calculate price adjustment based on stability threshold (S)', () => {
        // Test Case 1: High Stability (Should result in lower risk-based pricing)
        const highStability = 0.8;
        const calculatedPrice = pricingService.adjustPrice(highStability);
        // Expect a smaller adjustment/less aggressive change when S is high
        expect(calculatedPrice).toBeLessThan(1500); // Assuming base price is around 1500 for context

        // Test Case 2: Low Stability (Should result in higher risk-based pricing)
        const lowStability = 0.3;
        const calculatedPriceLow = pricingService.adjustPrice(lowStability);
        // Expect a larger adjustment/more aggressive change when S is low
        expect(calculatedPriceLow).toBeGreaterThan(1500);

    });

    it('should correctly simulate the impact on SWRI based on pipeline data', () => {
        const stability = 0.6; // Example stability value
        const pipelineData = mockDataPipeline.getPipelineData(stability);

        // Verify that the simulated impact matches the expected logic flow
        const result = mockDataPipeline.simulateImpact(stability);

        expect(result.deltaSWRI).toBeCloseTo(0.00, 2); // Check if the simulation function yields a predictable result
    });

    it('should integrate S and SWRI for final dynamic pricing decision', () => {
        const stability = 0.9;
        const pipelineData = mockDataPipeline.getPipelineData(stability);
        
        // Assuming the PricingService uses these inputs to determine the final adjustment factor
        const finalAdjustment = pricingService.calculateDynamicAdjustment(stability, pipelineData.SWRI_actual);

        // Verification: High stability should lead to a lower multiplier or less aggressive change
        expect(finalAdjustment).toBeLessThan(0.1); // Check against expected safe bounds
    });
});