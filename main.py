import streamlit as st

from preprocess import (
    load_raw_posts,
    process_posts
)

from style_analyzer import analyze_style

from post_generator import generate_post


# ==========================================
# OPTIONS
# ==========================================

length_options = [
    "Short",
    "Medium",
    "Long"
]

language_options = [
    "English",
    "Hinglish"
]


# ==========================================
# MAIN APP
# ==========================================

def main():

    st.set_page_config(
        page_title="AI LinkedIn Post Generator",
        page_icon="💼",
        layout="wide"
    )

    st.title(
        "💼 AI LinkedIn Post Generator"
    )

    st.caption(
        "Generate LinkedIn posts in your own writing style using LangChain + Groq."
    )

    st.divider()

    # ==========================================
    # STEP 1: UPLOAD POSTS
    # ==========================================

    st.subheader(
        "1. Upload Your Previous LinkedIn Posts"
    )

    uploaded_file = st.file_uploader(
        "Upload a JSON file containing 7–30 of your previous posts",
        type=["json"]
    )

    # ==========================================
    # NO FILE UPLOADED
    # ==========================================

    if uploaded_file is None:

        st.info(
            "Upload your previous LinkedIn posts to create your personalized writing style profile."
        )

        st.markdown(
            """
### Expected JSON format

```json
[
    {
        "text": "Your LinkedIn post here...",
        "engagement": 500
    },
    {
        "text": "Another LinkedIn post...",
        "engagement": 320
    }
]
```

`engagement` is optional.
"""
        )

        return

    # ==========================================
    # PROCESS UPLOADED POSTS
    # ==========================================

    if (
        "processed_posts" not in st.session_state
        or st.session_state.get("uploaded_file_name") != uploaded_file.name
    ):
        try:
            with st.spinner("Reading and analyzing your posts..."):
                raw_posts = load_raw_posts(uploaded_file)
                processed_posts = process_posts(raw_posts)
                style_profile = analyze_style(processed_posts)

                st.session_state.processed_posts = processed_posts
                st.session_state.style_profile = style_profile
                st.session_state.uploaded_file_name = uploaded_file.name

        except ValueError as e:
            st.error(str(e))
            return

        except Exception:
            st.error(
                "Unable to process your LinkedIn posts. Please check your JSON file and try again.")
            return

    # ==========================================
    # GET SESSION DATA
    # ==========================================

    processed_posts = (
        st.session_state.processed_posts
    )

    style_profile = (
        st.session_state.style_profile
    )

    # ==========================================
    # STEP 2: WRITING STYLE PROFILE
    # ==========================================

    st.subheader("2. Your Writing Style Profile")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Language**")
        st.info(style_profile["language"])

        st.markdown("**Average Length**")
        st.info(f'{style_profile["average_length"]} lines')

        st.markdown("**Emoji Usage**")
        st.info(style_profile["emoji_usage"])

    with col2:
        st.markdown("**Tone**")
        st.info(style_profile["tone"])

        st.markdown("**Vocabulary**")
        st.info(style_profile["vocabulary"])

        st.markdown("**Hook Style**")
        st.info(style_profile["hook_style"])

    with col3:
        st.markdown("**Structure**")
        st.info(style_profile["structure"])

        st.markdown("**CTA Style**")
        st.info(style_profile["cta_style"])

        st.markdown("**Posts Analyzed**")
        st.info(str(len(processed_posts)))

    st.divider()

    # ==========================================
    # STEP 3: GENERATE POST
    # ==========================================

    st.subheader(
        "3. Generate Your LinkedIn Post"
    )

    # ------------------------------------------
    # TOPIC
    # ------------------------------------------

    topic = st.text_area(
        "What do you want to post about?",
        placeholder=(
            "Example: My experience building "
            "a RAG application using LangChain"
        ),
        height=100
    )

    # ------------------------------------------
    # LENGTH + LANGUAGE
    # ------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        selected_length = st.selectbox(
            "Post Length",
            options=length_options
        )

    with col2:

        selected_language = st.selectbox(
            "Language",
            options=language_options,
            index=(
                0
                if style_profile["language"] == "English"
                else 1
            )
        )

    # ==========================================
    # GENERATE BUTTON
    # ==========================================

    if st.button(
        "✨ Generate Post",
        use_container_width=True
    ):
        if not topic.strip():
            st.warning("Please enter a topic.")
            return

        try:
            with st.spinner("Writing your LinkedIn post..."):
                post = generate_post(
                    length=selected_length,
                    language=selected_language,
                    topic=topic,
                    processed_posts=processed_posts,
                    style_profile=style_profile
                )

            st.subheader("Generated Post")

            st.text_area(
                "Your personalized LinkedIn post",
                value=post,
                height=300
            )

        except Exception:
            st.error(
                "Unable to generate the post. Please try again."
            )


# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":
    main()
