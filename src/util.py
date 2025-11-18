"""
Utility functions for naval mine warfare simulation
"""

import json
from datetime import datetime
from typing import Dict


def export_results_json(stats: Dict, threat_name: str, 
                       output_dir: str, config, scenario_results: Dict = None):
    """Export simulation results to JSON"""
    export_data = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'threat_level': threat_name,
            'simulation_count': config.num_simulations,
            'version': '3.0'
        },
        'configuration': {
            'area': {
                'width_m': config.area_width,
                'height_m': config.area_height,
                'max_depth_m': config.max_depth
            },
            'total_mines': config.threat_level.value[0],
            'target_risk': config.threat_level.value[1],
            'deployment': {
                'linear_ratio': config.linear_density,
                'random_ratio': config.random_density,
                'core_route_width_m': config.core_route_width
            },
            'mine_parameters': {
                'surface_depth_range_m': config.surface_mine_depth_range,
                'surface_spacing_m': config.surface_mine_spacing,
                'subsurface_depth_range_m': config.subsurface_mine_depth_range,
                'subsurface_spacing_m': config.subsurface_mine_spacing,
                'mine_radius_m': config.mine_radius
            }
        },
        'results': {
            'surface_vessel': {
                'probabilities': {
                    'mine_hit': round(stats['surface_vessel']['mine_hit_prob'], 4),
                    'net_hit': round(stats['surface_vessel']['net_hit_prob'], 4),
                    'both_hit': round(stats['surface_vessel']['both_hit_prob'], 4),
                    'any_hit': round(stats['surface_vessel']['any_hit_prob'], 4),
                    'safe_passage': round(stats['surface_vessel']['safe_prob'], 4)
                },
                'counts': stats['surface_vessel']['counts']
            },
            'submarine': {
                'probabilities': {
                    'mine_hit': round(stats['submarine']['mine_hit_prob'], 4),
                    'net_hit': round(stats['submarine']['net_hit_prob'], 4),
                    'both_hit': round(stats['submarine']['both_hit_prob'], 4),
                    'any_hit': round(stats['submarine']['any_hit_prob'], 4),
                    'safe_passage': round(stats['submarine']['safe_prob'], 4)
                },
                'counts': stats['submarine']['counts']
            }
        }
    }
    
    if scenario_results:
        export_data['route_scenarios'] = {}
        for scenario_name, result in scenario_results.items():
            export_data['route_scenarios'][scenario_name] = {
                'probabilities': {
                    'mine_hit': round(result['mine_hit_prob'], 4),
                    'net_hit': round(result['net_hit_prob'], 4),
                    'both_hit': round(result['both_hit_prob'], 4),
                    'any_hit': round(result['any_hit_prob'], 4),
                    'safe_passage': round(result['safe_prob'], 4)
                },
                'counts': result['counts']
            }
    
    filename = f'{output_dir}/results_{threat_name.lower()}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Saved: results_{threat_name.lower()}.json")