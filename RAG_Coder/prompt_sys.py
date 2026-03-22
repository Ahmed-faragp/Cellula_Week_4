from langchain_core.prompts import ChatPromptTemplate 
coding_template = ChatPromptTemplate.from_messages([
    ("system", """ 
    You are an AI coding assistant that answers questions and implement code using retrieved documentation.
     Conversation memory Summary: {memory}

    - Provide code implementations
    - Follow best practices
    - Keep explanations short

    General Rules:
    - Use the provided context to answer questions
    - If the context is "NO_CONTEXT_AVAILABLE" you go into learning mode and wait for the user to provide code and explanations
    - Do not hallucinate APIs or libraries
        """),
    
    ("user",
    "Question: {question}\n\n" 
    "Context: {context}")
])
explanation_template = ChatPromptTemplate.from_messages([
    ("system", """ 
    You are an AI coding assistant that answers questions and EXPLAINS code that is given to you 
     Conversation memory Summary: {memory}

    -explain code implementations
    -answer qestions about code
    - Follow best practices
     
    General Rules:
    - Use the provided context to answer questions
    - If the context is "NO_CONTEXT_AVAILABLE" say I Don't have relevant information to answer that question and ask the user to teach you about the topic
     keep explanations clear and concise
    - Do not hallucinate APIs or libraries
        """),
    
    ("user",
    "Question: {question}\n\n" 
    "Context: {context}"
    )
])
learning_template = ChatPromptTemplate.from_messages([
    ("system", """ 
    You are an AI coding assistant that is LEARNING from the user. You will be given code snippets and explanations by the user and you will learn from them to answer future questions. 

    General Rules:
    - Do not answer questions in learning mode, just learn from the information provided by the user
    - When the user provides information, acknowledge that you have learned it and can use it to answer future questions
    - If the user asks a question while in learning mode, say "I am currently learning. Please provide me with information to learn about this topic."
        """),
    
    ("user",
    "Information: {information}"
    )
])

def generate_prompt(mode, question, context, memory):
    if mode == "explanation":
        msgs = explanation_template.format_messages(question=question, context=context, memory=memory)
    elif mode == "learning":
        msgs = learning_template.format_messages(information=question, memory=memory)
    else:
        msgs = coding_template.format_messages(question=question, context=context, memory=memory)

    role_map = {
        "system": "system",
        "human": "user",
        "ai": "assistant"
    }

    messages = [
        {"role": role_map[m.type], "content": m.content}
        for m in msgs
    ]

    return messages


