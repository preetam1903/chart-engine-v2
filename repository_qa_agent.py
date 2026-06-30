import json

from openai import OpenAI


class RepositoryQAAgent:

    def __init__(self, api_key):

        self.client = OpenAI(api_key=api_key)

    #########################################################

    def ask(

        self,

        repository,

        question

    ):

        prompt = f"""
You are an Executive Manufacturing Intelligence Assistant.

Answer ONLY using the repository below.

If the answer is not present,
say:

Information not available.

Repository

{json.dumps(repository, indent=2)}

Executive Question

{question}

Answer like an executive.

Maximum 5 lines.
"""

        response = self.client.responses.create(

            model="gpt-4.1-mini",

            input=prompt

        )

        return response.output_text.strip()
