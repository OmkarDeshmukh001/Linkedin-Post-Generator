# AI LinkedIn Post Generator

An AI-powered LinkedIn post generator that learns a user's writing style from their previous LinkedIn posts and generates new, original posts on different topics while preserving their writing characteristics.

The application uses **LangChain, Groq LLMs, and Streamlit** to analyze previous posts, build a personalized writing style profile, and generate style-conditioned LinkedIn content.

---

## 🚀 Features

- Upload 7–30 previous LinkedIn posts
- Automatic post preprocessing
- Unicode-safe text cleaning
- LLM-based language detection
- Automatic topic/tag extraction
- Similar tag unification
- Writing style analysis
- Personalized writing style profile
- Tone and vocabulary analysis
- Hook and CTA style analysis
- Emoji usage analysis
- Few-shot prompting using previous posts
- Engagement-aware reference post selection
- Generate posts for completely new topics
- English and Hinglish support
- Custom post length selection
- Graceful error handling
- Streamlit-based user interface
- Groq-powered LLM generation

---

## 🎯 Project Objective

The goal of this project is to create a personalized LinkedIn content generation system.

Instead of generating generic LinkedIn posts, the application learns how a particular user writes by analyzing their previous posts.

It identifies patterns such as:

- Language
- Tone
- Vocabulary
- Hook style
- Post structure
- Emoji usage
- Average post length
- CTA style

These characteristics are then provided to the LLM along with relevant reference posts.

The LLM generates a **new and original post on a different topic while following the user's writing style**.

---

## 🧠 How It Works

````text
User uploads previous LinkedIn posts
                ↓
        Input Validation
                ↓
        Text Preprocessing
                ↓
       Metadata Extraction
                ↓
          Tag Unification
                ↓
        Style Analysis
                ↓
      Writing Style Profile
                ↓
     Reference Post Selection
                ↓
   Topic + Style + Examples
                ↓
            Groq LLM
                ↓
      Generated LinkedIn Post
✨ Writing Style Analysis

The application creates a structured writing style profile from the uploaded posts.

Example:

Language       → Hinglish
Tone           → Conversational
Vocabulary     → Simple
Average Length → 9 lines
Emoji Usage    → High
Hook Style     → Direct / Relatable
Structure      → Hook → Story → Insight → Conclusion
CTA Style      → Engagement-focused

This profile is used to guide the LLM during generation.

🔄 Example
User's Previous Writing Style
Hey folks, LangChain ko samajhne ki koshish mein
main AI ki jungle safari pe nikla! 🌲🤖

Har prompt ek naya raasta, aur GenAI ne meri
learning speed ko turbo mode pe daal diya 🚀📚

Kya aap bhi apni AI journey ko next level pe
le jaana chahte ho? Comment karo, let's discuss! 💬✨
New Topic
My experience building a RAG application

The application does not copy the original post.

Instead, it tries to preserve characteristics such as:

Hinglish language
Conversational tone
Simple vocabulary
Short paragraphs
High emoji usage
Personal experience
Enthusiastic tone
Engagement-oriented CTA

while generating completely new content for the new topic.

🏗️ Project Architecture
                    ┌──────────────────────┐
                    │      User Input      │
                    │  Previous LinkedIn   │
                    │        Posts         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Preprocessing      │
                    │  Validation + Clean  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Metadata Extraction │
                    │ Language + Tags       │
                    │ Line Count            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Style Analyzer     │
                    │ Tone + Vocabulary    │
                    │ Hook + Structure     │
                    │ Emoji + CTA          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Style Profile       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Few-Shot Examples   │
                    │ Relevant Posts       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Groq LLM          │
                    │  LangChain Prompting  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Generated LinkedIn   │
                    │        Post          │
                    └──────────────────────┘
🛠️ Tech Stack
Technology	Purpose
Python	Core programming language
Streamlit	Web application interface
LangChain	LLM orchestration and prompting
Groq	LLM inference
Pandas	Data processing and filtering
JSON	Post data storage and processing
python-dotenv	Environment variable management
📁 Project Structure
linkedin-post-generator/
│
├── data/
│   ├── raw_posts.json
│   └── processed_posts.json
│
├── main.py
├── preprocess.py
├── style_analyzer.py
├── few_shot.py
├── post_generator.py
├── llm_helper.py
│
├── requirements.txt
├── README.md
├── .gitignore
│
└── venv/
File Responsibilities
main.py

Handles the Streamlit user interface, file upload, style profile display, topic input, and post generation.

preprocess.py

Handles:

JSON validation
Text cleaning
Metadata extraction
Language detection
Tag extraction
Tag unification
style_analyzer.py

Analyzes uploaded posts and creates the user's writing style profile.

few_shot.py

Processes previous posts and selects suitable reference posts for few-shot prompting.

post_generator.py

Builds the generation prompt using:

Topic
Language
Post length
Style profile
Reference posts

and sends it to the LLM.

llm_helper.py

Initializes the Groq LLM through LangChain.

⚙️ Local Setup
1. Clone the repository
git clone https://github.com/OmkarDeshmukh001/Linkedin-Post-Generator.git
cd Linkedin-Post-Generator
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment

For Git Bash on Windows:

source venv/Scripts/activate
4. Install dependencies
pip install -r requirements.txt
5. Create .env

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here

Never commit your .env file to GitHub.

6. Run the application
python -m streamlit run main.py

The application will be available at:

http://localhost:8501
📄 Input Format

The application accepts a JSON file containing previous LinkedIn posts.

Example:

[
    {
        "text": "Your first LinkedIn post...",
        "engagement": 500
    },
    {
        "text": "Your second LinkedIn post...",
        "engagement": 320
    }
]
Requirements
Minimum: 7 posts
Maximum: 30 posts
text is required
engagement is optional

If engagement is not provided, the application assigns a default value.

🔐 Security

The Groq API key is stored in an environment variable:

GROQ_API_KEY

The .env file is excluded from Git using .gitignore.

Never expose API keys in source code or commit them to GitHub.

🚀 Deployment

The application can be deployed using Streamlit Community Cloud.

Deployment flow:

GitHub Repository
        ↓
Streamlit Community Cloud
        ↓
Configure GROQ_API_KEY
        ↓
Deploy Application
        ↓
Live LinkedIn Post Generator
🔮 Future Improvements

Potential future improvements include:

Semantic similarity-based example selection
Vector database integration
More advanced style embeddings
Multiple user profiles
Authentication
Post history
LinkedIn API integration
Engagement-based generation insights
More language support
Advanced prompt evaluation
Generation quality evaluation
👨‍💻 Author

Omkar Deshmukh

B.E. Artificial Intelligence & Machine Learning

GitHub:
https://github.com/OmkarDeshmukh001

LinkedIn:
https://www.linkedin.com/in/omkar-deshmukh/

⭐ Project Highlights

This project demonstrates practical implementation of:

Generative AI
LLM application development
LangChain
Prompt engineering
Few-shot prompting
Personalized content generation
LLM-based text analysis
Streamlit application development
API-based LLM integration
End-to-end AI application development

### Then save it

In VS Code, save `README.md`.

Then run:

```bash
git add README.md
git commit -m "Add project documentation"
git push
````
