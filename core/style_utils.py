import streamlit as st
import textwrap

def inject_custom_css():
    custom_css = """
    <style>
        /* Import Premium Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Outfit:wght@300;500;700&display=swap');

        :root {
            --primary-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --card-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        }

        /* Global Styles */
        html, body, [class*="st-"] {
            font-family: 'Outfit', sans-serif;
        }

        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            font-weight: 800 !important;
            letter-spacing: -0.02em;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Main Container Padding */
        .main > div {
            padding-top: 2rem;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0f172a;
            border-right: 1px solid var(--glass-border);
        }

        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2 {
            color: white !important;
            -webkit-text-fill-color: white !important;
        }

        /* Button Styling */
        .stButton > button {
            border-radius: 12px;
            padding: 0.6rem 1.5rem;
            background: var(--primary-gradient);
            color: white !important;
            border: none;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
            width: 100%;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
            opacity: 0.9;
        }

        /* Custom Card Component */
        .job-card {
            background: var(--glass-bg);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: var(--card-shadow);
        }

        .job-card:hover {
            transform: scale(1.02);
            border-color: #a855f7;
        }

        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 0.5rem;
            background: rgba(168, 85, 247, 0.1);
            color: #a855f7;
            border: 1px solid rgba(168, 85, 247, 0.2);
        }

        /* Metrics Styling */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: #6366f1 !important;
        }

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }

        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            border-radius: 4px 4px 0px 0px;
            border-bottom: 2px solid transparent;
            font-weight: 600;
        }

        .stTabs [aria-selected="true"] {
            border-bottom: 2px solid #a855f7 !important;
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .stApp {
            animation: fadeIn 0.8s ease-out;
        }

        /* Hide Streamlit Menu */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def job_card_html(title, company, location, match_score, matched_skills, missing_skills):
    color = "#10b981" if match_score > 70 else "#f59e0b" if match_score > 40 else "#ef4444"
    
    matched_html = "".join([f'<span class="badge" style="color: #10b981; background: rgba(16, 185, 129, 0.1); border-color: rgba(16, 185, 129, 0.2);">{s}</span>' for s in matched_skills[:5]])
    missing_html = "".join([f'<span class="badge" style="color: #ef4444; background: rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.2);">{s}</span>' for s in missing_skills[:5]])

    return textwrap.dedent(f"""
    <div class="job-card">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <h3 style="margin: 0; background: none; -webkit-text-fill-color: inherit; color: inherit;">{title}</h3>
                <p style="margin: 0.2rem 0; opacity: 0.8; font-weight: 500;">{company} • {location}</p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 1.5rem; font-weight: 800; color: {color};">{match_score}%</div>
                <div style="font-size: 0.7rem; font-weight: 600; opacity: 0.6; text-transform: uppercase;">Match Score</div>
            </div>
        </div>
        <div style="margin-top: 1rem;">
            <p style="margin-bottom: 0.5rem; font-size: 0.8rem; font-weight: 700; opacity: 0.7;">TOP MATCHED SKILLS</p>
            <div>{matched_html}</div>
        </div>
        <div style="margin-top: 1rem;">
            <p style="margin-bottom: 0.5rem; font-size: 0.8rem; font-weight: 700; opacity: 0.7;">SKILL GAPS</p>
            <div>{missing_html if missing_skills else '<span class="badge">Perfect Match!</span>'}</div>
        </div>
    </div>
    """)

def database_job_card_html(title, company, location, description, skills):
    skills_html = "".join([f'<span class="badge">{s}</span>' for s in skills[:8]]) if skills else ""
    return textwrap.dedent(f"""
    <div class="job-card">
        <h3 style="margin: 0; background: none; -webkit-text-fill-color: inherit; color: inherit;">{title}</h3>
        <p style="margin: 0.2rem 0; opacity: 0.8; font-weight: 500;">{company} • {location}</p>
        <p style="font-size: 0.85rem; margin: 1rem 0; opacity: 0.9; line-height: 1.5;">{description[:300]}...</p>
        <div style="margin-top: 0.5rem;">{skills_html}</div>
    </div>
    """)
def resume_summary_html(result):
    skills = result.get("skills", [])
    all_skills_html = "".join([f'<span class="badge" style="background: rgba(0, 0, 0, 0.05); color: #444; border: 1px solid #ccc;">{s}</span>' for s in skills])
    
    experience = f"{result.get('experience_years', 0)} Years"
    
    projects_html = "".join([
        f'<div style="margin-bottom: 0.6rem; font-size: 0.9rem;"><strong>{p.get("title")}</strong><br><span style="opacity: 0.8;">{p.get("description")}</span></div>' 
        for p in result.get("projects", [])
    ])
    
    education_html = "".join([
        f'<div style="margin-bottom: 0.5rem; font-size: 0.9rem;">🎓 <strong>{e.get("degree")}</strong><br><span style="opacity: 0.8;">{e.get("institution")} ({e.get("year")})</span></div>' 
        for e in result.get("education", [])
    ])

    return textwrap.dedent(f"""
    <div style="background: white; color: #333; border: 1px solid #ddd; border-top: 5px solid #6366f1; border-radius: 12px; padding: 2rem; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
        <h2 style="margin-top: 0; margin-bottom: 1.5rem; color: #333; -webkit-text-fill-color: #333; letter-spacing: 0;">Your Profile Summary</h2>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
            <div>
                <p style="margin-bottom: 0.5rem; font-size: 1rem;"><strong>Experience:</strong> {experience}</p>
                <p style="margin-bottom: 1.5rem; font-size: 1rem;"><strong>Focus Area:</strong> {", ".join(result.get("domain_expertise", []))}</p>
                
                <h3 style="font-size: 0.9rem; margin-bottom: 0.6rem; color: #666; -webkit-text-fill-color: #666; text-transform: uppercase;">Top Strengths</h3>
                <p style="font-size: 0.95rem; line-height: 1.5;">{ " • ".join(result.get("strengths", [])) }</p>
                
                <h3 style="font-size: 0.9rem; margin-top: 1.5rem; margin-bottom: 0.6rem; color: #666; -webkit-text-fill-color: #666; text-transform: uppercase;">Technical Skills</h3>
                <div style="display: flex; flex-wrap: wrap; gap: 0.4rem;">{all_skills_html}</div>
            </div>
            
            <div>
                <h3 style="font-size: 0.9rem; margin-bottom: 0.8rem; color: #666; -webkit-text-fill-color: #666; text-transform: uppercase;">Key Projects</h3>
                <div style="max-height: 250px; overflow-y: auto;">{projects_html if projects_html else "No projects listed"}</div>
                
                <h3 style="font-size: 0.9rem; margin-top: 1.5rem; margin-bottom: 0.8rem; color: #666; -webkit-text-fill-color: #666; text-transform: uppercase;">Education</h3>
                <div>{education_html if education_html else "No education listed"}</div>
            </div>
        </div>
    </div>
    """)
