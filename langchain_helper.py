# import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType

from langchain_core.tools import Tool
from langchain_experimental.utilities import PythonREPL

from extractQuestions import extract_json_from_text
from generateImage import get_updated_image
from helpers.customPdf import PDF
import os


# from dotenv import load_dotenv

# load_dotenv()


def generate_paper(curriculum, past_papers):
    llm = OllamaLLM(temperature=0.7, model="llama3.1:8b")

    # Define the prompt template with clear separation
    prompt_template_name = PromptTemplate(
        input_variables=['curriculum', 'past_papers'],
        template="""From the Curriculum:
    {curriculum}

    And Sample Past Paper Questions:
    {past_papers}

    Output Format:
    [
        {{
            "questionNumber": "1",
            "questionText": "In a right-angled triangle, the lengths of the two legs are 5 cm and 12 cm. Find the length of the hypotenuse.",
            "givenValues": [5, 12]
            "options": ["13cm", "17cm", "7cm", "11cm"]
        }},
        {{
            "questionNumber": "2",
            "questionText": "The lengths of the two legs of a right-angled triangle are 3 cm and 9 cm. Find the length of the hypotenuse.",
            "givenValues": [3, 9]
            "options": ["10cm", "12cm", "15cm", "8cm"]
        }}
    ]

    Generate two new questions from the Context provided similar to the Sample Quesitons provided where output should be in the template `Output Format` Provided"""
    )

    # Initialize the chain
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="generatedPaper")

    # Call the chain with the correct inputs
    response = name_chain({'curriculum': curriculum, 'past_papers': past_papers})

    dummy_output = """Here is a single question:
[
	{
		"questionNumber": "1",
		"questionText": "In a right-angled triangle, the lengths of the two legs are 5 cm and 12 cm. Find the length of the hypotenuse.",
		"givenValues": [5, 12],
		"options": ["13cm", "17cm", "7cm", "11cm"]
	},
	{
		"questionNumber": "2",
		"questionText": "The lengths of the two legs of a right-angled triangle are 3 cm and 9 cm. Find the length of the hypotenuse.",
		"givenValues": [3, 9],
		"options": ["10cm", "12cm", "15cm", "8cm"]
	}
]"""

    questions = extract_json_from_text(response["generatedPaper"])
    if questions:
        pdf = PDF()

        # Add a page
        pdf.add_page()

        # Set title and author
        pdf.set_title('Sample PDF Document')
        pdf.set_author('Your Name')

        for question in questions:
            base, height = question["givenValues"]
            image_name = get_updated_image("./image_page_0.png", base, height, question["questionNumber"])
            # Instantiate PDF class

            pdf.add_text(question["questionText"])

            # Add an image
            pdf.add_image(image_name, w=100)

            pdf.add_text('a) '+question["options"][0])
            pdf.add_text('b) '+question["options"][1])
            pdf.add_text('c) '+question["options"][2])
            pdf.add_text('d) '+question["options"][3])
        
        # Save the PDF to a file
        pdf.output('sample.pdf')

    
    # Get the current working directory
    current_directory = os.getcwd()
    # return response["generatedPaper"]
    return f"{current_directory}\\sample.pdf"

def langchain_agent():
    
    llm = OllamaLLM(temperature=0.7, model="llama3.1:8b")

    tools = load_tools(["wikipedia", "llm-math"], llm = llm)

    agent = initialize_agent( tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose= True)

    reuslt = agent.run("What is the average age of a dog? Multiply the age by 3")

def lc_tool_calling():
    # Define a simple prompt for code execution
    llm = OllamaLLM(temperature=0.7, model="llama3.1:8b")

    code_prompt = PromptTemplate(
        input_variables=["code"],
        template="""
        You are a Python interpreter. Execute the following code and provide the output:
        {code}
        """,
    )
    
    python_repl = PythonREPL()

    # Create a tool for code execution
    code_tool = Tool(
        name="PythonCodeExecutor",
        func=lambda code: exec(code, globals()),
        description="Executes Python code",
    )

    repl_tool = Tool(
        name="python_repl",
        description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
        func=python_repl.run,
    )

    # Initialize the agent
    agent = initialize_agent(
        tools=[repl_tool],
        code_prompt= code_prompt,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        llm=llm,
        verbose=True
    )

    # Example query
    query = "What is the answer of 2 + 2?"

    code = """import matplotlib.pyplot as plt
    import math

    def plot_right_triangle(base, height, question_number):
        plt.figure()
        plt.plot([0, base], [0, 0], 'k')  # Base
        plt.plot([0, 0], [0, height], 'k')  # Height
        plt.plot([0, base], [height, 0], 'k')  # Hypotenuse
        plt.text(base / 2, -0.5, f'{base} cm', ha='center')
        plt.text(-0.5, height / 2, f'{height} cm', va='center', rotation='vertical')
        plt.xlim(-1, base + 1)
        plt.ylim(-1, height + 1)
        plt.axis('off')
        # plt.title('Right Triangle')
        plt.savefig(f'right_triangle_{question_number}.png')  # Save as image
        #plt.close()

    # Test the function
    plot_right_triangle(30, 4, 1)"""

    # Generate a response
    print(agent.run(code))


if __name__ == "__main__":
    # langchain_agent()
    print(lc_tool_calling())