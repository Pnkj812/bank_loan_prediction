import streamlit as st
import pickle
import streamlit.components.v1 as components

st.set_page_config(page_title="Loan Predictor", layout="centered", initial_sidebar_state="collapsed")

# ─── Dark/Light Mode Toggle ───────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Color tokens
if st.session_state.dark_mode:
    BG = "#0f172a"
    CARD = "#1e293b"
    ACCENT = "#60a5fa"
    HEADING = "#93c5fd"
    TEXT = "#94a3b8"
    BORDER = "#334155"
    INPUT_BG = "#1e293b"
    INPUT_TXT = "#e2e8f0"
    SUB_CARD = "#0f172a"
    BTN_BG = "#3b82f6"
    BTN_TXT = "#ffffff"
    BTN_HOVER = "#2563eb"
    OK_CLR = "#60a5fa"
    ERR_CLR = "#f87171"
    LBL_CLR = "#60a5fa"
    MODE_ICON = "☀️"
    MODE_LBL = "Light Mode"
else:
    BG = "#eaf0f6"
    CARD = "#ffffff"
    ACCENT = "#1d4ed8"
    HEADING = "#1d4ed8"
    TEXT = "#475569"
    BORDER = "#dbeafe"
    INPUT_BG = "#f8fafc"
    INPUT_TXT = "#1e293b"
    SUB_CARD = "#f0f7ff"
    BTN_BG = "#1d4ed8"
    BTN_TXT = "#ffffff"
    BTN_HOVER = "#1e40af"
    OK_CLR = "#1d4ed8"
    ERR_CLR = "#dc2626"
    LBL_CLR = "#1d4ed8"
    MODE_ICON = "🌙"
    MODE_LBL = "Dark Mode"

custom_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    transition: background-color 0.3s ease, color 0.3s ease;
}}

.stApp {{
    background-color: {BG};
}}

.main .block-container {{
    background-color: {CARD};
    padding: 2.5rem 3.5rem;
    border-radius: 20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.08);
    max-width: 860px;
    margin-top: 2rem;
    margin-bottom: 2rem;
}}

header {{visibility: hidden;}}
footer {{visibility: hidden;}}
#MainMenu {{visibility: hidden;}}

/* ── Headings ── */
h1 {{
    color: {HEADING} !important;
    font-weight: 700;
    font-size: 2.3rem;
    margin-bottom: 0;
    padding-bottom: 0;
    margin-top: 12px;
}}

h3 {{
    color: {HEADING} !important;
    font-size: 1.1rem;
    font-weight: 600;
    margin-top: 1.8rem;
    margin-bottom: 1rem;
    border-bottom: 2px solid {BORDER};
    padding-bottom: 0.5rem;
}}

.subtitle {{
    color: {TEXT};
    font-size: 1rem;
    margin-bottom: 2rem;
}}

/* ── Inputs ── */
.stTextInput input, .stNumberInput input {{
    border-radius: 6px !important;
    background-color: {INPUT_BG} !important;
    border: 1px solid {BORDER} !important;
    color: {INPUT_TXT} !important;
    font-size: 0.9rem !important;
}}

.stSelectbox div[data-baseweb="select"] > div {{
    border-radius: 6px !important;
    background-color: {INPUT_BG} !important;
    border: 1px solid {BORDER} !important;
    color: {INPUT_TXT} !important;
}}

/* ── Labels ── */
label, .stSelectbox label, .stTextInput label, .stNumberInput label, .stSlider label {{
    color: {LBL_CLR} !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.3px !important;
}}

/* ── Sliders ── */
.stSlider > div > div > div > div {{
    background-color: {ACCENT} !important;
}}

.stSlider > div > div > div > div > div {{
    background-color: #ffffff !important;
    border: 2.5px solid {ACCENT} !important;
    box-shadow: 0 2px 6px rgba(29,78,216,0.25) !important;
}}

/* ── Button ── */
.stButton > button {{
    background-color: {BTN_BG} !important;
    color: {BTN_TXT} !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    border: none !important;
    font-size: 1rem !important;
    box-shadow: 0 4px 10px rgba(29,78,216,0.3) !important;
    transition: all 0.2s ease !important;
    margin-top: 1.2rem !important;
}}

