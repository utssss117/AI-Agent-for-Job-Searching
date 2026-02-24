import streamlit as st
import json
from resume_parser import extract_text_from_pdf
from llm_analyzer import LLMAnalyzer
from live_job_fetcher import LiveJobFetcher
from cover_letter_gen import CoverLetterGenerator

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("📄 AI Resume Analyzer")
st.markdown("Upload a PDF resume to extract structured data using Groq Llama 3.1.")

# Sidebar for API Key and Live Search
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Groq API Key", type="password")
    if not api_key:
        st.info("Please provide a Groq API Key or set GROQ_API_KEY environment variable.")
    
    st.divider()
    st.header("Live Job Search")
    job_query = st.text_input("Job Title/Keywords", placeholder="e.g. Python Developer")
    job_location = st.text_input("Location", placeholder="e.g. London")
    job_country = st.selectbox("Country", ["United Kingdom", "India", "United States", "Canada", "Germany", "France", "Australia", "United Arab Emirates"])
    fetch_live = st.button("Fetch Live Jobs")

# Initialize Helper Classes
live_fetcher = LiveJobFetcher()
cover_letter_gen = CoverLetterGenerator(api_key=api_key if api_key else None)

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
    st.subheader("Analyze Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF resume", type="pdf")
    
    if uploaded_file is not None:
        try:
            # Initialize LLM Analyzer
            analyzer = LLMAnalyzer(api_key=api_key if api_key else None)
            
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
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Extracted Data Summary")
                st.write(f"**Experience Years:** {result.get('experience_years', 'N/A')}")
                st.write("**Domain Expertise:**", ", ".join(result.get("domain_expertise", [])))
                st.write("**Strengths:**", ", ".join(result.get("strengths", [])))
                
                st.write("**Skills:**")
                st.write(", ".join(result.get("skills", [])))
                
                st.write("**Education:**")
                for edu in result.get("education", []):
                    st.write(f"- {edu.get('degree')} @ {edu.get('institution')} ({edu.get('year')})")

            with col2:
                st.subheader("Structured JSON Output")
                st.json(result)
                
                # Download button
                json_str = json.dumps(result, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_str,
                    file_name="resume_analysis.json",
                    mime="application/json"
                )
            
            # --- Job Matching Section ---
            st.divider()
            st.header("🎯 AI Job Match Analysis")
            
            from matching_engine import analyze_job_matches
            
            with st.spinner("Analyzing skill gaps and matching jobs..."):
                job_matches = analyze_job_matches(result, resume_text)
            
            if not job_matches:
                st.warning("No matching jobs found above the threshold. Try fetching more live jobs!")
            else:
                for match in job_matches:
                    score = match['match_percentage']
                    color = "green" if score > 70 else "orange" if score > 40 else "red"
                    
                    with st.expander(f"**{match['job_title']}** at {match['company']} (Match: :{color}[{score}%])"):
                        st.write(f"📍 **Location:** {match['location']}")
                        
                        m_col1, m_col2 = st.columns(2)
                        with m_col1:
                            st.write("✅ **Matched Skills**")
                            matched = [s for s in match['matched_skills'] if s]
                            st.write(", ".join(matched) if matched else "*None*")
                                
                        with m_col2:
                            st.write("⚠️ **Missing Skills**")
                            missing = [s for s in match['missing_skills'] if s]
                            st.write(", ".join(missing) if missing else "*Perfect match!*")
                        
                        st.divider()
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
    
    from supabase_client import get_supabase_client
    try:
        supabase = get_supabase_client()
        response = supabase.table("jobs").select("*").execute()
        jobs = response.data
        
        if not jobs:
            st.info("Your database is empty. Use the sidebar to fetch some live jobs!")
        else:
            st.success(f"Currently tracking {len(jobs)} jobs in your local database.")
            for job in jobs:
                with st.expander(f"**{job['title']}** at {job['company']} ({job['location']})"):
                    st.write(f"**📝 Description summary:** {job['description'][:500]}...")
                    if job.get('required_skills'):
                        st.write(f"**🛠 Skills:** {', '.join(job['required_skills'])}")
                    st.write(f"**💼 Experience Req:** {job.get('experience_required', 'N/A')}")
    except Exception as e:
        st.error(f"Error loading jobs from Supabase: {e}")
