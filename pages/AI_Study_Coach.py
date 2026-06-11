import streamlit as st
from modules.auth import require_login
from modules.ai_coach import get_today_checkin, save_checkin, generate_ai_insights, generate_regenerated_plan

st.set_page_config(page_title="AI Study Coach", page_icon="🤖", layout="wide")

# Enforce authentication
require_login()

st.title("🤖 AI Study Coach")
st.markdown("Your personal AI mentor for GATE preparation. Analyze progress, identify weak areas, and receive personalized recommendations.")

user_id = st.session_state.user_id

# --- ACCOUNTABILITY PARTNER ---
st.subheader("Daily Check-In")
current_checkin = get_today_checkin(user_id)

if current_checkin:
    st.success(f"You've already checked in today! Status: **{current_checkin}**")
else:
    with st.container(border=True):
        st.write("**Accountability Partner**")
        st.write("Did you complete today's study goals?")
        
        c_col1, c_col2, c_col3 = st.columns(3)
        if c_col1.button("✅ Yes, absolutely!"):
            save_checkin(user_id, "Yes")
            st.rerun()
        if c_col2.button("🟨 Partially"):
            save_checkin(user_id, "Partially")
            st.rerun()
        if c_col3.button("❌ No, I missed it"):
            save_checkin(user_id, "No")
            st.rerun()

st.markdown("---")

# --- AI INSIGHTS ---
st.subheader("Coach Insights")
with st.spinner("Analyzing your progress data..."):
    insights = generate_ai_insights(user_id)
    
if insights["type"] == "ai_raw":
    # Render the pure Gemini Markdown output
    st.markdown(insights["content"])
else:
    # Render the Rule-Based fallback cleanly
    data = insights["content"]
    
    st.info(f"💡 **Coach Motivation:** {data['motivation']}")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("📈 Progress Summary & Recommendations", expanded=True):
            st.write(data['summary'])
            st.write("**Recommendations:**")
            for rec in data['recommendations']:
                st.write(f"- {rec}")
                
        with st.expander("💪 Strong Subjects", expanded=True):
            for s in data['strong']:
                st.write(f"- {s}")
                
    with col2:
        with st.expander("⚠️ Weak Subjects", expanded=True):
            for w in data['weak']:
                st.write(f"- {w}")
                
        with st.expander("🔄 Missed & Revision Needed", expanded=True):
            st.write("**Pending / Missed:**")
            for m in data['missed']:
                st.write(f"- {m}")
            st.write("**Needs Revision:**")
            for r in data['revision']:
                st.write(f"- {r}")

st.markdown("---")

# --- ADAPTIVE PLANNING ---
st.subheader("Adaptive Plan Regeneration")
st.write("Falling behind or want to increase the intensity? The Coach can automatically rebuild your monthly roadmap based on the time remaining.")

if st.button("Regenerate Study Plan", type="primary"):
    with st.spinner("Rebuilding your personalized study plan..."):
        resp = generate_regenerated_plan(user_id)
        if resp["success"]:
            st.success("Your plan has been regenerated! Go to the **Study Plan** page to view it.")
            st.balloons()
        else:
            st.error(resp["message"])
