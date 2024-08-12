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
from generateImage import get_new_image
from helpers.saveQuestionImage import save_right_triangle
from helpers.customPdf import PDF
import os
import json

# from dotenv import load_dotenv

# load_dotenv()


def generate_paper(curriculum, past_papers):
    llm = OllamaLLM(temperature=0.7, model="llama3.1:8b")

    past_questions = preprocess_input(past_papers)

    # Define the prompt template with clear separation
    prompt_template_name = PromptTemplate(
        input_variables=['curriculum', 'past_papers'],
        template="""Task:

Generate two new multiple-choice questions based on the provided Curriculum. The new questions should be similar in structure to the provided sample questions

{curriculum}

Sample Questions Format:
{past_papers}

Instructions:

Follow the format of the sample questions.
Ensure the questions involve either finding the hypotenuse or one of the legs of a right-angled triangle using the Pythagorean Theorem.
Provide the necessary values and multiple-choice options for each question.
Maintain the JSON structure."""
    )

    # Initialize the chain
    name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="generatedPaper")

    # Call the chain with the correct inputs
    response = name_chain({'curriculum': curriculum, 'past_papers': past_questions})
    
    questions = extract_json_from_text(response['generatedPaper'])
    if questions:
        pdf = PDF()

        # Add a page
        pdf.add_page()

        # Set title and author
        pdf.set_title('Sample PDF Document')
        pdf.set_author('Your Name')

        for question in questions:
            image_name = get_new_image(question['givenValues'], question['toFind'], question["questionNumber"])
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
    return f"{current_directory}\\sample_1.pdf"


def preprocess_input(past_papers):
    llm = OllamaLLM(temperature=0.7, model="gemma2:2b")

    # Define the prompt template with clear separation
    preprocess_prompt_template = PromptTemplate(
        input_variables=['past_papers'],
        template="""
You will be provided with a list of mathematical questions. Your task is to extract the key information from each question, such as the quantities given, what needs to be found, and the multiple-choice options. Then, organize this information in a structured JSON format with the following attributes:

questionNumber: The number of the question.
questionText: The full text of the question.
givenValues: A dictionary of the values provided in the question (e.g., base, height, radius, etc.).
toFind: The specific value or concept that needs to be determined (e.g., hypotenuse, area, length, etc.).
options: A list of the multiple-choice options provided.

Example Questions:
In a right-angled triangle, the lengths of the two legs are 5 cm and 12 cm. Find the length of the hypotenuse.

a) 13 cm
b) 17 cm
c) 7 cm
d) 11 cm
In a right-angled triangle, one leg is 8 cm and the hypotenuse is 15 cm. Find the length of the other leg.

a) 7 cm
b) 9 cm
c) 11 cm
d) 13 cm

Example Output:
[
	{{
		"questionNumber": "1",
		"questionText": "In a right-angled triangle, the lengths of the two legs are 5 cm and 12 cm. Find the length of the hypotenuse.",
		"givenValues": {{"base": 5, "height": 12}},
		"toFind": "hypotenuse",
		"options": ["13 cm", "17 cm", "7 cm", "11 cm"]
	}},
	{{
		"questionNumber": "2",
		"questionText": "In a right-angled triangle, one leg is 8 cm and the hypotenuse is 15 cm. Find the length of the other leg.",
		"givenValues": {{"base": 8, "hypotenuse": 15}},
		"toFind": "height",
		"options": ["7 cm", "9 cm", "11 cm", "13 cm"]
	}}
]    
Given Questions:
{past_papers}

Instructions:

For each question, carefully extract and categorize the numerical values or terms provided.
Identify what needs to be calculated or determined, and categorize this under toFind.
List the options exactly as they are provided, in the same order.
Organize everything in a JSON format as described above.
Provide only the output no additional details or explanations."""
    )

    # Initialize the chain
    name_chain = LLMChain(llm=llm, prompt=preprocess_prompt_template, output_key="preprocessedQuestions")

    # Call the chain with the correct inputs
    response = name_chain({'past_papers': past_papers})

    dummy_output = """Here is a single question:
[
  {
    "questionNumber": "1",
    "questionText": "The hypotenuse of a right-angled triangle is 16 cm and one leg is 3 cm. Find the length of the other leg.",
    "givenValues": {"base": 3, "hypotenuse": 16},
    "toFind": "height",
    "options": ["13 cm", "15 cm", "11 cm", "9 cm"]
  }
]"""
    folder_path = "meta"
    questions = extract_json_from_text(response['preprocessedQuestions'])
    if questions:
        for question in questions:
            givenValues = question["givenValues"]
            base = None
            height = None
            hypotenuse = None
            if "base" in givenValues:
                base = givenValues['base']
            if "height" in givenValues:
                height = givenValues['height']
            if "hypotenuse" in givenValues:
                hypotenuse = givenValues['hypotenuse']
            
            image_path = save_right_triangle(base, height, hypotenuse, question_number=question['questionNumber'])

            question["image_path"] = image_path

            # Specify the filename
            filename = f"{folder_path}/{os.path.splitext(os.path.basename(image_path))[0]}.json"

            # Write the list of dictionaries to a JSON file
            with open(filename, 'w') as json_file:
                json.dump(question, json_file, indent=4)

            print(f"{question} has been written to {filename}")
    
    return questions

if __name__ == "__main__":
    # langchain_agent()
#     print(preprocess_input("""The lengths of the two legs of a right-angled triangle are 3 cm and 9 cm. Find the length of the hypotenuse.

# a) 10 cm
# b) 12 cm
# c) 15 cm
# d) 18 cm"""))
    generate_paper("", "")
    