import json
import re

from llm_helper import llm

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


json_parser = JsonOutputParser()


def calculate_emoji_usage(posts):

    emoji_count = 0
    total_posts = len(posts)

    for post in posts:

        text = post["text"]

        # Approximate emoji detection
        emojis = re.findall(
            r"[^\x00-\x7F]",
            text
        )

        if len(emojis) > 0:
            emoji_count += 1

    percentage = (
        emoji_count / total_posts
    ) * 100

    if percentage < 30:
        return "Low"

    elif percentage < 70:
        return "Moderate"

    else:
        return "High"


def analyze_style(posts):

    if not posts:
        return {}

    # -------------------------
    # Python-calculated metrics
    # -------------------------

    average_length = round(
        sum(
            post["line_count"]
            for post in posts
        ) / len(posts)
    )

    languages = [
        post["language"]
        for post in posts
    ]

    english_count = languages.count(
        "English"
    )

    hinglish_count = languages.count(
        "Hinglish"
    )

    if hinglish_count > english_count:
        dominant_language = "Hinglish"
    else:
        dominant_language = "English"

    emoji_usage = calculate_emoji_usage(
        posts
    )

    # -------------------------
    # Prepare posts for LLM
    # -------------------------

    post_text = "\n\n".join(
        [
            f"POST {i + 1}:\n{post['text']}"
            for i, post in enumerate(posts)
        ]
    )

    template = """
You are analyzing a person's LinkedIn writing style.

Analyze the provided posts and return a JSON object.

Return exactly these keys:

{{
    "tone": "",
    "vocabulary": "",
    "hook_style": "",
    "structure": "",
    "cta_style": ""
}}

Possible useful values:

Tone:
- Conversational
- Professional
- Inspirational
- Educational
- Storytelling

Vocabulary:
- Simple
- Conversational
- Technical
- Formal

Focus on the actual writing patterns.

Do not invent characteristics that are not visible
in the posts.

Return JSON only.

Posts:

{posts}
"""

    pt = PromptTemplate.from_template(
        template
    )

    chain = pt | llm

    try:

        response = chain.invoke(
            input={
                "posts": post_text
            }
        )

        llm_profile = json_parser.parse(
            response.content
        )

    except OutputParserException:

        llm_profile = {
            "tone": "Conversational",
            "vocabulary": "Simple",
            "hook_style": "Direct",
            "structure": "Short paragraphs",
            "cta_style": "Occasional"
        }

    # -------------------------
    # Final structured profile
    # -------------------------

    style_profile = {
        "language": dominant_language,
        "tone": llm_profile.get(
            "tone",
            "Conversational"
        ),
        "average_length": average_length,
        "emoji_usage": emoji_usage,
        "vocabulary": llm_profile.get(
            "vocabulary",
            "Simple"
        ),
        "hook_style": llm_profile.get(
            "hook_style",
            "Direct"
        ),
        "structure": llm_profile.get(
            "structure",
            "Short paragraphs"
        ),
        "cta_style": llm_profile.get(
            "cta_style",
            "Occasional"
        )
    }

    return style_profile