.stButton > button:hover {{
    background-color: {BTN_HOVER} !important;
    transform: translateY(-1px) !important;
    color: {BTN_TXT} !important;
}}

/* ── Result Card ── */
.result-card {{
    background-color: {SUB_CARD};
    border-radius: 12px;
    padding: 1.8rem 2rem;
    margin-top: 2rem;
    border: 1px solid {BORDER};
}}

.result-header {{
    font-size: 1.1rem;
    font-weight: 700;
    color: {HEADING};
    border-bottom: 1px solid {BORDER};
    padding-bottom: 0.6rem;
    margin-bottom: 1.2rem;
}}

.result-row {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-top: 1rem;
}}

.result-item {{
    display: flex;
    flex-direction: column;
}}

.result-label {{
    color: {TEXT};
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-top: 3px;
}}

.result-value {{
    color: {INPUT_TXT};
    font-size: 1.15rem;
    font-weight: 600;
}}

.status-approved {{
    color: {OK_CLR};
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -1px;
}}

.status-rejected {{
    color: {ERR_CLR};
    font-size: 2.5rem;
    font-weight: 800;
}}

.status-label {{
    color: {TEXT};
    font-size: 0.85rem;
    font-weight: 600;
    text-align: right;
    margin-top: 4px;
}}
</style>
"""

SLIDER_SOUND_JS = """
<script>
(function() {
    const parentDoc = window.parent.document;
    let audioCtx;

    function getCtx() {
        if (!audioCtx) audioCtx = new (window.parent.AudioContext || window.parent.webkitAudioContext)();
        if (audioCtx.state === 'suspended') audioCtx.resume();
        return audioCtx;
    }

    function playTick() {
        try {
            const ctx = getCtx();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(700, ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(950, ctx.currentTime + 0.04);
            
            gain.gain.setValueAtTime(0.09, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.04);
            
            osc.connect(gain);
            gain.connect(ctx.destination);
            
            osc.start();
            osc.stop(ctx.currentTime + 0.04);
        } catch(e) {}
    }

    let dragging = false;
    let lastTick = 0;

    function isSlider(el) {
        return el && (el.closest('[role="slider"]') || el.closest('[data-baseweb="slider"]') || el.closest('input[type="range"]'));
    }

    parentDoc.addEventListener('mousedown', e => {
        if(isSlider(e.target)) {
            dragging=true;
            playTick();
        }
    });

    parentDoc.addEventListener('mouseup', () => {
        dragging=false;
    });

    parentDoc.addEventListener('mousemove', e => {
        if(!dragging) return;
        const now = Date.now();
        if(now - lastTick > 40) {
            playTick();
            lastTick = now;
        }
    });

    parentDoc.addEventListener('keydown', e => {
        if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key) && isSlider(parentDoc.activeElement)) {
            playTick();
        }
    });
})();
</script>
"""

def run():
    st.markdown(custom_css, unsafe_allow_html=True)
    components.html(SLIDER_SOUND_JS, height=0)

    # ── Top bar: title + dark mode toggle ──
    col_logo, col_title, col_toggle = st.columns([1, 8, 2])
    
    with col_logo:
        st.markdown(f'''
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:5px;width:26px;margin-top:22px;">
                {"".join([f'<div style="width:11px;height:11px;background:{ACCENT};border-radius:50%;"></div>' for _ in range(6)])}
            </div>
        ''', unsafe_allow_html=True)
        
    with col_title:
        st.markdown(f"<h1>Loan Predictor</h1>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtitle'>Find out your loan eligibility in seconds</div>", unsafe_allow_html=True)
        
    with col_toggle:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button(f"{MODE_ICON} {MODE_LBL}", on_click=toggle_theme, key="theme_btn")

    # ── Personal Information ──
    st.markdown("<h3>👤 Personal Information</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        fn = st.text_input('Full Name', placeholder="e.g. Aditi Sharma")
        gen_display = ('Female', 'Male')
        gen = st.selectbox("Gender", range(len(gen_display)), format_func=lambda x: gen_display[x])
        mar_display = ('No', 'Yes')
        mar = st.selectbox("Marital Status", range(len(mar_display)), format_func=lambda x: mar_display[x])
        edu_display = ('Not Graduate', 'Graduate')
        edu = st.selectbox("Education", range(len(edu_display)), format_func=lambda x: edu_display[x])
        
    with c2:
        account_no = st.text_input('Account Number', placeholder="XXXX-XXXX-XXXX")
        dep_display = ('No', 'One', 'Two', 'More than Two')
        dep = st.selectbox("Dependents", range(len(dep_display)), format_func=lambda x: dep_display[x])
        emp_display = ('No', 'Yes')
        emp = st.selectbox("Self Employed", range(len(emp_display)), format_func=lambda x: emp_display[x])
        prop_display = ('Rural', 'Semi-Urban', 'Urban')
        prop = st.selectbox("Property Area", range(len(prop_display)), format_func=lambda x: prop_display[x])

    # ── Financial Summary ──
    st.markdown("<h3>💰 Financial Summary</h3>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    with c3:
        mon_income = st.slider("Applicant's Monthly Income (₹)", 0, 500000, 50000, step=5000)
        co_mon_income = st.slider("Co-Applicant's Monthly Income (₹)", 0, 500000, 0, step=5000)
        cred_opts = ('Between 300 to 500', 'Above 500')
        cred = st.selectbox("Credit Score", range(len(cred_opts)), format_func=lambda x: cred_opts[x])
        
    with c4:
        loan_amt = st.slider("Required Loan Amount (₹)", 0, 10000000, 200000, step=10000)
        
        # ── Loan Duration – full-width horizontal custom slider ──
        if "dur_months" not in st.session_state:
            st.session_state.dur_months = 12

        TRACK = ACCENT
        CARD_C = CARD
        BORDER_C= BORDER
        TXT_C = TEXT
        LBL_C = LBL_CLR
        cur_m = st.session_state.dur_months

        dur_slider_html = f"""
        <style>
            .dur-wrap {{
                background:{CARD_C}; 
                border:1.5px solid {BORDER_C}; 
                border-radius:16px; 
                padding:28px 32px 20px; 
                box-shadow:0 2px 14px rgba(0,0,0,0.06); 
                margin-top:8px;
                font-family:'Inter',sans-serif;
            }}
            .dur-title {{
                font-size:0.82rem; font-weight:600; letter-spacing:0.5px; text-transform:uppercase;
                color:{LBL_C}; margin-bottom:22px; display:flex; justify-content:space-between; align-items:center;
            }}
            .dur-badge {{ background:{TRACK}; color:#fff; font-size:0.85rem; font-weight:700; padding:3px 14px; border-radius:20px; }}
            .dur-track-wrap {{ position:relative; padding-top:30px; padding-bottom:6px; }}
            
            /* bubble above thumb */
            #dur-bubble {{
                position:absolute; top:0; transform:translateX(-50%); background:{TRACK}; color:#fff;
                font-size:0.78rem; font-weight:700; padding:3px 9px; border-radius:8px; white-space:nowrap;
                pointer-events:none; transition:left 0.08s;
            }}
            #dur-bubble::after {{
                content:''; position:absolute; top:100%;left:50%; transform:translateX(-50%);
                border:5px solid transparent; border-top-color:{TRACK};
            }}

            /* range input */
            #dur-range {{
                -webkit-appearance:none; appearance:none; width:100%; height:6px; border-radius:6px;
                background:linear-gradient(to right, {TRACK} var(--pct), {BORDER_C} var(--pct));
                outline:none; cursor:pointer;
            }}
            #dur-range::-webkit-slider-thumb {{
                -webkit-appearance:none; width:22px;height:22px; border-radius:50%; background:#fff;
                border:3px solid {TRACK}; box-shadow:0 2px 8px rgba(29,78,216,0.25); cursor:pointer;
                display:flex;align-items:center;justify-content:center;
            }}
            #dur-range::-moz-range-thumb {{
                width:22px;height:22px; border-radius:50%; background:#fff;
                border:3px solid {TRACK}; box-shadow:0 2px 8px rgba(29,78,216,0.25); cursor:pointer;
            }}
            .dur-labels {{
                display:flex; justify-content:space-between; margin-top:8px;
                font-size:0.75rem; color:{TXT_C}; font-weight:500;
            }}
        </style>

        <div class="dur-wrap">
            <div class="dur-title">
                <span>⏳ Loan Duration</span>
                <span class="dur-badge" id="dur-badge-top">{cur_m} Months</span>
            </div>
            <div class="dur-track-wrap">
                <div id="dur-bubble">{cur_m}m</div>
                <input id="dur-range" type="range" min="1" max="60" step="1" value="{cur_m}" />
            </div>
            <div class="dur-labels">
                <span>1 Month</span>
                <span>1 Year</span>
                <span>2 Years</span>
                <span>3 Years</span>
                <span>4 Years</span>
                <span>5 Years</span>
            </div>
        </div>

        <script>
            (function(){{
                const slider = document.getElementById('dur-range');
                const bubble = document.getElementById('dur-bubble');
                const badge = document.getElementById('dur-badge-top');

                // Audio
                let audioCtx;
                function getCtx(){{
                    if(!audioCtx) audioCtx = new (window.AudioContext||window.webkitAudioContext)();
                    if(audioCtx.state==='suspended') audioCtx.resume();
                    return audioCtx;
                }}
                function playTick(){{
                    try{{
                        const ctx=getCtx();
                        const osc=ctx.createOscillator(), g=ctx.createGain();
                        osc.type='triangle'; 
                        osc.frequency.setValueAtTime(700,ctx.currentTime);
                        osc.frequency.exponentialRampToValueAtTime(1000,ctx.currentTime+0.04);
                        g.gain.setValueAtTime(0.09,ctx.currentTime);
                        g.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+0.04);
                        osc.connect(g); g.connect(ctx.destination);
                        osc.start(); osc.stop(ctx.currentTime+0.04);
                    }}catch(e){{}}
                }}

                function updateUI(){{
                    const v = parseInt(slider.value);
                    const min = parseInt(slider.min);
                    const max = parseInt(slider.max);
                    const pct = ((v-min)/(max-min))*100;
                    
                    // gradient fill
                    slider.style.setProperty('--pct', pct+'%');
                    
                    // bubble position
                    const trackW = slider.offsetWidth;
                    const thumbR = 11;
                    const left = thumbR + (pct/100)*(trackW - 2*thumbR);
                    bubble.style.left = left+'px';

                    const label = v===1 ? '1 Month' : v<12 ? v+' Months' : v===12 ? '1 Year' : (v/12).toFixed(1).replace('.0','')+' Yrs';
                    bubble.textContent = v+'m';
                    badge.textContent = label;
                }}

                let lastV = slider.value;
                slider.addEventListener('input', ()=>{{
                    const v=parseInt(slider.value);
                    if(v!==parseInt(lastV)){{
                        playTick();
                        lastV=v;
                    }}
                    updateUI();
                }});

                slider.addEventListener('mousedown', ()=>playTick());
                slider.addEventListener('keydown', e=>{{
                    if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)) playTick();
                }});

                updateUI();
            }})();
        </script>
        """
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        components.html(dur_slider_html, height=180, scrolling=False)
        dur_months = st.session_state.dur_months

    # ── Submit ──
    if st.button("🔍 Check Eligibility"):
        duration_days = dur_months * 30
        features = [[gen, mar, dep, edu, emp, mon_income, co_mon_income, loan_amt/1000.0, duration_days, cred, prop]]
        model = pickle.load(open('model1.pkl', 'rb'))
        ans = model.predict(features)[0]

        loan_fmt = f"₹{loan_amt:,}"
        income_fmt = f"₹{mon_income:,}"
        dur_str = f"{dur_months} Month{'s' if dur_months != 1 else ''}"

        if ans == 1:
            status_html = f'<div class="status-approved">Approved ✓</div>'
        else:
            status_html = f'<div class="status-rejected">Rejected ✗</div>'

        st.markdown(f"""
            <div class="result-card">
                <div class="result-header">Your Application Results</div>
                <div style="color:{TEXT};font-size:0.8rem;">Summary based on entered details</div>
                <div class="result-row">
                    <div style="display:flex;gap:2.5rem;">
                        <div class="result-item"><div class="result-value">{{loan_fmt}}</div><div class="result-label">Loan Amount</div></div>
                        <div class="result-item"><div class="result-value">{{dur_str}}</div><div class="result-label">Duration</div></div>
                        <div class="result-item"><div class="result-value">{{income_fmt}}</div><div class="result-label">Monthly Income</div></div>
                    </div>
                    <div style="text-align:right;">
                        {{status_html}}
                        <div class="status-label">Status</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

if __name__ == '__main__':
    run()
