# 🔬 Interactive Laser Physics Lab

A real-time **laser beam simulator** for learning and research prototyping.  
Adjust wavelength, waist, **M²** beam quality, lens/aperture, and noise (RIN, linewidth, pointing, energy jitter).  
See **beam propagation**, **divergence**, **Rayleigh range**, and **coherence length** update live.

---

## 📖 What this simulation does
This project models **Gaussian beam optics** interactively.  
It’s designed to:
- Build **intuition** (equations → visuals)
- Run **what-if experiments** quickly
- Provide **research-realistic defaults** (He–Ne, Fiber, Nd:YAG, Ti:Sa)

### Research properties included
- Wavelength (λ)
- Beam waist (w₀)
- Beam quality (M²)
- Rayleigh range (zR), divergence (θ)
- Coherence length (Lc) from linewidth Δν
- RIN (Relative Intensity Noise)
- Pointing jitter, energy jitter
- Lens (focal length) and aperture clipping

---

## 🧠 Physics behind it
- **Gaussian beam width**  
  `w(z) = w0 * sqrt(1 + (z/zR)^2)`  
  with `zR = π w0² / (λ M²)`  

- **Beam quality M²**  
  Larger M² → worse focusability, faster divergence.  

- **Coherence length**  
  `Lc = c / (π Δν)`  

- **Noise**  
  Simple sinusoidal models for RIN, pointing, jitter.

---

## ✅ Strengths
- Interactive **virtual lab** (learn faster than equations alone)
- Research-relevant parameters (M², RIN, linewidth)
- Two versions:
  - **React (Vite)** → Web demo (GitHub Pages)
  - **Python (Streamlit)** → Research app, easy to extend

## ⚠️ Weaknesses
- Simplified Gaussian model (no vector diffraction/polarization)
- Noise is approximate (for intuition, not metrology)
- No full cavity/nonlinear optics yet

## 🧪 Try these experiments

Decrease w₀ → divergence θ increases

Increase M² → Rayleigh range shrinks

Add a lens (f) → watch beam refocus

Enable aperture → see clipping effects

Increase Δν → coherence length drops

Add RIN/pointing → beam flickers

## 📚 References

ISO 11146 (Beam quality M² standard)

Gaussian beam optics (Kogelnik formalism)

Vendor datasheets (He–Ne, Nd:YAG, Ti:Sa, Fiber lasers)

## 📝 License

MIT License — free to use and modify.


