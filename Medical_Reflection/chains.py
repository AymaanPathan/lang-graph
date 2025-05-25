from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from schema import MedicAnswer

llm = ChatOllama(model="mistral")
base_template = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an AI-powered medical assistant. Your task is to analyze a user's symptoms and return a categorized medical response.

Instructions:
1.{first_instruction}
2. Read the user's symptoms carefully.
3. Analyze and provide a diagnosis or likely condition if appropriate.
4. Suggest remedies across **three categories**:
   - High Risk: Conditions that require urgent medical attention or prescription drugs.
   - Moderate Risk: Common over-the-counter medicines like paracetamol, Dolo 650, etc.
   - Low Risk: Natural or lifestyle remedies such as drinking fluids, taking rest, etc.
5. Give a brief explanation of how each medicine/remedy works and why it is recommended.
6. Be concise, factual, and user-friendly. Avoid unnecessary text.
7. Do not give medical advice that could be harmful. Warn users to consult real doctors in case of doubt.
8. Output your answer in structured bullet points.

Then, reflect on your response by identifying:
- What critical information might be missing? (missing)
- What unnecessary or redundant information could be removed? (superfluous)

Do not respond yet. Await the user's message."""
    ),
    MessagesPlaceholder(variable_name="messages"),
])

first_responder_prompt_template = base_template.partial(
    first_instruction="Respond in a structured Markdown format."
)

revised_instruction = """Revise your previous answer using the new information:
- Use the previous critique to add missing info and remove superfluous parts.
- Must not exceed 250 words.
- Include numerical citations like [1], [2], etc.
- Add a "References" section:
  - [1] https://example.com
  - [2] https://example.com"""

revised_prompt_template = first_responder_prompt_template.partial(
    first_instruction=revised_instruction
)

first_chain= first_responder_prompt_template |llm.with_structured_output(MedicAnswer)
revised_chain = revised_prompt_template |llm.with_structured_output(MedicAnswer)