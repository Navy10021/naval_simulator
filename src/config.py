"""
Configuration classes for naval mine warfare simulation
"""

from dataclasses import dataclass
from typing import Tuple
from enum import Enum


class ThreatLevel(Enum):
    """위협 수준"""
    MODERATE = (150, 0.50)  # 기뢰 150개, 목표 위험률 50%
    HIGH = (300, 0.75)      # 기뢰 300개, 목표 위험률 75%
    CRITICAL = (450, 0.90)  # 기뢰 450개, 목표 위험률 90%


class RouteScenario(Enum):
    """경로 시나리오"""
    DIRECT = "Straight"
    ZIGZAG = "Zig-zag"
    DEEP_DIVE = "Deep Dive"
    COASTAL = "Coastal Route"


@dataclass
class TacticalMineConfig:
    """전술적 기뢰 부설 설정"""
    # Area settings
    area_width: float = 10000
    area_height: float = 10000
    max_depth: float = 280
    
    # Threat level
    threat_level: ThreatLevel = ThreatLevel.HIGH
    
    # Mine deployment strategy
    core_route_width: float = 1000  # Core route width (m)
    linear_density: float = 0.7  # Linear deployment ratio (0-1)
    random_density: float = 0.3  # Random deployment ratio (0-1)
    
    # Surface mines (3-50m depth)
    surface_mine_depth_range: Tuple[float, float] = (3, 50)
    surface_mine_spacing: Tuple[float, float] = (70, 150)
    
    # Moored/Bottom mines (30-55m depth, 30-55m spacing)
    subsurface_mine_depth_range: Tuple[float, float] = (30, 55)
    subsurface_mine_spacing: Tuple[float, float] = (30, 55)
    
    # Mine parameters
    mine_radius: float = 150
    
    # Nets
    num_nets: int = 30
    net_width: float = 50
    net_length_range: Tuple[float, float] = (300, 1000)
    net_depth_range: Tuple[float, float] = (50, 200)
    
    # Vessel parameters
    vessel_width: float = 20
    vessel_draft: float = 8
    submarine_width: float = 12
    
    # Simulation parameters
    num_simulations: int = 1000
    path_sampling_points: int = 200