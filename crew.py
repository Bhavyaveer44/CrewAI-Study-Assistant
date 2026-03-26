# 3 agents, 3 tasks, Crew orchestrates them.
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

# LLM 
llm = "groq/llama-3.1-8b-instant"

# TOOL — Google search via Serper
# CrewAI reads SERPER_API_KEY from your .env automatically
search_tool = SerperDevTool()

# AGENTS
# role + goal + backstory are injected into the LLM system prompt
researcher = Agent(
    role="Research Specialist",
    goal=(
        "Find the most accurate, up-to-date information about {topic}. "
        "Focus on key concepts, real-world examples, and recent developments."
    ),
    backstory=(
        "You are a meticulous researcher who digs deep into topics and "
        "surfaces reliable, structured information from the web. "
        "You always cite what you found and organize it clearly."
    ),
    tools=[search_tool],  # only this agent can search Google
    llm=llm,
    verbose=True,
    max_iter=3,           # max 3 search loops before stopping
)

explainer = Agent(
    role="Learning Coach",
    goal=(
        "Take raw research about {topic} and turn it into a crystal-clear "
        "explanation that a curious beginner could understand instantly. "
        "Use analogies, bullet points, and a short summary paragraph."
    ),
    backstory=(
        "You are an expert educator who makes complex ideas click instantly. "
        "You never use jargon without explaining it. "
        "Your explanations always include a real-world analogy."
    ),
    llm=llm,
    verbose=True,
    # No tools — pure reasoning only
)

quiz_master = Agent(
    role="Quiz Designer",
    goal=(
        "Create exactly 5 multiple-choice questions about {topic} based on "
        "the explanation provided. Each question must test a distinct concept. "
        "Always include the correct answer and a one-sentence explanation."
    ),
    backstory=(
        "You design quizzes that reveal whether someone truly understood a topic, "
        "not just memorised facts. Your questions are clear and progressively harder."
    ),
    llm=llm,
    verbose=True,
    # No tools — only reads context from previous task
)

# TASKS
# description = exact instructions for the agent
# expected_output = what good output looks like
# context=[] = pass a previous task's output into this task
# output_file = auto-save result as markdown

research_task = Task(
    description=(
        "Search Google thoroughly for '{topic}'. Collect and structure:\n"
        "1. Core definition — what is it in one clear sentence?\n"
        "2. How it works — the underlying mechanism or process\n"
        "3. Two or three real-world examples or applications\n"
        "4. One surprising or counterintuitive fact\n"
        "5. Any recent developments or current relevance\n\n"
        "Return a well-structured markdown report with these as section headers."
    ),
    expected_output=(
        "A markdown report with 5 sections: Definition, How It Works, "
        "Real-World Examples, Surprising Fact, Recent Developments."
    ),
    agent=researcher,
    output_file="outputs/01_research.md",
)

explain_task = Task(
    description=(
        "Using the research report in your context, write a "
        "beginner-friendly explanation of '{topic}':\n"
        "1. Start with ONE plain-English summary sentence (no jargon)\n"
        "2. Give one everyday analogy that makes the core idea click\n"
        "3. List exactly 5 key takeaways as bullet points\n"
        "4. End with a short 'Why It Matters' paragraph (3-4 sentences)\n\n"
        "Write for someone with ZERO background in this topic."
    ),
    expected_output=(
        "A beginner-friendly markdown explanation with: 1-sentence summary, "
        "analogy, 5 bullet takeaways, and a 'Why It Matters' section."
    ),
    agent=explainer,
    context=[research_task],  
    output_file="outputs/02_explanation.md",
)

quiz_task = Task(
    description=(
        "Based on the explanation of '{topic}' in your context, create a "
        "5-question multiple-choice quiz:\n"
        "- Each question has exactly 4 options labelled A, B, C, D\n"
        "- Mark the correct answer with a checkmark after the option\n"
        "- Add a one-sentence explanation below each question\n"
        "- Questions go from easy to hard (Q1=easy, Q5=hardest)\n\n"
        "Format as clean markdown numbered Q1 through Q5."
    ),
    expected_output=(
        "A 5-question MCQ quiz in markdown with A-D options, "
        "correct answers marked, and one-sentence explanations."
    ),
    agent=quiz_master,
    context=[explain_task],   
    output_file="outputs/03_quiz.md",
)

# CREW
# Assembles agents + tasks, sets execution order
# Process.sequential = runs tasks one by one, passing context forward
study_crew = Crew(
    agents=[researcher, explainer, quiz_master],
    tasks=[research_task, explain_task, quiz_task],
    process=Process.sequential,
    verbose=True,
)
