"""
Basic simulation example
Demonstrates how to run a simple mine warfare simulation
"""

import sys
sys.path.append('..')

from src.config import TacticalMineConfig, ThreatLevel
from src.simulation import TacticalMineSimulation

def main():
    print("="*60)
    print("Basic Naval Mine Warfare Simulation Example".center(60))
    print("="*60)
    
    # Create configuration
    config = TacticalMineConfig(
        threat_level=ThreatLevel.MODERATE,
        num_simulations=100  # Quick test
    )
    
    # Initialize simulation
    sim = TacticalMineSimulation(config)
    
    # Define routes
    surface_start = (1000, 1000)
    surface_end = (9000, 9000)
    sub_start = (1000, 1000, 100)
    sub_end = (9000, 9000, 200)
    
    print(f"\nRunning {config.num_simulations} simulations...")
    print(f"Threat Level: {config.threat_level.name}")
    print(f"Total Mines: {config.threat_level.value[0]}\n")
    
    # Run simulation
    stats = sim.run_simulation(surface_start, surface_end, sub_start, sub_end)
    
    # Display results
    print("\n" + "="*60)
    print("Results".center(60))
    print("="*60)
    
    for vessel_type, name in [('surface_vessel', 'Surface Vessel'), 
                              ('submarine', 'Submarine')]:
        s = stats[vessel_type]
        print(f"\n{name}:")
        print(f"  Total Risk:   {s['any_hit_prob']*100:6.2f}%")
        print(f"  Safe Transit: {s['safe_prob']*100:6.2f}%")
        print(f"  Mine Hits:    {s['mine_hit_prob']*100:6.2f}%")
        print(f"  Net Hits:     {s['net_hit_prob']*100:6.2f}%")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()