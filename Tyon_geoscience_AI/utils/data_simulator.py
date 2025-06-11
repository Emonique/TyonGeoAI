# utils/data_simulator.py
import numpy as np
import pandas as pd

class DataSimulator:
    """Generates synthetic well log data for testing"""
    
    @staticmethod
    def simulate_groundwater(depth_range=(50, 500), n_points=100):
        """Generate realistic groundwater formation data"""
        depth = np.linspace(depth_range[0], depth_range[1], n_points)
        
        # Base geological patterns
        porosity = 15 + 10 * np.sin(depth/50) + np.random.normal(0, 3, n_points)
        permeability = 80 * np.exp(-depth/300) + np.random.normal(0, 15, n_points)
        clay_content = np.clip(0.3 - 0.0005*depth + np.random.normal(0, 0.05, n_points), 0.05, 0.6)
        salinity = np.clip(300 + 5*depth + np.random.normal(0, 100, n_points), 100, 3000)
        
        return pd.DataFrame({
            'depth': depth,
            'porosity': np.clip(porosity, 5, 35),
            'permeability': np.clip(permeability, 1, 300),
            'clay_content': clay_content,
            'salinity': salinity
        })
    
    @staticmethod
    def simulate_hydrocarbon(depth_range=(1500, 3000), n_points=100):
        """Generate hydrocarbon reservoir data"""
        # Similar patterns but different depth ranges and parameters
        ...
