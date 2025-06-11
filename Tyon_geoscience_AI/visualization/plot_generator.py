# visualization/plot_generator.py
import matplotlib.pyplot as plt
import numpy as np

class PlotGenerator:
    """Creates domain-specific visualizations"""
    
    @staticmethod
    def groundwater_analysis(depths, quality, entropy, target_zones):
        """Generate groundwater-specific plot"""
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # Flow Capacity (Primary)
        ax1.plot(quality, depths, 'g-', label='Flow Capacity Index')
        ax1.set_xlabel('Flow Capacity Index', color='g')
        ax1.set_ylabel('Depth (m)', color='k')
        ax1.tick_params(axis='x', labelcolor='g')
        ax1.invert_yaxis()
        ax1.grid(True, linestyle='--', alpha=0.3)
        
        # Entropy (Secondary)
        ax2 = ax1.twiny()
        ax2.plot(entropy, depths, 'b-', label='Entropy')
        ax2.set_xlabel('Entropy (bits)', color='b')
        ax2.tick_params(axis='x', labelcolor='b')
        
        # Highlight target zones
        for zone in target_zones:
            ax1.axhspan(zone['depth']-5, zone['depth']+5, alpha=0.3, color='green')
        
        # Highlight risk zones
        plt.title('Groundwater Potential Analysis')
        fig.tight_layout()
        return fig
    
    @staticmethod
    def hydrocarbon_analysis(...):
        # Domain-specific plot for hydrocarbons
        ...
