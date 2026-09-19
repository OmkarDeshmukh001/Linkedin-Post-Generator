from llm_helper import llm
from few_shot import FewShotPosts


def get_length_str(length):

    if length == "Short":
        return "1 to 5 lines"

    if length == "Medium":
        return "6 to 10 lines"

    if length == "Long":
        return "11 to 15 lines"


def generate_post(
    length,
    language,
    topic,
    processed_posts,
    style_profile
):

    few_shot = FewShotPosts(
        processed_posts
    )

    examples = few_shot.get_best_examples(
        length=length,
        language=language,
        tag=None,
        max_examples=2
    )

    prompt = get_prompt(
        length,
        language,
        topic,
        style_profile,
        examples
    )

    response = llm.invoke(prompt)

    return response.content


def get_prompt(
    length,
    language,
    topic,
    style_profile,
    examples
):

    length_str = get_length_str(
        length
    )

    prompt = f"""
Generate a LinkedIn post using the
following information.

Do not include any preamble.

TOPIC:
{topic}

LENGTH:
{length_str}

LANGUAGE:
{language}

WRITING STYLE PROFILE:

Language:
{style_profile["language"]}

Tone:
{style_profile["tone"]}

Average Length:
{style_profile["average_length"]} lines

Emoji Usage:
{style_profile["emoji_usage"]}

Vocabulary:
{style_profile["vocabulary"]}

Hook Style:
{style_profile["hook_style"]}

Structure:
{style_profile["structure"]}

CTA Style:
{style_profile["cta_style"]}

IMPORTANT:

The generated post should feel like it was
written by the same person who created the
provided examples.

Preserve:

- writing tone
- vocabulary simplicity
- sentence style
- paragraph structure
- hook pattern
- emoji behavior
- CTA behavior
- overall formatting

Do not copy any example directly.

Create an original post based on the topic.
"""

    if examples:

        prompt += """

REFERENCE POSTS:

"""

        for i, post in enumerate(examples):

            prompt += f"""
Example {i + 1}:

{post["text"]}

"""

    return prompt
