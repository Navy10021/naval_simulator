"""
Mine and net objects for naval warfare simulation
"""

import numpy as np
from typing import Tuple


class SurfaceMine:
    """부유 기뢰 (Surface mine)"""
    
    def __init__(self, x: float, y: float, z: float, radius: float, 
                 placement_type: str = "random"):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.type = "surface"
        self.placement_type = placement_type
    
    def check_collision_2d(self, path_points: np.ndarray, vessel_width: float, 
                          vessel_draft: float) -> bool:
        """Check 2D collision with surface vessel"""
        if vessel_draft < self.z:
            return False
        distances = np.sqrt((path_points[:, 0] - self.x)**2 + 
                          (path_points[:, 1] - self.y)**2)
        return np.any(distances <= (self.radius + vessel_width/2))
    
    def check_collision_3d(self, path_points: np.ndarray, vessel_width: float) -> bool:
        """Check 3D collision with submarine"""
        surface_points = path_points[path_points[:, 2] <= self.z + 20]
        if len(surface_points) == 0:
            return False
        distances = np.sqrt((surface_points[:, 0] - self.x)**2 + 
                          (surface_points[:, 1] - self.y)**2)
        return np.any(distances <= (self.radius + vessel_width/2))


class MooredMine:
    """계류 기뢰 (Moored mine)"""
    
    def __init__(self, x: float, y: float, z: float, radius: float, 
                 placement_type: str = "random"):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius
        self.type = "moored"
        self.placement_type = placement_type
    
    def check_collision_3d(self, path_points: np.ndarray, vessel_width: float) -> bool:
        """Check 3D collision"""
        distances = np.sqrt((path_points[:, 0] - self.x)**2 + 
                          (path_points[:, 1] - self.y)**2 +
                          (path_points[:, 2] - self.z)**2)
        return np.any(distances <= (self.radius + vessel_width/2))


class BottomMine:
    """침저 기뢰 (Bottom mine)"""
    
    def __init__(self, x: float, y: float, z_bottom: float, radius: float, 
                 placement_type: str = "random"):
        self.x = x
        self.y = y
        self.z = z_bottom
        self.radius = radius
        self.type = "bottom"
        self.placement_type = placement_type
    
    def check_collision_3d(self, path_points: np.ndarray, vessel_width: float) -> bool:
        """Check 3D collision"""
        distances = np.sqrt((path_points[:, 0] - self.x)**2 + 
                          (path_points[:, 1] - self.y)**2 +
                          (path_points[:, 2] - self.z)**2)
        return np.any(distances <= (self.radius + vessel_width/2))


class Net3D:
    """닻자망 (3D Net)"""
    
    def __init__(self, x1: float, y1: float, x2: float, y2: float, 
                 depth_top: float, depth_bottom: float, width: float):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.z_top = depth_top
        self.z_bottom = depth_bottom
        self.width = width
        self.length = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        self.type = "net"
    
    def check_collision_2d(self, path_points: np.ndarray, vessel_width: float,
                          vessel_draft: float) -> bool:
        """Check 2D collision with surface vessel"""
        if vessel_draft < self.z_top:
            return False
        
        total_width = (self.width + vessel_width) / 2
        
        for i in range(len(path_points) - 1):
            p1 = path_points[i, :2]
            p2 = path_points[i + 1, :2]
            
            if self._segment_intersects_2d(p1, p2, total_width):
                return True
        
        return False
    
    def check_collision_3d(self, path_points: np.ndarray, vessel_width: float) -> bool:
        """Check 3D collision with submarine"""
        total_width = (self.width + vessel_width) / 2
        
        for i in range(len(path_points) - 1):
            p1 = path_points[i]
            p2 = path_points[i + 1]
            
            if not (self.z_top <= p1[2] <= self.z_bottom or 
                   self.z_top <= p2[2] <= self.z_bottom):
                continue
            
            if self._segment_intersects_2d(p1[:2], p2[:2], total_width):
                return True
        
        return False
    
    def _segment_intersects_2d(self, p1: np.ndarray, p2: np.ndarray, 
                              safe_distance: float) -> bool:
        """Check if two 2D segments intersect within safe distance"""
        q1 = np.array([self.x1, self.y1])
        q2 = np.array([self.x2, self.y2])
        
        dist1 = self._point_to_segment_distance(p1, q1, q2)
        dist2 = self._point_to_segment_distance(p2, q1, q2)
        dist3 = self._point_to_segment_distance(q1, p1, p2)
        dist4 = self._point_to_segment_distance(q2, p1, p2)
        
        return min(dist1, dist2, dist3, dist4) <= safe_distance
    
    def _point_to_segment_distance(self, point: np.ndarray, 
                                   seg_start: np.ndarray, seg_end: np.ndarray) -> float:
        """Calculate minimum distance from point to line segment"""
        segment = seg_end - seg_start
        point_vec = point - seg_start
        
        segment_length_sq = np.dot(segment, segment)
        
        if segment_length_sq < 1e-6:
            return np.linalg.norm(point - seg_start)
        
        t = np.clip(np.dot(point_vec, segment) / segment_length_sq, 0, 1)
        projection = seg_start + t * segment
        
        return np.linalg.norm(point - projection)