import streamlit as st
import os
from openai import OpenAI

# Initialize OpenAI client using environment variable
client = OpenAI()

def generate_initial_bullets(job_description):
    prompt = f"Convert the following job responsibilities into 3-5 resume bullet points using professional resume language with action verbs:\n\n{job_description}\n\nBullet Points:"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )
    return response.choices[0].message.content.strip().split("\n")

def enhance_bullets_with_impact(bullets):
    prompt = f"Enhance the following resume bullet points to show clear impact, outcomes, or metrics:\n\n{chr(10).join(bullets)}\n\nEnhanced Bullet Points:"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )
    return response.choices[0].message.content.strip().split("\n")

st.title("Resume Bullet Point Generator")

step = st.session_state.get("step", 1)

if step == 1:
    st.subheader("Step 1: Describe Your Job")
    job_description = st.text_area("What do you handle at your job?", height=200)
    if st.button("Generate Bullet Points") and job_description:
        bullets = generate_initial_bullets(job_description)
        st.session_state["bullets"] = bullets
        st.session_state["step"] = 2
        st.experimental_rerun()

elif step == 2:
    st.subheader("Step 2: Initial Resume Bullet Points")
    bullets = st.session_state["bullets"]
    for bullet in bullets:
        st.markdown(f"- {bullet}")

    if st.button("Looks Good. Add Impact"):
        enhanced_bullets = enhance_bullets_with_impact(bullets)
        st.session_state["enhanced_bullets"] = enhanced_bullets
        st.session_state["step"] = 3
        st.experimental_rerun()
    elif st.button("Go Back and Edit Input"):
        st.session_state["step"] = 1
        st.experimental_rerun()

elif step == 3:
    st.subheader("Step 3: Enhanced Resume Bullet Points with Impact")
    enhanced_bullets = st.session_state["enhanced_bullets"]
    for bullet in enhanced_bullets:
        st.markdown(f"- {bullet}")

    st.success("Done! You can copy and use these in your resume.")
    if st.button("Start Over"):
        st.session_state.clear()
        st.experimental_rerun()
