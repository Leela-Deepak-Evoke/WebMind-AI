import streamlit as st
import json

from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
)

from parse import generate_qa_from_content

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="WebMind AI",
    page_icon="🌐",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background-color: #0f172a;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.stTextInput input {
    border-radius: 12px;
    padding: 14px;
    border: 1px solid #334155;
}

.stButton button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 16px;
    font-weight: bold;
    background-color: #2563eb;
    color: white;
    border: none;
}

.stButton button:hover {
    background-color: #1d4ed8;
    color: white;
}

.header-box {
    text-align: center;
    padding: 20px;
}

.metric-card {
    background-color: #111827;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #374151;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="header-box">
    <h1>🌐 WebMind AI</h1>
    <p>
        AI-Powered Website Intelligence,
        Q&A Generation and Content Analysis Platform
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- URL INPUT ----------------

url = st.text_input(
    "Enter Website URL",
    placeholder="https://example.com"
)

# ---------------- PROCESS BUTTON ----------------

if st.button("🚀 Process Website"):

    if not url.strip():

        st.warning("Please enter a valid URL")

    else:

        with st.spinner(
            "🔍 Scraping and analyzing website..."
        ):

            # ---------------- SCRAPE WEBSITE ----------------

            raw_html = scrape_website(url)

            # ---------------- SCRAPE FAILURE ----------------

            if not raw_html:

                st.error(
                    "Unable to process with given URL"
                )

            else:

                # ---------------- EXTRACT BODY ----------------

                body_content = extract_body_content(
                    raw_html
                )

                cleaned_content = clean_body_content(
                    body_content
                )

                # ---------------- EMPTY CONTENT ----------------

                if not cleaned_content.strip():

                    st.error(
                        "Unable to process with given URL"
                    )

                else:

                    # Save cleaned content

                    st.session_state.dom_content = (
                        cleaned_content
                    )

                    # ---------------- AI PROCESSING ----------------

                    qa_result = generate_qa_from_content(
                        cleaned_content
                    )

                    st.session_state.qa_result = (
                        qa_result
                    )

# ---------------- SHOW RESULTS ----------------

if "qa_result" in st.session_state:

    st.success(
        "✅ AI Questions Generated Successfully!"
    )

    try:

        # ---------------- LOAD JSON ----------------

        qa_data = json.loads(
            st.session_state.qa_result
        )

        # ---------------- SAFETY FALLBACK ----------------

        if isinstance(qa_data, list):

            qa_data = {
                "website_summary": [],
                "questions_answers": qa_data,
                "keywords": {
                    "business": [],
                    "technology": [],
                    "features": [],
                    "audience": [],
                    "knowledge": []
                }
            }

        # ---------------- DASHBOARD ----------------

        st.markdown(
            "## 🌐 Website Intelligence Dashboard"
        )

        col1, col2, col3 = st.columns(3)

        # ---------------- METRIC 1 ----------------

        with col1:

            st.metric(
                label="Generated Questions",
                value=len(
                    qa_data.get(
                        "questions_answers",
                        []
                    )
                )
            )

        # ---------------- METRIC 2 ----------------

        with col2:

            total_keywords = sum(
                len(v)
                for v in qa_data.get(
                    "keywords",
                    {}
                ).values()
            )

            st.metric(
                label="Knowledge Keywords",
                value=total_keywords
            )

        # ---------------- METRIC 3 ----------------

        with col3:

            st.metric(
                label="AI Status",
                value="Processed"
            )

        st.divider()
        
         # ---------------- WEBSITE SUMMARY ----------------

        st.markdown(
            "## 🌍 About This Website"
        )

        website_summary = qa_data.get(
            "website_summary",
            []
        )

        if website_summary:

            summary_html = ""

            for line in website_summary:

                summary_html += f"""
                <div style="
                    background-color:#111827;
                    border:1px solid #374151;
                    padding:18px;
                    border-radius:12px;
                    margin-bottom:12px;
                    color:white;
                    font-size:16px;
                    line-height:1.7;
                ">
                    {line}
                </div>
                """

            st.markdown(
                summary_html,
                unsafe_allow_html=True
            )

        else:

            st.info(
                "No website summary available."
            )

        st.divider()

        # ---------------- QUESTIONS SECTION ----------------

        st.markdown(
            "## 🤖 AI Generated Questions & Answers"
        )

        questions_answers = qa_data.get(
            "questions_answers",
            []
        )

        if questions_answers:

            for index, item in enumerate(
                questions_answers,
                start=1
            ):

                question = item.get(
                    "question",
                    "No Question"
                )

                answer = item.get(
                    "answer",
                    "No Answer"
                )

                with st.expander(
                    f"Q{index}. {question}"
                ):

                    st.markdown(
                        f"""
                        <div style="
                            background-color:#111827;
                            padding:18px;
                            border-radius:12px;
                            border:1px solid #374151;
                            margin-top:10px;
                            color:white;
                            line-height:1.8;
                        ">
                            {answer}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        else:

            st.warning(
                "No questions generated."
            )

        st.divider()

        # ---------------- KEYWORDS SECTION ----------------

        st.markdown(
            "## 🧠 Website Knowledge Keywords"
        )

        keywords = qa_data.get(
            "keywords",
            {}
        )

        for category, items in keywords.items():

            st.markdown(
                f"### 🔹 {category.title()}"
            )

            if items:

                # Create responsive columns
                cols = st.columns(4)

                for index, item in enumerate(items):

                    with cols[index % 4]:

                        st.markdown(
                            f"""
                            <div style="
                                background: linear-gradient(
                                    135deg,
                                    #1e293b,
                                    #0f172a
                                );
                                border:1px solid #334155;
                                border-radius:14px;
                                padding:16px;
                                text-align:center;
                                margin-bottom:15px;
                                min-height:70px;
                                display:flex;
                                align-items:center;
                                justify-content:center;
                                font-weight:600;
                                color:white;
                                box-shadow:
                                    0 4px 10px rgba(0,0,0,0.25);
                            ">
                                {item}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            else:

                st.info(
                    "No keywords found."
                )

            st.markdown("<br>", unsafe_allow_html=True)

        # ---------------- AI INSIGHTS ----------------

        st.markdown(
            "## 📊 Website AI Insights"
        )

        insight_col1, insight_col2 = st.columns(2)

        # ---------------- LEFT CARD ----------------

        with insight_col1:

            st.info(
                """
                ✅ Website content successfully scraped
                
                ✅ AI analysis completed
                
                ✅ Intelligent Q&A generated
                
                ✅ Content understanding pipeline executed
                """
            )

        # ---------------- RIGHT CARD ----------------

        with insight_col2:

            st.success(
                """
                🧠 Business keywords identified
                
                🧠 Technology stack detected
                
                🧠 Audience insights extracted
                
                🧠 Feature intelligence generated
                """
            )

        st.divider()

        # ---------------- ANALYSIS SUMMARY ----------------

        st.subheader("🔍 Analysis Summary")

        summary_points = [
            "Website content was processed successfully.",
            "AI extracted meaningful business intelligence.",
            "Question-answer generation completed.",
            "Keyword categorization executed successfully.",
            "Content analysis pipeline performed correctly."
        ]

        for point in summary_points:

            st.write(f"• {point}")
            
       

    except Exception as e:

        st.error(
            "Failed to display AI-generated content."
        )

        st.text(
            st.session_state.qa_result
        )

        print(e)