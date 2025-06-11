# utils/data_loader.py
import pandas as pd
import numpy as np

class DataLoader:
    """Handles data loading and validation"""
    
    @staticmethod
    def load_csv(file_path, required_columns):
        """Load and validate CSV data"""
        df = pd.read_csv(file_path)
        missing = [col for col in required_columns if col not in df.columns]
        
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
            
        # Basic data validation
        if df.isnull().sum().sum() > 0:
            df = DataLoader._handle_missing_data(df)
            
        return {col: df[col].values for col in df.columns}
    
    @staticmethod
    def _handle_missing_data(df, max_missing=0.1):
        """Simple missing data handling"""
        # Drop columns with too much missing data
        df = df.dropna(axis=1, thresh=int(len(df)*(1-max_missing)))
        
        # Interpolate remaining missing values
        return df.interpolate().fillna(method='bfill')
