import PyPDF2
from transformers import pipeline
import openai
import json
import requests
from io import BytesIO

openai.api_key = "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"

def evaluate_business_pitch(pdf_path):
    try:

        response = requests.get(pdf_path)
        pdf_file = BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        full_text = ""


        for page in pdf_reader.pages:
            full_text += page.extract_text()

        summarizer = pipeline("summarization", model="facebook/bart-base")


        max_chunk = 1000
        chunks = [full_text[i:i + max_chunk] for i in range(0, len(full_text), max_chunk)]

        summarized_text = ""
        for chunk in chunks:
            summary = summarizer(chunk, max_length=100, min_length=30, do_sample=False)
            summarized_text += summary[0]['summary_text'] + "\n"

        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": f'''
                    We have summarized text: {summarized_text}.
                    It is the summary of a business pitch. Your task is to evaluate the idea based on multiple
                    factors like scalability, innovation, etc., and give the percentage score between 50 to 100
                    (it can be a float). Your main task is to give a score based on how efficient the idea is.
                    The output should be in strictly below JSON format and no other field or character should be there:
                       (
                           "title":score
                       )
                       Note: the score should be genuine and should not be the same for all.
                '''
            }]
        )


        response_content = response.choices[0].message.content

        try:
            evaluation = json.loads(response_content)
            return evaluation
        except json.JSONDecodeError:
            print("Error: Unable to parse the response as JSON.")
            print("Response content:", response_content)
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None






# import PyPDF2
# from transformers import pipeline
# import openai
# import json
# import requests
# from io import BytesIO
# openai.api_key = "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"


# def evaluate_business_pitch(pdf_path):
#     try:
#         # Read PDF and extract text
#         response = requests.get(pdf_path)
#         pdf_file = BytesIO(response.content)
#         pdf_reader = PyPDF2.PdfReader(pdf_file)
#         full_text = ""
#         for page in pdf_reader.pages:
#             full_text += page.extract_text()

#         # Summarize text
#         summarizer = pipeline("summarization")
#         max_chunk = 1000
#         chunks = [full_text[i:i + max_chunk]
#                   for i in range(0, len(full_text), max_chunk)]

#         summarized_text = ""
#         for chunk in chunks:
#             summary = summarizer(chunk, max_length=100,
#                                  min_length=30, do_sample=False)
#             summarized_text += summary[0]['summary_text'] + "\n"

#         # Evaluate summarized text using OpenAI
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[{
#                 "role": "user",
#                 "content": f'''
#                     We have summarized text :{summarized_text}.
#                     It is the summary of a business pitch. Your task is to evaluate the idea based on multiple
#                     factors like scalability, innovation, etc., and give the percentage score between 50 to 100
#                     (it can be a float). Your main task is to give a score based on how efficient the idea is.
#                     The output should be in strictly below JSON format and no other field or character should be there:
#                        (
#                            "title":score
#                        )
#                        Note: the score should be genuine and should not be same for all.
#                 '''
#             }]
#         )

#         # Parse and return the response content
#         response_content = response.choices[0].message.content

#         evaluation = json.loads(response_content)  # Parse JSON
#         return evaluation

#     except json.JSONDecodeError:
#         return None
#     except Exception as e:
#         return None
