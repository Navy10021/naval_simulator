"""
Custom threat level example
Demonstrates how to create custom threat configurations
"""

import sys
sys.path.append('..')

from src.config import TacticalMineConfig, ThreatLevel
from src.simulation import TacticalMineSimulation
from enum import Enum

# Define custom threat level
class CustomThreatLevel(Enum):
    EXTREME = (600, 0.95)  # 600 mines, 95% target risk
    LOW = (75, 0.30)       # 75 mines, 30% target risk

def main():
    print("="*60)
    print("Custom Threat Level Example".center(60))
    print("="*60)
    
    # Test both custom threat levels
    for custom_threat in [CustomThreatLevel.LOW, CustomThreatLevel.EXTREME]:
        print(f"\n\nTesting {custom_threat.name} Threat Level")
        print(f"Mines: {custom_threat.value[0]}, Target Risk: {custom_threat.value[1]*100:.0f}%")
        print("-"*60)
        
        # Create custom configuration
        config = TacticalMineConfig(
            threat_level=custom_threat,
            num_simulations=50
        )
        
        # Initialize simulation
        sim = TacticalMineSimulation(config)
        
        # Define routes
        surface_start = (1000, 1000)
        surface_end = (9000, 9000)
        sub_start = (1000, 1000, 100)
        sub_end = (9000, 9000, 200)
        
        # Run simulation
        stats = sim.run_simulation(surface_start, surface_end, sub_start, sub_end, 
                                   verbose=False)
        
        # Display results
        print(f"\nSurface Vessel Risk: {stats['surface_vessel']['any_hit_prob']*100:.1f}%")
        print(f"Submarine Risk:      {stats['submarine']['any_hit_prob']*100:.1f}%")
        
        # Compare with target
        target = custom_threat.value[1] * 100
        actual_surf = stats['surface_vessel']['any_hit_prob'] * 100
        diff = actual_surf - target
        
        print(f"\nTarget Risk:     {target:.1f}%")
        print(f"Actual Risk:     {actual_surf:.1f}%")
        print(f"Difference:      {diff:+.1f}%")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()