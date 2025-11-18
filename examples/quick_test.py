"""
Quick test example
Fast simulation for testing purposes
"""

import sys
sys.path.append('..')

from src.config import TacticalMineConfig, ThreatLevel
from src.simulation import TacticalMineSimulation
import time

def main():
    print("="*60)
    print("Quick Test - Performance Check".center(60))
    print("="*60)
    
    # Quick configuration
    config = TacticalMineConfig(
        threat_level=ThreatLevel.MODERATE,
        num_simulations=10  # Very quick
    )
    
    sim = TacticalMineSimulation(config)
    
    surface_start = (1000, 1000)
    surface_end = (9000, 9000)
    sub_start = (1000, 1000, 100)
    sub_end = (9000, 9000, 200)
    
    print(f"\nRunning {config.num_simulations} simulations...")
    
    start_time = time.time()
    stats = sim.run_simulation(surface_start, surface_end, sub_start, sub_end, 
                               verbose=False)
    elapsed_time = time.time() - start_time
    
    print(f"\n✓ Completed in {elapsed_time:.2f} seconds")
    print(f"  Average: {elapsed_time/config.num_simulations*1000:.1f} ms per simulation")
    
    print(f"\nQuick Results:")
    print(f"  Surface Risk: {stats['surface_vessel']['any_hit_prob']*100:.1f}%")
    print(f"  Sub Risk:     {stats['submarine']['any_hit_prob']*100:.1f}%")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()