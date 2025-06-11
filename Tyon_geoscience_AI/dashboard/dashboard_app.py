import streamlit as st
import pandas as pd
import numpy as np
from core import FormationAnalyzer, ZoneDetector, DrillingEfficiencyPredictor
from utils.data_loader import DataLoader
from utils.data_simulator import DataSimulator
from visualization.plot_generator import PlotGenerator

def run_dashboard():
    st.set_page_config(page_title="TYON Geoscience AI", layout="wide")
    st.title("🌍 TYON - Geoscience Analysis Platform")
    
    # Initialize session state
    if 'results' not in st.session_state:
        st.session_state.results = None
        st.session_state.target_zones = None
        st.session_state.drilling_model = DrillingEfficiencyPredictor()
        st.session_state.model_trained = False
    
    # Application selection
    app = st.sidebar.selectbox("Application", 
                              ["Groundwater", "Hydrocarbon", "Geothermal"])
    
    # Data input section
    st.sidebar.header("Data Input")
    data_source = st.sidebar.radio("Source", ["Sample Data", "Upload CSV", "Simulate Data"])
    
    well_data = None
    
    if data_source == "Sample Data":
        if app == "Groundwater":
            well_data = pd.read_csv("data/sample_groundwater.csv")
        elif app == "Hydrocarbon":
            well_data = pd.read_csv("data/sample_hydrocarbon.csv")
            
    elif data_source == "Upload CSV":
        uploaded = st.sidebar.file_uploader("Upload well data", type="csv")
        if uploaded:
            required_cols = ['depth', 'porosity', 'permeability']
            if app == "Groundwater":
                required_cols += ['clay_content', 'salinity']
            well_data = DataLoader.load_csv(uploaded, required_cols)
    
    elif data_source == "Simulate Data":
        depth_range = st.sidebar.slider("Depth Range (m)", 50, 1000, (100, 500))
        if st.sidebar.button("Generate Data"):
            if app == "Groundwater":
                well_data = DataSimulator.simulate_groundwater(depth_range)
    
    # Display data
    if well_data is not None:
        st.subheader("Well Data")
        st.dataframe(well_data.head())
        
        # Run analysis
        if st.button("Analyze Formation"):
            analyzer = FormationAnalyzer(application=app.lower())
            params = {col: well_data[col] for col in well_data.columns 
                     if col not in ['depth', 'porosity', 'permeability']}
            
            results = analyzer.analyze(
                well_data['depth'].values,
                well_data['porosity'].values,
                well_data['permeability'].values,
                **params
            )
            
            detector = ZoneDetector()
            target_zones = detector.detect(results)
            
            st.session_state.results = results
            st.session_state.target_zones = target_zones
            st.success(f"Analysis complete! Found {len(target_zones)} target zones")
    
    # Display results
    if st.session_state.results is not None:
        st.subheader("Analysis Results")
        
        # Generate visualization
        depths = [r['depth'] for r in st.session_state.results]
        quality = [r['quality_index'] for r in st.session_state.results]
        entropy = [r['entropy'] for r in st.session_state.results]
        
        fig = PlotGenerator.groundwater_analysis(
            depths, quality, entropy, st.session_state.target_zones
        )
        st.pyplot(fig)
        
        # Drilling efficiency prediction
        st.subheader("Drilling Efficiency Prediction")
        if app == "Groundwater":
            if st.button("Train Drilling Model"):
                # In real app, load historical drilling data
                X_train = np.random.rand(100, 4)  # Features: quality_index, entropy, etc.
                y_train = np.random.uniform(5, 25, 100)  # Drilling rate m/h
                r2 = st.session_state.drilling_model.train(X_train, y_train)
                st.session_state.model_trained = True
                st.info(f"Model trained with R²: {r2:.2f}")
            
            if st.session_state.model_trained and st.session_state.target_zones:
                zone = st.session_state.target_zones[0]
                features = [
                    zone['quality_index'],
                    zone['entropy'],
                    zone['fractal_dim'],
                    0.3  # Example clay content
                ]
                rate = st.session_state.drilling_model.predict(features)
                st.metric("Predicted Drilling Rate", f"{rate:.1f} m/hour")
        
        # Export results
        st.subheader("Data Export")
        if st.button("Export Analysis Results"):
            df = pd.DataFrame(st.session_state.results)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="tyon_analysis.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    run_dashboard()
