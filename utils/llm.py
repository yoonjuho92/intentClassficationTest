from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Set up the language model and chain
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # Using GPT-4 as a stand-in for GPT-4-Mini

def call_llm(intent, rule, user_input):

    prompt = PromptTemplate(
        template="""
        Below are the NLU rule for entity classification.
        Detect entities from user_input with the rule.
        If there is no entity, leave the entity empty.

        Rule:
        {rule}

        Input: {user_input}

        Generate Only JSON object ouput with the following structure:
        {{
            "text" : "inputText",
            "intent": {intent},
            "entity": {{
                entityKey: entityValue
            }}
        }}
        
        If there's time value in entity. Format the value yyyy-mm-dd. For example, "2012년" to "2012".
        And today is {today}, so "지난달" is {today}'s month minus one.
        """
    )

    chain = prompt | llm | JsonOutputParser()

    # Run the chain and return
    return chain.invoke({"intent":intent,"rule": rule, "user_input": user_input, "today": datetime.today().strftime('%Y-%m-%d')})