import json
import re

from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

json_parser = JsonOutputParser()


def calculate_emoji_usage(posts):
    """
    Estimate emoji usage based on:
    - percentage of posts containing emojis
    - average number of emojis per post
    """

    total_posts = len(posts)

    if total_posts == 0:
        return "Low"

    posts_with_emoji = 0
    total_emojis = 0

    # Basic emoji ranges.
    emoji_pattern = re.compile(
        r"[\U0001F300-\U0001FAFF"
        r"\U00002700-\U000027BF"
        r"\U0001F1E6-\U0001F1FF]"
    )

    for post in posts:
        emojis = emoji_pattern.findall(post["text"])

        if emojis:
            posts_with_emoji += 1
            total_emojis += len(emojis)

    percentage = (posts_with_emoji / total_posts) * 100
    average_emojis = total_emojis / total_posts

    if percentage < 30 or average_emojis < 0.5:
        return "Low"

    elif percentage < 70 or average_emojis <= 2:
        return "Moderate"

    else:
        return "High"


def analyze_style(posts):

    if not posts:
        return {}

    average_length = round(
        sum(post["line_count"] for post in posts) / len(posts)
    )

    languages = [post["language"] for post in posts]

    english_count = languages.count("English")
    hinglish_count = languages.count("Hinglish")

    dominant_language = (
        "Hinglish"
        if hinglish_count > english_count
        else "English"
    )

    emoji_usage = calculate_emoji_usage(posts)

    post_text = "\n\n".join(
        [
            f"POST {i + 1}:\n{post['text']}"
            for i, post in enumerate(posts)
        ]
    )

    template = """
You are analyzing the writing style of a LinkedIn creator.

Study the posts carefully and identify the creator's ACTUAL writing patterns.

Do NOT describe generic LinkedIn writing.
Do NOT make the writing sound more professional than it actually is.
Do NOT invent characteristics that are not visible in the posts.

Return exactly this JSON:

{{
    "tone": "",
    "vocabulary": "",
    "hook_style": "",
    "structure": "",
    "cta_style": "",
    "sentence_style": "",
    "humor_style": "",
    "directness": "",
    "storytelling_style": ""
}}

Analyze:

1. Tone
Examples:
- Conversational
- Professional
- Inspirational
- Educational
- Emotional
- Humorous
- Sarcastic

2. Vocabulary
Examples:
- Simple
- Conversational
- Technical
- Formal

3. Hook Style
Describe HOW the writer usually starts posts.
Examples:
- Direct statement
- Question
- Relatable analogy
- Personal experience
- Humor
- Controversial observation
- Emotional statement

4. Structure
Describe the common progression of the post.

5. CTA Style
Describe how the writer ends posts.
Examples:
- Direct question
- Soft encouragement
- Comment invitation
- Reflection
- No CTA

6. Sentence Style
Pay attention to:
- short vs long sentences
- sentence fragments
- conversational wording
- use of questions
- line breaks
- simple vs complex grammar

7. Humor Style
Describe whether humor is:
- absent
- occasional
- sarcastic
- observational
- analogy-based
- punchline-based

8. Directness
Describe whether the writer is:
- indirect
- balanced
- blunt/direct

9. Storytelling Style
Describe whether posts use:
- personal experience
- hypothetical situations
- analogies
- observations
- advice
- emotional storytelling

IMPORTANT:
The goal is to reproduce the creator's natural writing behavior,
not generic polished LinkedIn content.

Return JSON only.

Posts:

{posts}
"""

    pt = PromptTemplate.from_template(template)

    chain = pt | llm

    try:
        response = chain.invoke(
            input={"posts": post_text}
        )

        llm_profile = json_parser.parse(
            response.content
        )

    except OutputParserException:

        llm_profile = {
            "tone": "Conversational",
            "vocabulary": "Simple",
            "hook_style": "Direct or relatable",
            "structure": "Hook → explanation → lesson",
            "cta_style": "Occasional question",
            "sentence_style": "Short conversational sentences",
            "humor_style": "Occasional",
            "directness": "Direct",
            "storytelling_style": "Personal experience and observations"
        }

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
            "Direct or relatable"
        ),
        "structure": llm_profile.get(
            "structure",
            "Hook → explanation → lesson"
        ),
        "cta_style": llm_profile.get(
            "cta_style",
            "Occasional question"
        ),
        "sentence_style": llm_profile.get(
            "sentence_style",
            "Short conversational sentences"
        ),
        "humor_style": llm_profile.get(
            "humor_style",
            "Occasional"
        ),
        "directness": llm_profile.get(
            "directness",
            "Direct"
        ),
        "storytelling_style": llm_profile.get(
            "storytelling_style",
            "Personal experience and observations"
        )
    }

    return style_profile
