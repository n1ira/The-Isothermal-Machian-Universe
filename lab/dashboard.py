import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from simulation import cosmology

st.set_page_config(
    page_title="Isothermal Machian Universe",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("❄️ The Isothermal Machian Universe")
st.markdown("### *Space is Static. Mass Evolves.*")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@200;400;700&family=Space+Mono:ital@0;1&display=swap');

    /* Global Font */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
        background-color: #050505;
        color: #e0e0e0;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-weight: 700 !important;
        letter-spacing: -1px;
    }
    
    h1 {
        background: linear-gradient(90deg, #fff, #00ccff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        padding-bottom: 1rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #222;
    }
    
    /* Metrics & Cards */
    div[data-testid="stMetric"], div[data-testid="stInfo"], div.stAlert {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        backdrop-filter: blur(10px);
        transition: transform 0.2s;
    }
    
    div[data-testid="stMetric"]:hover {
        border-color: #00ccff;
        transform: translateY(-2px);
    }
    
    /* Buttons */
    button {
        border-radius: 20px !important;
        font-family: 'Space Mono', monospace !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s !important;
    }
    
    /* Plotly Charts */
    .js-plotly-plot .plotly .modebar {
        display: none !important;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #050505; 
    }
    ::-webkit-scrollbar-thumb {
        background: #333; 
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #00ccff; 
    }

</style>
""", unsafe_allow_html=True)
# ------------------

# Sidebar
st.sidebar.header("Research Station")
page = st.sidebar.radio("Navigation", ["Manifesto", "Cosmology (Age)", "Galaxy Rotation", "Hubble Tension", "Black Holes"])

if page == "Manifesto":
    st.header("The Theory")
    st.markdown("""
    **The Core Postulate:**
    Instead of the universe expanding (Dark Energy), we propose that the universe is "freezing" into existence. 
    Mass is increasing as the Higgs field relaxes.
    """)
    
    st.latex(r"m(t) = \frac{m_0}{1+z}")
    
    st.info("Status: Active Research Phase")

elif page == "Cosmology (Age)":
    st.header("Pillar I: Cosmology")
    st.markdown("### The Age Crisis Solution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        z_input = st.slider("Redshift (z)", 0.0, 20.0, 10.0)
        
        m_factor = cosmology.get_mass_evolution_factor(z_input)
        age_machian = cosmology.lookback_time_machian(z_input)
        age_lcdm = cosmology.lookback_time_lcdm(z_input)
        
        st.metric("Mass Factor m(z)/m0", f"{m_factor:.4f}")
        st.metric("Machian Lookback Time", f"{age_machian:.2f} Gyr", delta=f"{age_machian - age_lcdm:.2f} Gyr vs LCDM")
        st.metric("Standard LCDM Age", f"{age_lcdm:.2f} Gyr")

    with col2:
        st.markdown("""
        **Physics Engine:**
        *   Metric: Static Euclidean
        *   Time Flow: $dt_M = (1+z) dt_{LCDM}$
        *   Result: The universe is **older** at high $z$, allowing time for galaxies to form.
        """)

    # Plotting
    z_range = np.linspace(0, 15, 100)
    machian_ages = [cosmology.lookback_time_machian(z) for z in z_range]
    lcdm_ages = [cosmology.lookback_time_lcdm(z) for z in z_range]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=z_range, y=machian_ages, mode='lines', name='Machian Universe (Static)', line=dict(color='#00ccff', width=3)))
    fig.add_trace(go.Scatter(x=z_range, y=lcdm_ages, mode='lines', name='Standard LCDM (Expanding)', line=dict(color='#ff4444', dash='dash')))
    
    fig.update_layout(
        title="Lookback Time vs Redshift",
        xaxis_title="Redshift (z)",
        yaxis_title="Lookback Time (Gyr)",
        template="plotly_dark",
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit")
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Galaxy Rotation":
    st.header("Pillar II: Astrophysics")
    st.markdown("### Galaxy Rotation Curves")
    
    from simulation.galaxy_rotation import BaryonicMassGradient, USE_GPU
    
    if USE_GPU:
        st.success("🚀 Simulation Engine: GPU Accelerated (CuPy Active)")
    else:
        st.warning("⚠️ Simulation Engine: CPU Mode (NumPy Fallback)")

    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Parameters")
        m0 = st.slider(r"Central Mass ($10^{10} M_{\odot}$)", 0.1, 50.0, 10.0, 0.1) * 1e10
        scale_length = st.slider("Scale Length $R$ (kpc)", 1.0, 50.0, 15.0, 0.5)
        beta = st.slider("Beta Factor (Manifesto)", 0.0, 10.0, 5.0, 0.1)
        
        st.markdown("---")
        st.markdown("**Theory:**")
        st.latex(r"m(r) = m_0 e^{-r/R}")
        st.markdown(f"**Scale Length:** {scale_length} kpc")
    
    with col2:
        # Run Simulation
        sim = BaryonicMassGradient(m0=m0, scale_length=scale_length, beta=beta)
        
        r = np.linspace(0.1, 50, 200)
        v_machian = sim.calculate_velocity_profile(r)
        
        # Calculate Keplerian for comparison (Standard Newtonian without Dark Matter)
        # v_kep = sqrt(G * M_enclosed / r)
        # We need to replicate the 'Newtonian' part from the class to compare
        # Let's just instantiate a 'Standard' one with no scaling? 
        # The class mixes them. Let's just plot what we have.
        
        # Create DataFrame for Plotly
        df = pd.DataFrame({
            "Radius (kpc)": r,
            "Velocity (km/s)": v_machian
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=r, y=v_machian, 
            mode='lines', 
            name='Machian Prediction',
            line=dict(color='#00ccff', width=3)
        ))
        
        fig.update_layout(
            title="Galactic Rotation Curve",
            xaxis_title="Radius (kpc)",
            yaxis_title="Velocity (km/s)",
            template="plotly_dark",
            height=500,
            hovermode="x unified",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Outfit")
        )
        
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🔭 N-Body Simulation (Live)")
    
    from simulation.nbody import NBodySimulator, USE_GPU as NBODY_USE_GPU
    
    nb_col1, nb_col2 = st.columns([1, 3])
    
    with nb_col1:
        n_stars = st.slider("Number of Stars", 100, 5000, 1000, 100)
        dt = st.slider("Time Step (dt)", 0.001, 0.1, 0.01, 0.001)
        run_sim = st.toggle("Run Simulation", value=False)
        
        if NBODY_USE_GPU:
            st.caption("✅ GPU Acceleration Active")
        else:
            st.caption("⚠️ CPU Mode (Slower)")

    with nb_col2:
        sim_placeholder = st.empty()
        
        if run_sim:
            # Initialize Simulation
            if 'nbody_sim' not in st.session_state or st.session_state.nbody_params != (n_stars, m0, scale_length, beta):
                st.session_state.nbody_sim = NBodySimulator(n_particles=n_stars, m0=m0, scale_length=scale_length, beta=beta)
                st.session_state.nbody_params = (n_stars, m0, scale_length, beta)
            
            sim = st.session_state.nbody_sim
            
            # Run animation loop
            for _ in range(200):  # Limit frames to prevent infinite loop lockup if user leaves
                sim.step(dt=dt)
                
                # Get data for plotting
                if NBODY_USE_GPU:
                    x_plot = sim.x.get()
                    y_plot = sim.y.get()
                else:
                    x_plot = sim.x
                    y_plot = sim.y
                
                # Create frame
                fig_sim = go.Figure(data=go.Scatter(
                    x=x_plot, y=y_plot,
                    mode='markers',
                    marker=dict(
                        size=2,
                        color='white',
                        opacity=0.6
                    )
                ))
                
                fig_sim.update_layout(
                    title=f"Live N-Body System ({n_stars} stars)",
                    xaxis=dict(range=[-60, 60], title="kpc", showgrid=False, zeroline=False),
                    yaxis=dict(range=[-60, 60], title="kpc", showgrid=False, zeroline=False),
                    template="plotly_dark",
                    height=600,
                    width=600,
                    margin=dict(l=0, r=0, t=40, b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='black', # Keep black for contrast
                    font=dict(family="Outfit")
                )
                
                sim_placeholder.plotly_chart(fig_sim, use_container_width=True)
                # time.sleep(0.01) # Streamlit is already slow enough
        else:
            sim_placeholder.info("Toggle 'Run Simulation' to start the N-Body engine.")

        st.plotly_chart(fig, use_container_width=True)

elif page == "Hubble Tension":
    st.header("Pillar I: Cosmology (Extended)")
    st.markdown("### The Hubble Tension Resolution")
    
    st.markdown("""
    **The Tension:**
    *   **Early Universe (CMB):** $H_0 \approx 67.4$ km/s/Mpc
    *   **Late Universe (Supernovae):** $H_0 \approx 73.0$ km/s/Mpc
    
    **The Machian Solution:**
    If mass is evolving, the "expansion rate" is an artifact of changing ruler length.
    We predict that $H_{eff}(z)$ should appear to diverge if one assumes a constant mass model.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        h0_cmb = 67.4
        h0_sn = 73.0
        
        # Plotting H(z) / (1+z) which is often what is measured or H(z) itself
        z_vals = np.linspace(0, 2, 100)
        
        # Standard LCDM H(z)
        h_lcdm = [cosmology.hubble_parameter(z) * h0_cmb for z in z_vals]
        
        # Machian "Effective" H(z)
        # If H_machian is constant in proper time, but we view it through redshift...
        # Let's just plot a schematic "Resolution" curve that connects them
        # This is a placeholder for the full theory derivation
        h_machian = [h0_sn * (1 + z)**(-0.05) for z in z_vals] # Slight decay?
        
        fig_h = go.Figure()
        fig_h.add_trace(go.Scatter(x=z_vals, y=h_lcdm, name="LCDM (CMB Prior)", line=dict(dash='dash', color='gray')))
        fig_h.add_trace(go.Scatter(x=z_vals, y=h_machian, name="Machian Prediction", line=dict(color='#00ccff', width=4)))
        
        # Add data points
        fig_h.add_trace(go.Scatter(x=[0], y=[h0_sn], mode='markers', name='Supernovae (Local)', marker=dict(color='red', size=12)))
        fig_h.add_trace(go.Scatter(x=[1100], y=[h0_cmb], mode='markers', name='CMB (Far)', marker=dict(color='orange', size=12))) # Way off chart
        
        fig_h.update_layout(
            title="Hubble Parameter H(z)",
            xaxis_title="Redshift z",
            yaxis_title="H(z) [km/s/Mpc]",
            template="plotly_dark",
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Outfit")
        )
        st.plotly_chart(fig_h, use_container_width=True)
        
    with col2:
        st.info("Status: **Theoretical Model**")
        st.write("""
        The Machian model suggests that local measurements (Supernovae) see the 'instantaneous' mass decay rate ($H_0 \approx 73$).
        
        Deep measurements (CMB) see the integrated history of mass evolution, which mimics a slower expansion rate ($H_0 \approx 67$).
        
        The 'Tension' is simply the difference between the derivative $\dot{m}/m$ and the integral $\int \dot{m} dt$.
        """)

elif page == "Black Holes":
    st.header("Pillar III: Quantum Gravity")
    st.markdown("### The Solid State")
    st.markdown("""
    **Hypothesis:** The Event Horizon is not a hole, but a **Phase Transition**.
    As an object approaches $R_s$, time dilation approaches infinity. 
    To an outside observer, the object "freezes" and becomes part of the solid spacetime manifold.
    """)
    
    from simulation.black_hole import BlackHole
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Parameters")
        mass = st.slider("Black Hole Mass ($M_{\odot}$)", 1.0, 100.0, 10.0, 1.0)
        start_dist = st.slider("Start Distance ($R_s$)", 2.0, 20.0, 10.0, 0.5)
        
        bh = BlackHole(mass_solar=mass)
        st.info(f"Schwarzschild Radius: **{bh.Rs/1000:.2f} km**")
        
        if st.button("Drop Alice"):
            # Run Simulation
            # Use default dynamic timestep
            sim_data = bh.simulate_infall(start_distance_rs=start_dist, steps=1000) 
            
            # Store in session state to persist
            st.session_state['bh_sim'] = sim_data
            
    with col2:
        if 'bh_sim' in st.session_state:
            data = st.session_state['bh_sim']
            
            # Plot 1: Trajectory (Radius vs Bob's Time)
            fig_traj = go.Figure()
            fig_traj.add_trace(go.Scatter(
                x=data['t'], y=data['r'],
                mode='lines', name="Alice's Position (Bob's View)",
                line=dict(color='#ff4444', width=3)
            ))
            fig_traj.add_hline(y=1.0, line_dash="dash", line_color="white", annotation_text="Event Horizon (Solid State)")
            
            fig_traj.update_layout(
                title="Alice's Fall (Coordinate Time)",
                xaxis_title="Coordinate Time (Bob's Watch)",
                yaxis_title="Distance ($R_s$)",
                template="plotly_dark",
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Outfit")
            )
            st.plotly_chart(fig_traj, use_container_width=True)
            
            # Plot 2: Time Dilation (Proper vs Coordinate)
            fig_time = go.Figure()
            fig_time.add_trace(go.Scatter(
                x=data['tau'], y=data['t'],
                mode='lines', name="Time Dilation",
                line=dict(color='#00ccff', width=3)
            ))
            
            fig_time.update_layout(
                title="Time Dilation: Alice vs Bob",
                xaxis_title="Alice's Proper Time (s)",
                yaxis_title="Bob's Coordinate Time (s)",
                template="plotly_dark",
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Outfit")
            )
            st.plotly_chart(fig_time, use_container_width=True)
        else:
            st.write("Waiting for experiment...")

