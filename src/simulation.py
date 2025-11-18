"""
Core simulation engine for tactical mine warfare
"""

import numpy as np
from typing import List, Tuple, Dict
from .config import TacticalMineConfig, RouteScenario
from .mine_objects import SurfaceMine, MooredMine, BottomMine, Net3D
from .utils import export_results_json


class TacticalMineSimulation:
    """전술적 기뢰 부설 시뮬레이션"""
    
    def __init__(self, config: TacticalMineConfig):
        self.config = config
        self.surface_mines: List[SurfaceMine] = []
        self.moored_mines: List[MooredMine] = []
        self.bottom_mines: List[BottomMine] = []
        self.nets: List[Net3D] = []
        
        self.results = {
            'surface_vessel': {'mine_hits': 0, 'net_hits': 0, 'both_hits': 0, 'safe': 0},
            'submarine': {'mine_hits': 0, 'net_hits': 0, 'both_hits': 0, 'safe': 0}
        }
        
        self.scenario_results = {}
    
    def _calculate_core_route(self, start: Tuple[float, float], 
                             end: Tuple[float, float]) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate core route centerline and perpendicular vector"""
        direction = np.array([end[0] - start[0], end[1] - start[1]])
        direction = direction / np.linalg.norm(direction)
        perpendicular = np.array([-direction[1], direction[0]])
        return direction, perpendicular
    
    def generate_tactical_mines(self, start: Tuple[float, float], 
                                end: Tuple[float, float], 
                                seed: int = None):
        """Generate tactical mine deployment"""
        if seed is not None:
            np.random.seed(seed)
        
        total_mines = self.config.threat_level.value[0]
        
        # Mine type ratio (surface:moored:bottom = 3:4:3)
        num_surface = int(total_mines * 0.3)
        num_moored = int(total_mines * 0.4)
        num_bottom = total_mines - num_surface - num_moored
        
        direction, perpendicular = self._calculate_core_route(start, end)
        route_length = np.sqrt((end[0]-start[0])**2 + (end[1]-start[1])**2)
        
        # Deploy surface mines
        self._deploy_surface_mines(start, end, perpendicular, route_length, 
                                   num_surface)
        
        # Deploy moored mines
        self._deploy_moored_mines(start, end, perpendicular, route_length, 
                                 num_moored)
        
        # Deploy bottom mines
        self._deploy_bottom_mines(start, end, perpendicular, route_length, 
                                 num_bottom)
        
        # Deploy nets
        self._deploy_nets()
    
    def _deploy_surface_mines(self, start, end, perpendicular, route_length, num_surface):
        """Deploy surface mines"""
        self.surface_mines = []
        num_linear = int(num_surface * self.config.linear_density)
        spacing = np.random.uniform(*self.config.surface_mine_spacing)
        num_line_mines = int(route_length / spacing)
        
        # Linear deployment
        for i in range(min(num_linear, num_line_mines)):
            t = i / max(num_line_mines - 1, 1)
            base_x = start[0] + t * (end[0] - start[0])
            base_y = start[1] + t * (end[1] - start[1])
            
            offset = np.random.uniform(-self.config.core_route_width/3, 
                                      self.config.core_route_width/3)
            x = base_x + offset * perpendicular[0]
            y = base_y + offset * perpendicular[1]
            z = np.random.uniform(*self.config.surface_mine_depth_range)
            
            x = np.clip(x, 0, self.config.area_width)
            y = np.clip(y, 0, self.config.area_height)
            
            self.surface_mines.append(SurfaceMine(x, y, z, self.config.mine_radius, "linear"))
        
        # Random deployment
        num_random = num_surface - len(self.surface_mines)
        for _ in range(num_random):
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2
            
            x = np.random.normal(mid_x, self.config.area_width / 4)
            y = np.random.normal(mid_y, self.config.area_height / 4)
            z = np.random.uniform(*self.config.surface_mine_depth_range)
            
            x = np.clip(x, 0, self.config.area_width)
            y = np.clip(y, 0, self.config.area_height)
            
            self.surface_mines.append(SurfaceMine(x, y, z, self.config.mine_radius, "random"))
    
    def _deploy_moored_mines(self, start, end, perpendicular, route_length, num_moored):
        """Deploy moored mines"""
        self.moored_mines = []
        num_linear = int(num_moored * self.config.linear_density)
        spacing = np.random.uniform(*self.config.subsurface_mine_spacing)
        num_line_mines = int(route_length / spacing)
        
        # Linear deployment
        for i in range(min(num_linear, num_line_mines)):
            t = i / max(num_line_mines - 1, 1)
            base_x = start[0] + t * (end[0] - start[0])
            base_y = start[1] + t * (end[1] - start[1])
            
            offset = np.random.uniform(-self.config.core_route_width/2, 
                                      self.config.core_route_width/2)
            x = base_x + offset * perpendicular[0]
            y = base_y + offset * perpendicular[1]
            z = np.random.uniform(*self.config.subsurface_mine_depth_range)
            
            x = np.clip(x, 0, self.config.area_width)
            y = np.clip(y, 0, self.config.area_height)
            
            self.moored_mines.append(MooredMine(x, y, z, self.config.mine_radius, "linear"))
        
        # Random deployment
        num_random = num_moored - len(self.moored_mines)
        for _ in range(num_random):
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2
            
            x = np.random.normal(mid_x, self.config.area_width / 3)
            y = np.random.normal(mid_y, self.config.area_height / 3)
            z = np.random.uniform(*self.config.subsurface_mine_depth_range)
            
            x = np.clip(x, 0, self.config.area_width)
            y = np.clip(y, 0, self.config.area_height)
            
            self.moored_mines.append(MooredMine(x, y, z, self.config.mine_radius, "random"))
    
    def _deploy_bottom_mines(self, start, end, perpendicular, route_length, num_bottom):
        """Deploy bottom mines"""
        self.bottom_mines = []
        num_linear = int(num_bottom * self.config.linear_density)
        spacing = np.random.uniform(*self.config.subsurface_mine_spacing)
        num_line_mines = int(route_length / spacing)
        
        # Linear deployment
        for i in range(min(num_linear, num_line_mines)):
            t = i / max(num_line_mines - 1, 1)
            base_x = start[0] + t * (end[0] - start[0])
            base_y = start[1] + t * (end[1] - start[1])
            
            offset = np.random.uniform(-self.config.core_route_width/2, 
                                      self.config.core_route_width/2)
            x = base_x + offset * perpendicular[0]
            y = base_y + offset * perpendicular[1]
            
            x = np.clip(x, 0, self.config.area_width)
            y = np.clip(y, 0, self.config.area_height)
            
            self.bottom_mines.append(BottomMine(x, y, self.config.max_depth, 
                                               self.config.mine_radius, "linear"))
        
        # Random deployment
        num_random = num_bottom - len(self.bottom_mines)
        for _ in range(num_random):
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2
            
            x = np.random.normal(mid_x, self.config.area_width / 3)
            y = np.random.normal(mid_y, self.config.area_height / 3)
            
            x = np.clip(x, 0, self.config.area_width)
            y = np.clip(y, 0, self.config.area_height)
            
            self.bottom_mines.append(BottomMine(x, y, self.config.max_depth, 
                                               self.config.mine_radius, "random"))
    
    def _deploy_nets(self):
        """Deploy nets"""
        self.nets = []
        for _ in range(self.config.num_nets):
            x1 = np.random.uniform(0, self.config.area_width)
            y1 = np.random.uniform(0, self.config.area_height)
            
            length = np.random.uniform(*self.config.net_length_range)
            angle = np.random.uniform(0, 2 * np.pi)
            
            x2 = np.clip(x1 + length * np.cos(angle), 0, self.config.area_width)
            y2 = np.clip(y1 + length * np.sin(angle), 0, self.config.area_height)
            
            z_top = np.random.uniform(*self.config.net_depth_range)
            z_bottom = z_top + np.random.uniform(50, 150)
            
            self.nets.append(Net3D(x1, y1, x2, y2, z_top, z_bottom, self.config.net_width))
    
    def generate_path_2d(self, start: Tuple[float, float], 
                        end: Tuple[float, float]) -> np.ndarray:
        """Generate 2D path for surface vessel"""
        t = np.linspace(0, 1, self.config.path_sampling_points)
        x = start[0] + t * (end[0] - start[0])
        y = start[1] + t * (end[1] - start[1])
        z = np.zeros_like(x)
        return np.column_stack([x, y, z])
    
    def generate_path_3d(self, start: Tuple[float, float, float], 
                        end: Tuple[float, float, float]) -> np.ndarray:
        """Generate 3D path for submarine"""
        t = np.linspace(0, 1, self.config.path_sampling_points)
        x = start[0] + t * (end[0] - start[0])
        y = start[1] + t * (end[1] - start[1])
        z = start[2] + t * (end[2] - start[2])
        return np.column_stack([x, y, z])
    
    def generate_scenario_path(self, scenario: RouteScenario, 
                              start: Tuple[float, float, float],
                              end: Tuple[float, float, float]) -> np.ndarray:
        """Generate path based on scenario"""
        if scenario == RouteScenario.DIRECT:
            return self.generate_path_3d(start, end)
        
        elif scenario == RouteScenario.ZIGZAG:
            waypoints = []
            num_zigs = 5
            for i in range(num_zigs):
                t = (i + 1) / (num_zigs + 1)
                x = start[0] + t * (end[0] - start[0])
                y = start[1] + t * (end[1] - start[1])
                offset = 800 * (-1 if i % 2 == 0 else 1)
                y += offset
                z = start[2] + t * (end[2] - start[2])
                waypoints.append((x, y, z))
            
            paths = [self.generate_path_3d(start, waypoints[0])]
            for i in range(len(waypoints) - 1):
                paths.append(self.generate_path_3d(waypoints[i], waypoints[i+1]))
            paths.append(self.generate_path_3d(waypoints[-1], end))
            
            return np.vstack(paths)
        
        elif scenario == RouteScenario.DEEP_DIVE:
            mid_x = (start[0] + end[0]) / 2
            mid_y = (start[1] + end[1]) / 2
            mid_z = min(250, self.config.max_depth - 30)
            mid = (mid_x, mid_y, mid_z)
            
            path1 = self.generate_path_3d(start, mid)
            path2 = self.generate_path_3d(mid, end)
            return np.vstack([path1, path2])
        
        elif scenario == RouteScenario.COASTAL:
            waypoint1 = (start[0] + 1000, 500, start[2])
            waypoint2 = (end[0] - 1000, 500, end[2])
            
            path1 = self.generate_path_3d(start, waypoint1)
            path2 = self.generate_path_3d(waypoint1, waypoint2)
            path3 = self.generate_path_3d(waypoint2, end)
            
            return np.vstack([path1, path2, path3])
    
    def check_surface_vessel_safety(self, path: np.ndarray) -> Tuple[bool, bool]:
        """Check safety for surface vessel"""
        mine_hit = any(mine.check_collision_2d(path, self.config.vessel_width,
                                               self.config.vessel_draft)
                      for mine in self.surface_mines)
        
        net_hit = any(net.check_collision_2d(path, self.config.vessel_width,
                                             self.config.vessel_draft)
                     for net in self.nets)
        
        return mine_hit, net_hit
    
    def check_submarine_safety(self, path: np.ndarray) -> Tuple[bool, bool]:
        """Check safety for submarine"""
        mine_hit = False
        
        for mine in self.surface_mines:
            if mine.check_collision_3d(path, self.config.submarine_width):
                mine_hit = True
                break
        
        if not mine_hit:
            for mine in self.moored_mines:
                if mine.check_collision_3d(path, self.config.submarine_width):
                    mine_hit = True
                    break
        
        if not mine_hit:
            for mine in self.bottom_mines:
                if mine.check_collision_3d(path, self.config.submarine_width):
                    mine_hit = True
                    break
        
        net_hit = any(net.check_collision_3d(path, self.config.submarine_width)
                     for net in self.nets)
        
        return mine_hit, net_hit
    
    def run_simulation(self, 
                      surface_start: Tuple[float, float],
                      surface_end: Tuple[float, float],
                      sub_start: Tuple[float, float, float],
                      sub_end: Tuple[float, float, float],
                      num_iterations: int = None,
                      verbose: bool = True) -> Dict:
        """Run main simulation"""
        if num_iterations is None:
            num_iterations = self.config.num_simulations
        
        self.results = {
            'surface_vessel': {'mine_hits': 0, 'net_hits': 0, 'both_hits': 0, 'safe': 0},
            'submarine': {'mine_hits': 0, 'net_hits': 0, 'both_hits': 0, 'safe': 0}
        }
        
        print_interval = max(1, num_iterations // 20)
        
        for i in range(num_iterations):
            self.generate_tactical_mines(surface_start, surface_end, seed=i)
            
            # Surface vessel
            surface_path = self.generate_path_2d(surface_start, surface_end)
            mine_hit, net_hit = self.check_surface_vessel_safety(surface_path)
            
            if mine_hit and net_hit:
                self.results['surface_vessel']['both_hits'] += 1
            elif mine_hit:
                self.results['surface_vessel']['mine_hits'] += 1
            elif net_hit:
                self.results['surface_vessel']['net_hits'] += 1
            else:
                self.results['surface_vessel']['safe'] += 1
            
            # Submarine
            sub_path = self.generate_path_3d(sub_start, sub_end)
            mine_hit, net_hit = self.check_submarine_safety(sub_path)
            
            if mine_hit and net_hit:
                self.results['submarine']['both_hits'] += 1
            elif mine_hit:
                self.results['submarine']['mine_hits'] += 1
            elif net_hit:
                self.results['submarine']['net_hits'] += 1
            else:
                self.results['submarine']['safe'] += 1
            
            if verbose and (i + 1) % print_interval == 0:
                progress = (i + 1) / num_iterations * 100
                print(f"Progress: {progress:.1f}% ({i+1}/{num_iterations})")
        
        return self.calculate_statistics(num_iterations)
    
    def run_scenario_comparison(self,
                               sub_start: Tuple[float, float, float],
                               sub_end: Tuple[float, float, float],
                               num_iterations: int = 100) -> Dict:
        """Compare multiple route scenarios"""
        print("\n" + "="*80)
        print("ROUTE SCENARIO COMPARISON".center(80))
        print("="*80)
        
        scenarios = list(RouteScenario)
        scenario_results = {}
        
        for scenario in scenarios:
            print(f"\nTesting {scenario.value} scenario...")
            
            results = {'mine_hits': 0, 'net_hits': 0, 'both_hits': 0, 'safe': 0}
            
            for i in range(num_iterations):
                self.generate_tactical_mines((sub_start[0], sub_start[1]), 
                                            (sub_end[0], sub_end[1]), seed=i)
                
                path = self.generate_scenario_path(scenario, sub_start, sub_end)
                mine_hit, net_hit = self.check_submarine_safety(path)
                
                if mine_hit and net_hit:
                    results['both_hits'] += 1
                elif mine_hit:
                    results['mine_hits'] += 1
                elif net_hit:
                    results['net_hits'] += 1
                else:
                    results['safe'] += 1
            
            total = num_iterations
            scenario_results[scenario.value] = {
                'mine_hit_prob': results['mine_hits'] / total,
                'net_hit_prob': results['net_hits'] / total,
                'both_hit_prob': results['both_hits'] / total,
                'any_hit_prob': (results['mine_hits'] + results['net_hits'] + 
                               results['both_hits']) / total,
                'safe_prob': results['safe'] / total,
                'counts': results
            }
            
            print(f"  Safe: {scenario_results[scenario.value]['safe_prob']*100:.1f}%, "
                  f"Risk: {scenario_results[scenario.value]['any_hit_prob']*100:.1f}%")
        
        self.scenario_results = scenario_results
        return scenario_results
    
    def calculate_statistics(self, total: int) -> Dict:
        """Calculate statistics"""
        stats = {}
        
        for vessel_type in ['surface_vessel', 'submarine']:
            r = self.results[vessel_type]
            stats[vessel_type] = {
                'mine_hit_prob': r['mine_hits'] / total,
                'net_hit_prob': r['net_hits'] / total,
                'both_hit_prob': r['both_hits'] / total,
                'any_hit_prob': (r['mine_hits'] + r['net_hits'] + r['both_hits']) / total,
                'safe_prob': r['safe'] / total,
                'counts': r
            }
        
        return stats