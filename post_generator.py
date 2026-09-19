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

    few_shot = FewShotPosts(processed_posts)

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

    length_str = get_length_str(length)

    prompt = f"""
You are writing a LinkedIn post for the SAME PERSON
who wrote the reference posts below.

Your job is NOT to write a generic high-quality LinkedIn post.

Your job is to reproduce the person's NATURAL WRITING STYLE
while creating completely original content.

TOPIC:
{topic}

LENGTH:
{length_str}

LANGUAGE:
{language}


WRITING STYLE PROFILE
---------------------

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

Sentence Style:
{style_profile["sentence_style"]}

Humor Style:
{style_profile["humor_style"]}

Directness:
{style_profile["directness"]}

Storytelling Style:
{style_profile["storytelling_style"]}


STYLE RULES
-----------

1. SOUND LIKE THE SAME WRITER.

Do not make the post sound like a generic AI-generated
LinkedIn post.

Preserve the writer's natural simplicity, directness,
humor, sentence patterns and way of explaining ideas.

2. HOOK

Use the same TYPE of hook commonly used by the writer.

Do not automatically start with:
"Ever wondered..."
"Here's the thing..."
"Imagine..."
unless the reference posts actually use this pattern.

3. SENTENCES

Match the reference posts' sentence length.

Prefer natural, simple sentences.

Do not unnecessarily use sophisticated vocabulary.

Do not make every sentence perfectly polished.

4. EMOJIS

This is extremely important.

Use emojis ONLY when they naturally fit the writer's style.

Do NOT put an emoji at the end of every line.

Do NOT increase emoji usage simply because the profile says
"High".

Match the approximate frequency and placement seen in the
reference posts.

5. HUMOR

If the writer uses humor, sarcasm or relatable comparisons,
use it naturally.

Do not force jokes into every post.

6. TECHNICAL CONTENT

Explain AIML concepts in simple language.

Avoid turning the post into a textbook explanation.

The technical concept should support the story or observation.

7. PERSONAL EXPERIENCE

When appropriate, write from personal experience or observation,
because this matches the reference writing style.

8. STRUCTURE

Follow the writer's natural progression.

For example:

Hook
→ personal experience / observation
→ simple explanation
→ realization or lesson
→ encouragement / CTA

But do NOT force this exact structure if the reference posts
show another pattern.

9. CTA

Use the writer's natural CTA style.

Do not always end with:
"What do you think?"
"Let me know in the comments."

Only use a question or CTA when it matches the reference style.

10. ORIGINALITY

Do not copy sentences, phrases, examples, stories or ideas
from the reference posts.

Learn the STYLE, not the CONTENT.

11. FORMATTING

Preserve the writer's natural use of:
- line breaks
- short paragraphs
- questions
- punctuation
- capitalization
- conversational expressions

12. DO NOT OVERWRITE

Avoid unnecessarily motivational or inspirational language.

Do not add phrases such as:
"unlock your potential"
"embrace the journey"
"game changer"
"transform your future"
unless the reference writer actually uses this type of language.

Generate ONLY the LinkedIn post.
Do not provide explanations.

"""

    if examples:

        prompt += "\nREFERENCE POSTS:\n"

        for i, post in enumerate(examples):

            prompt += f"""
Example {i + 1}:

{post["text"]}

"""

    return prompt
