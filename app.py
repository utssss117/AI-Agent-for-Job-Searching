import streamlit as st
import json
from resume_parser import extract_text_from_pdf
from llm_analyzer import LLMAnalyzer
from live_job_fetcher import LiveJobFetcher
from cover_letter_gen import CoverLetterGenerator
from style_utils import inject_custom_css, job_card_html
from supabase_client import get_supabase_client

st.set_page_config(page_title="SkyNet AI • Resume Analysis", page_icon="🚀", layout="wide")
inject_custom_css()

st.title("📄 Job Search Agent")
st.markdown("Upload your resume to find matching jobs and get insights.")

# Sidebar for Live Search
with st.sidebar:
    st.header("Live Job Search")
    job_query = st.text_input("Job Title/Keywords", placeholder="e.g. Python Developer")
    job_location = st.text_input("Location", placeholder="e.g. London")
    job_country = st.selectbox("Country", ["United Kingdom", "India", "United States", "Canada", "Germany", "France", "Australia", "United Arab Emirates"])
    fetch_live = st.button("Fetch Live Jobs")

# Initialize Helper Classes
live_fetcher = LiveJobFetcher()
cover_letter_gen = CoverLetterGenerator(api_key=None)

# Global Handle for Live Fetch (Works even without resume)
if fetch_live:
    if not job_query:
        st.sidebar.error("Enter a job title to search.")
    else:
        with st.sidebar:
            with st.spinner("Fetching live jobs..."):
                fetched = live_fetcher.fetch_live_jobs(
                    query=job_query, 
                    location=job_location or "", 
                    country=job_country,
                    results=10
                )
                if fetched:
                    st.success(f"Fetched {len(fetched)} live jobs for {job_country} and updated database!")
                    st.rerun() # Refresh to show new jobs in Database Explorer
                else:
                    st.warning(f"No jobs found in {job_country} or API error.")

# Main UI Tabs
tab1, tab2 = st.tabs(["🔍 Resume Intelligence", "📁 Job Database Explorer"])

with tab1:
    st.subheader("Your Resume Details")
    uploaded_file = st.file_uploader("Choose a PDF resume", type="pdf")
    
    if uploaded_file is not None:
        try:
            # Initialize LLM Analyzer
            analyzer = LLMAnalyzer(api_key=None)
            
            # Processing Phase
            with st.status("Processing resume...", expanded=True) as status:
                st.write("Extracting text from PDF...")
                resume_text = extract_text_from_pdf(uploaded_file.read())
                
                if not resume_text:
                    st.error("Could not extract text from the PDF. Please try another file.")
                    status.update(label="Extraction failed", state="error")
                    st.stop()
                
                st.write("Analyzing with Groq LLM...")
                result = analyzer.analyze_resume(resume_text)
                
                if "error" in result:
                    st.error(f"Analysis failed: {result['error']}")
                    status.update(label="Analysis failed", state="error")
                    st.stop()
                
                status.update(label="Analysis complete!", state="complete")

            # Results Display Phase
            st.divider()
            from style_utils import resume_summary_html
            st.markdown(resume_summary_html(result), unsafe_allow_html=True)
            
            # Download button
            json_str = json.dumps(result, indent=2)
            st.download_button(
                label="📥 Download Structured Analysis",
                data=json_str,
                file_name="resume_analysis.json",
                mime="application/json"
            )
            
            # --- Job Matching Section ---
            st.divider()
            st.header("🎯 Top Matched Jobs")
            
            from matching_engine import analyze_job_matches
            
            with st.spinner("Analyzing skill gaps and matching jobs..."):
                job_matches = analyze_job_matches(result, resume_text)
            
            if not job_matches:
                st.warning("No matching jobs found above the threshold. Try fetching more live jobs!")
            else:
                for match in job_matches:
                    score = match['match_percentage']
                    # Premium Job Card
                    st.markdown(job_card_html(
                        match['job_title'], 
                        match['company'], 
                        match['location'], 
                        score, 
                        match['matched_skills'], 
                        match['missing_skills']
                    ), unsafe_allow_html=True)
                    
                    with st.expander("📊 View Detailed ATS Analysis & Strategy"):
                        st.subheader("📊 ATS Evaluation")
                        ats = match.get('ats_analysis', {})
                        
                        a_col1, a_col2, a_col3 = st.columns(3)
                        a_col1.metric("Overall ATS Score", f"{ats.get('overall_ats_score', 0)}%")
                        a_col2.metric("Keyword Match", f"{ats.get('keyword_score', 0)}%")
                        a_col3.metric("Skills Alignment", f"{ats.get('skills_score', 0)}%")
                        
                        st.write("**Score Breakdown**")
                        b_col1, b_col2 = st.columns(2)
                        with b_col1:
                            st.write(f"Experience: {ats.get('experience_score', 0)}%")
                            st.progress(ats.get('experience_score', 0) / 100)
                            st.write(f"Structure: {ats.get('structure_score', 0)}%")
                            st.progress(ats.get('structure_score', 0) / 100)
                        with b_col2:
                            st.write(f"Impact Metrics: {ats.get('impact_score', 0)}%")
                            st.progress(ats.get('impact_score', 0) / 100)
                            st.write(f"Keyword Score: {ats.get('keyword_score', 0)}%")
                            st.progress(ats.get('keyword_score', 0) / 100)

                        if ats.get('improvement_suggestions'):
                            st.write("**🚀 How to Improve:**")
                            for suggestion in ats['improvement_suggestions']:
                                st.write(f"- {suggestion}")

                        st.divider()
                        st.write("**AI Recommendation:**")
                        st.write(match.get('recommendation_reason', 'Analysis pending...'))
                        
                        st.write("**Job Strategy Tip:**")
                        if match['missing_skills']:
                            st.info(f"To increase your chances, highlight or acquire: {', '.join(match['missing_skills'][:3])}")
                        else:
                            st.success("Your profile is a strong match for this role!")
                            
                        # Cover Letter Generation
                        st.divider()
                        if st.button(f"✍️ Draft Cover Letter for {match['company']}", key=f"btn_{match['job_title']}_{match['company']}"):
                            with st.spinner("Drafting your personalized cover letter..."):
                                letter = cover_letter_gen.generate_cover_letter(result, match)
                                st.text_area("Generated Cover Letter (Copy & Edit)", value=letter, height=300)
                                st.download_button(
                                    label="Download Cover Letter (TXT)",
                                    data=letter,
                                    file_name=f"Cover_Letter_{match['company']}.txt",
                                    mime="text/plain",
                                    key=f"dl_{match['job_title']}_{match['company']}"
                                )
                            
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

with tab2:
    st.header("📁 Job Database Explorer")
    st.write("View all jobs currently stored in your local matching engine.")
    
    from style_utils import database_job_card_html
    try:
        supabase = get_supabase_client()
        response = supabase.table("jobs").select("*").execute()
        jobs = response.data
        
        if not jobs:
            st.info("Your database is empty. Use the sidebar to fetch some live jobs!")
        else:
            st.success(f"Currently tracking {len(jobs)} jobs in your local database.")
            for job in jobs:
                st.markdown(database_job_card_html(
                    job['title'], 
                    job['company'], 
                    job['location'], 
                    job['description'], 
                    job.get('required_skills', [])
                ), unsafe_allow_html=True)
                with st.expander("🔍 View Full Description"):
                    st.write(job['description'])
    except Exception as e:
        st.error(f"Error loading jobs from Supabase: {e}")
