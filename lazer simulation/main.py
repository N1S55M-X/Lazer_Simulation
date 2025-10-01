# laser_physics_lab.py

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

# Page config
st.set_page_config(
    page_title="Interactive Laser Physics Lab",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Physics calculations
def calculate_physics_params(lam_nm, w0_mm, M2):
    lam = lam_nm * 1e-9         # m
    w0 = w0_mm * 1e-3           # m
    zR = np.pi * w0**2 / (lam * M2)
    theta = (lam * M2) / (np.pi * w0)
    return zR, theta

def beam_radius_at_z(z_mm, w0_mm, lam_nm, M2):
    z = z_mm * 1e-3
    lam = lam_nm * 1e-9
    w0 = w0_mm * 1e-3
    zR = np.pi * w0**2 / (lam * M2)
    return w0 * np.sqrt(1 + (z / zR)**2) * M2 * 1e3  # mm

def coherence_length(linewidth_ghz):
    c = 3e8
    return c / (linewidth_ghz * 1e9)  # m

def create_beam_plot(lam, w0, M2, L, power, linewidth, rin, pointing, ej, use_ap, ap_r, f, t):
    zR, theta = calculate_physics_params(lam, w0, M2)
    Lc = coherence_length(linewidth)
    # noise
    rin_noise = 1 + 0.01 * 10**(rin/20) * np.sin(t*10)
    ej_mod = 1 + (ej/100) * np.sin(t*3)
    # figure
    fig = go.Figure()
    # envelope
    z_pts = np.linspace(0, L, 200)
    r_pts = [beam_radius_at_z(z, w0, lam, M2) for z in z_pts]
    fig.add_trace(go.Scatter(x=z_pts, y=r_pts, mode='lines', line=dict(dash='dash', color='#60A5FA')))
    fig.add_trace(go.Scatter(x=z_pts, y=[-r for r in r_pts], mode='lines', line=dict(dash='dash', color='#60A5FA')))
    # cross-sections
    positions = [0, 0.2, 0.5, 0.8, 1.0]
    colors = ['#ec4899','#a855f7','#06b6d4','#10b981','#f59e0b']
    for frac, col in zip(positions, colors):
        z0 = L * frac
        r0 = beam_radius_at_z(z0, w0, lam, M2)
        coh = 1 if z0*1e-3 < Lc else np.exp(-(z0*1e-3 - Lc)/Lc)
        alpha = np.clip(rin_noise * ej_mod * coh, 0, 1)
        fig.add_trace(go.Scatter(
            x=[z0], y=[r0],
            mode='markers', marker=dict(color=col, size=15, opacity=alpha),
            showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[z0], y=[-r0],
            mode='markers', marker=dict(color=col, size=15, opacity=alpha),
            showlegend=False
        ))
    # aperture
    if use_ap:
        fig.add_hline(y=ap_r, line_color='#fbbf24')
        fig.add_hline(y=-ap_r, line_color='#fbbf24')
    # lens
    if f > 0:
        fig.add_vline(x=L/2, line_color='#8b5cf6', line_dash='dot')
    # layout
    fig.update_layout(
        title="Beam Propagation",
        xaxis_title="Distance (mm)",
        yaxis_title="Radius (mm)",
        plot_bgcolor='#0f172a', paper_bgcolor='#1e293b',
        font_color='white', hovermode='closest'
    )
    return fig

# Session state
if 'time' not in st.session_state:
    st.session_state.time = 0.0
if 'play' not in st.session_state:
    st.session_state.play = False

# Sidebar controls
st.sidebar.header("1. Source Properties")
lam = st.sidebar.slider("λ (nm)", 400, 2000, 632, step=10)
w0 = st.sidebar.slider("w₀ (mm)", 0.1, 3.0, 0.5, step=0.1)
M2 = st.sidebar.slider("M²", 1.0, 5.0, 1.1, step=0.05)
power = st.sidebar.slider("Power (mW)", 1, 10000, 5, step=10)
pulse = st.sidebar.slider("Pulse Width (ns)", 1, 1000, 5, step=5)
rep = st.sidebar.slider("Rep Rate (kHz)", 1, 100, 10, step=1)
st.sidebar.write("Presets:")
if st.sidebar.button("He-Ne"):
    lam, w0, M2, power = 632.8, 0.5, 1.1, 5
if st.sidebar.button("Fiber"):
    lam, w0, M2, power = 1550, 0.5, 1.05, 140
if st.sidebar.button("Nd:YAG"):
    lam, w0, M2, power = 1064, 1.0, 1.2, 10000
if st.sidebar.button("Ti:Sa"):
    lam, w0, M2, power = 800, 0.6, 1.08, 1000

st.sidebar.header("2. Optical Train")
L = st.sidebar.slider("Distance L (mm)", 10, 5000, 1000, step=10)
f = st.sidebar.slider("Focal f (mm)", 0, 1000, 200, step=10)
use_ap = st.sidebar.checkbox("Enable Aperture")
ap_r = st.sidebar.slider("Aperture Radius (mm)", 0.5, 10.0, 5.0, step=0.5) if use_ap else 0

# Calculated
zR, theta = calculate_physics_params(lam, w0, M2)
spot = beam_radius_at_z(L, w0, lam, M2)
st.sidebar.markdown(f"**Rayleigh z<sub>R</sub>:** {zR*1e3:.1f} mm")
st.sidebar.markdown(f"**Divergence θ:** {theta*1e3:.3f} mrad")
st.sidebar.markdown(f"**Spot @L:** {spot:.2f} mm")

st.sidebar.header("3. Noise & Stability")
rin = st.sidebar.slider("RIN (dBc/Hz)", -165, -120, -140, step=1)
linewidth = st.sidebar.slider("Δν (GHz)", 0.0001, 10000.0, 1.5, step=0.1)
point = st.sidebar.slider("Pointing (µrad)", 0, 100, 5, step=1)
ej = st.sidebar.slider("Energy Jitter (%)", 0.0, 20.0, 2.0, step=0.5)
Lc = coherence_length(linewidth)
status = "Excellent" if Lc>10 else "Good" if Lc>1 else "Short"
st.sidebar.markdown(f"**Lc:** {Lc:.2f} m ({Lc*1e3:.0f} mm), {status}")

# Main area
st.title("⚡ Interactive Laser Physics Lab")
col1, col2 = st.columns([1,5])
with col1:
    if st.button("▶️ Play" if not st.session_state.play else "⏸️ Pause"):
        st.session_state.play = not st.session_state.play
    if st.button("🔄 Reset"):
        st.session_state.time = 0.0
with col2:
    if st.session_state.play:
        st.session_state.time += 0.1
        time.sleep(0.05)
    fig = create_beam_plot(lam, w0, M2, L, power, linewidth, rin, point, ej, use_ap, ap_r, f, st.session_state.time)
    st.plotly_chart(fig, use_container_width=True)

# Metrics
zR, theta = calculate_physics_params(lam, w0, M2)
Lc = coherence_length(linewidth)
cols = st.columns(5)
cols[0].metric("Wavelength", f"{lam} nm")
cols[1].metric("Rayleigh zR", f"{zR*1e3:.0f} mm")
cols[2].metric("Divergence θ", f"{theta*1e3:.2f} mrad")
cols[3].metric("Coherence Lc", f"{Lc:.2f} m")
cols[4].metric("Beam Quality", f"M² = {M2:.2f}")

st.markdown("---")
st.markdown("### 🔬 Try These Experiments:")
st.info("1. **Beam Divergence:** Decrease w₀ → θ increases")
st.info("2. **Focusing:** Add lens (f) → beam converges then expands")
st.info("3. **Diffraction:** Enable aperture → observe clipping effects")
st.info("4. **Coherence:** Increase Δν → Lc drops")
st.info("5. **Noise:** Increase RIN/pointing → beam flickers")
st.info("6. **Beam Quality:** Increase M² → faster divergence")
