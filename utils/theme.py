import streamlit as st

def apply_theme():
    """Inject custom CSS for the modern Professional Blue + White theme."""
    st.markdown("""
        <style>
        /* Base Streamlit overrides */
        .stApp {
            background-color: #F8FAFC;
        }
        
        /* Modern Typography and Headings */
        h1, h2, h3 {
            color: #0F172A;
            font-family: 'Inter', 'Segoe UI', sans-serif;
            font-weight: 700;
        }
        
        /* Modern Buttons */
        div.stButton > button:first-child {
            background-color: #2563EB;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.2s ease-in-out;
        }
        div.stButton > button:first-child:hover {
            background-color: #1D4ED8;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.4);
            color: white;
        }
        
        /* Form Submit Buttons */
        div[data-testid="stFormSubmitButton"] > button {
            background-color: #2563EB;
            color: white;
            width: 100%;
        }
        
        /* Navigation Sidebar - Ensure active state is blue */
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background-color: #2563EB !important;
            color: white !important;
            border-radius: 8px;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] span {
            color: white !important;
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            color: #2563EB;
            font-weight: 800;
            font-size: 2rem;
        }
        [data-testid="stMetricLabel"] {
            color: #64748B;
            font-weight: 600;
            font-size: 1rem;
        }
        
        /* Custom Card Class (used with st.markdown if needed) */
        .modern-card {
            background-color: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            border: 1px solid #E2E8F0;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
