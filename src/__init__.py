"""
Naval Mine Warfare Simulator
3D tactical mine field simulation and risk analysis
"""

__version__ = "3.0.0"
__author__ = "Your Name"

from .config import TacticalMineConfig, ThreatLevel, RouteScenario
from .mine_objects import SurfaceMine, MooredMine, BottomMine, Net3D
from .simulation import TacticalMineSimulation
from .visualization import create_comparison_dashboard

__all__ = [
    'TacticalMineConfig',
    'ThreatLevel',
    'RouteScenario',
    'SurfaceMine',
    'MooredMine',
    'BottomMine',
    'Net3D',
    'TacticalMineSimulation',
    'create_comparison_dashboard'
]