import json

from llm_helper import llm

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


json_parser = JsonOutputParser()


def clean_text(text):
    """
    Clean invalid Unicode characters so the text
    can safely be processed by the LLM.
    """
    return text.encode("utf-8", "replace").decode("utf-8")


def process_posts(posts):
    """
    Process raw LinkedIn posts and return enriched posts.

    Input:
        List of dictionaries containing at least:
        {
            "text": "...",
            "engagement": 123
        }

    Output:
        List of processed posts containing:
        text, engagement, language, tags, line_count
    """

    enriched_posts = []

    for post in posts:

        cleaned_text = clean_text(post["text"])

        metadata = extract_metadata(cleaned_text)

        processed_post = {
            **post,
            "text": cleaned_text,
            **metadata
        }

        enriched_posts.append(processed_post)

    # Unify similar tags
    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:

        current_tags = post.get("tags", [])

        post["tags"] = list({
            unified_tags.get(tag, tag)
            for tag in current_tags
        })

    return enriched_posts


def extract_metadata(post):

    # Calculate line count using Python
    line_count = len(post.splitlines())

    template = """
You are given a LinkedIn post.

Extract:

1. Language
2. Tags

Requirements:

1. Return a valid JSON object.
2. No preamble or explanation.
3. JSON object must contain exactly:
   language and tags
4. tags must contain maximum two tags.
5. Language must be either:
   - English
   - Hinglish

Hinglish means Hindi + English written using English script.

LinkedIn post:

{post}
"""

    pt = PromptTemplate.from_template(template)

    chain = pt | llm

    try:

        response = chain.invoke(
            input={"post": post}
        )

        result = json_parser.parse(response.content)

        result["line_count"] = line_count

        return result

    except OutputParserException as e:

        response_text = getattr(response, "content", "")

        raise OutputParserException(
            f"Unable to parse metadata from LLM response.\n"
            f"Response: {response_text}"
        ) from e


def get_unified_tags(posts_with_metadata):

    unique_tags = set()

    for post in posts_with_metadata:
        unique_tags.update(post.get("tags", []))

    if not unique_tags:
        return {}

    unique_tags_list = ", ".join(sorted(unique_tags))

    template = """
I will give you a list of LinkedIn post tags.

Unify similar tags.

Examples:

"Jobseekers", "Job Hunting"
→ "Job Search"

"Motivation", "Inspiration", "Drive"
→ "Motivation"

"Personal Growth", "Personal Development",
"Self Improvement"
→ "Self Improvement"

"Scam Alert", "Job Scam"
→ "Scams"

Requirements:

1. Return valid JSON.
2. No explanation.
3. Return a mapping from every original tag
   to its unified tag.
4. Use Title Case.

Example:

{{
    "Jobseekers": "Job Search",
    "Job Hunting": "Job Search",
    "Motivation": "Motivation"
}}

Tags:

{tags}
"""

    pt = PromptTemplate.from_template(template)

    chain = pt | llm

    try:

        response = chain.invoke(
            input={"tags": unique_tags_list}
        )

        result = json_parser.parse(response.content)

        return result

    except OutputParserException as e:

        response_text = getattr(response, "content", "")

        raise OutputParserException(
            f"Unable to parse unified tags.\n"
            f"Response: {response_text}"
        ) from e


def load_raw_posts(uploaded_file):
    """
    Read uploaded JSON file.

    Expected format:

    [
        {
            "text": "LinkedIn post...",
            "engagement": 500
        },
        {
            "text": "Another post...",
            "engagement": 300
        }
    ]
    """

    posts = json.load(uploaded_file)

    if not isinstance(posts, list):
        raise ValueError("Uploaded JSON must contain a list of posts.")

    if len(posts) < 7:
        raise ValueError("Please upload at least 7 LinkedIn posts.")

    if len(posts) > 30:
        raise ValueError("Please upload a maximum of 30 posts.")

    for i, post in enumerate(posts):

        if "text" not in post:
            raise ValueError(
                f"Post {i + 1} is missing the 'text' field."
            )

        if not isinstance(post["text"], str):
            raise ValueError(
                f"Post {i + 1} has invalid text."
            )

        # Engagement is optional
        if "engagement" not in post:
            post["engagement"] = 0

    return posts


if __name__ == "__main__":

    with open(
        "data/raw_posts.json",
        encoding="utf-8"
    ) as file:

        posts = json.load(file)

    processed_posts = process_posts(posts)

    with open(
        "data/processed_posts.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            processed_posts,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Posts processed successfully.")
