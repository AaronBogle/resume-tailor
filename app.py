import streamlit as st
import requests

# Set Hugging Face Zephyr model URL
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {st.secrets['hf_api_key']}"} if 'hf_api_key' in st.secrets else {}

prompt_template = """
You are a professional resume optimization assistant.

Given a base resume and a job description, your job is to:
1. Retool the resume to better align with the job — by rewriting or editing bullet points and/or the professional summary.
2. Maintain the factual integrity of the resume. Do not invent experience or claim skills not present.
3. Emphasize transferable skills and reframe existing experience to match the language and focus of the job description.
4. List any missing but relevant keywords from the job description that are not clearly represented in the resume.

Return your response in the following format:

🔧 Tailored Summary (if applicable):
[Rewritten professional summary, if one is detected or included]

✅ Updated Bullet Points:
- [Improved or reframed bullet 1]
- [Improved or reframed bullet 2]
...

❗ Missing Keywords to Consider Adding:
- [keyword 1], [keyword 2], ...

Resume:
{resume}

Job Description:
{jd}
"""

st.title("🧵 AI Resume Tailor")
st.markdown("Improve your resume to better match a job description — without exaggerating or fabricating.")

resume_text = st.text_area("📄 Paste your base resume here", height=300)
job_description = st.text_area("💼 Paste the job description here", height=300)

if st.button("Tailor My Resume"):
    if not headers:
        st.error("Hugging Face API key not found. Please add it to Streamlit secrets.")
    elif resume_text and job_description:
        with st.spinner("Tailoring your resume..."):
            full_prompt = prompt_template.format(resume=resume_text, jd=job_description)
            response = requests.post(API_URL, headers=headers, json={
                "inputs": full_prompt,
                "parameters": {
                    "max_new_tokens": 500,
                    "return_full_text": False
                }
            })
            if response.status_code == 200:
                output = response.json()
                if isinstance(output, list) and "generated_text" in output[0]:
                    st.markdown("### ✨ Tailored Resume Suggestions")
                    st.markdown(output[0]["generated_text"])
                else:
                    st.error("Unexpected response structure from model.")
            else:
                st.error(f"Error from Hugging Face API: {response.status_code}\n{response.text}")
    else:
        st.warning("Please provide both resume and job description.")
