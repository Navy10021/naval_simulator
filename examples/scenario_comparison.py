"""
Route scenario comparison example
Compares different submarine route strategies
"""

import sys
sys.path.append('..')

from src.config import TacticalMineConfig, ThreatLevel
from src.simulation import TacticalMineSimulation

def main():
    print("="*60)
    print("Route Scenario Comparison Example".center(60))
    print("="*60)
    
    # Create configuration
    config = TacticalMineConfig(
        threat_level=ThreatLevel.HIGH,
        num_simulations=50
    )
    
    # Initialize simulation
    sim = TacticalMineSimulation(config)
    
    # Define submarine route
    sub_start = (1000, 1000, 100)
    sub_end = (9000, 9000, 200)
    
    print(f"\nTesting different route scenarios...")
    print(f"Threat Level: {config.threat_level.name}")
    print(f"Total Mines: {config.threat_level.value[0]}")
    
    # Run scenario comparison
    results = sim.run_scenario_comparison(sub_start, sub_end, num_iterations=100)
    
    # Display results
    print("\n" + "="*60)
    print("Scenario Comparison Results".center(60))
    print("="*60)
    print(f"\n{'Scenario':<20} {'Safe %':>10} {'Risk %':>10} {'Recommendation':<20}")
    print("-"*60)
    
    sorted_scenarios = sorted(results.items(), 
                             key=lambda x: x[1]['safe_prob'], 
                             reverse=True)
    
    for scenario_name, result in sorted_scenarios:
        safe = result['safe_prob'] * 100
        risk = result['any_hit_prob'] * 100
        
        if safe > 70:
            recommendation = "✓ Recommended"
        elif safe > 50:
            recommendation = "⚠ Moderate Risk"
        else:
            recommendation = "✗ High Risk"
        
        print(f"{scenario_name:<20} {safe:>9.1f}% {risk:>9.1f}% {recommendation:<20}")
    
    print("\n" + "="*60)
    print(f"\nBest Strategy: {sorted_scenarios[0][0]}")
    print(f"Safety Rate: {sorted_scenarios[0][1]['safe_prob']*100:.1f}%")
    print("="*60)

if __name__ == "__main__":
    main()