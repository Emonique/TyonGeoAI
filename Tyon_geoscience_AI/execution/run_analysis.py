# execution/run_analysis.py
from core import EntropyCalculator, FractalAnalyzer, ReservoirQualityIndex
import numpy as np

class FormationAnalyzer:
    """Core analysis workflow"""
    
    def __init__(self, application='groundwater', window_size=10):
        self.application = application
        self.window_size = window_size
        self.entropy_calc = EntropyCalculator()
        self.fractal_analyzer = FractalAnalyzer()
        self.results = []
        
    def analyze(self, depth, porosity, permeability, **params):
        """Run sliding window analysis"""
        results = []
        
        for i in range(len(depth) - self.window_size + 1):
            window = slice(i, i+self.window_size)
            window_depth = np.mean(depth[window])
            
            # Core calculations
            porosity_win = porosity[window]
            perm_win = permeability[window]
            
            entropy = self.entropy_calc.calculate(porosity_win)
            fractal_dim = self.fractal_analyzer.calculate(porosity_win)
            
            # Domain-specific quality index
            if self.application == 'groundwater':
                quality_index = ReservoirQualityIndex.groundwater(
                    np.mean(porosity_win), 
                    np.mean(perm_win)
                )
            elif self.application == 'hydrocarbon':
                quality_index = ReservoirQualityIndex.hydrocarbon(
                    np.mean(porosity_win), 
                    np.mean(perm_win)
                )
                
            # Risk factors (domain-specific)
            risks = self._calculate_risks(porosity_win, perm_win, params, window)
            risk_factor = 1 - (sum(risks.values()) / len(risks)) if risks else 1
            
            result = {
                'depth': window_depth,
                'quality_index': quality_index,
                'entropy': entropy,
                'fractal_dim': fractal_dim,
                'composite_score': quality_index * entropy * risk_factor,
                **risks
            }
            results.append(result)
            
        self.results = results
        return results
    
    def _calculate_risks(self, porosity, perm, params, window):
        """Calculate domain-specific risks"""
        risks = {}
        if self.application == 'groundwater':
            # High clay content risk
            if 'clay_content' in params:
                clay = np.mean(params['clay_content'][window])
                risks['high_clay_risk'] = 1 if clay > 0.35 else 0
                
            # High salinity risk
            if 'salinity' in params:
                salinity = np.mean(params['salinity'][window])
                risks['high_salinity_risk'] = 1 if salinity > 1000 else 0
                
        return risks
