from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import json
import os

class QuestionGenerator:
    def __init__(self, club_name="Real Madrid"):
        self.club_name = club_name
        self.prompt_template = f"""
        You are a football expert specializing in {club_name} history and statistics. 
        Based on these existing questions about {club_name}:

        {{existing_questions}}

        Generate {{num_questions}} new, unique, and interesting questions about {club_name}. Focus on:
        1. Recent achievements and records (2020-2024)
        2. Historical milestones not covered in existing questions
        3. Player statistics and records
        4. Memorable matches and moments
        5. Club culture and traditions

        For each question, follow this exact format:
        - All text content must be in Russian language
        - The field labels "QUESTION:", "ANSWER:", "OPTIONS:" must remain in English
        - Do not translate or modify these field labels
        QUESTION: [your question here]
        ANSWER: [correct answer]
        OPTIONS:
        1. [correct answer - same as above]
        2. [wrong option]
        3. [wrong option]
        4. [wrong option]
        ===

        Make sure:
        1. All content (questions, answers, and options) must be in Russian language, while keeping the field labels "QUESTION:", "ANSWER:", and "OPTIONS:" in English
        2. Questions are unique and not duplicates of existing ones
        3. Wrong options are plausible but clearly distinct
        4. Each question is separated by "==="
        """
        
        self.prompt = PromptTemplate(
            input_variables=["existing_questions", "num_questions"],
            template=self.prompt_template
        )
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.question_chain = self.prompt | self.llm
    
    def generate_questions(self, existing_questions, num_questions=5):
        # Format existing questions for the prompt
        questions_text = "\n".join([
            f"- {q['question']} (Answer: {q['correct_answer']})" 
            for q in existing_questions
        ])
        
        # Generate new questions using the new invoke syntax
        response = self.question_chain.invoke({
            "existing_questions": questions_text,
            "num_questions": num_questions
        })
        
        # print("\nRaw LLM Response:")
        # print("-" * 50)
        # print(response['text'])
        # print("-" * 50)
        
        # Parse the response into list of question objects
        questions = []
        question_blocks = response['text'].strip().split('===')
        
        for block in question_blocks:
            if not block.strip():
                continue
                
            try:
                # Extract question
                question = block[block.find('QUESTION:') + 9:block.find('ANSWER:')].strip()
                
                # Extract answer
                answer = block[block.find('ANSWER:') + 7:block.find('OPTIONS:')].strip()
                
                # Extract options
                options_text = block[block.find('OPTIONS:'):].strip()
                options = []
                for line in options_text.split('\n')[1:]:  # Skip the "OPTIONS:" line
                    if line.strip() and '. ' in line:
                        options.append(line.split('. ', 1)[1].strip())
                
                if len(options) == 4:  # Only add if we have all 4 options
                    questions.append({
                        'question': question,
                        'correct_answer': answer,
                        'options': options
                    })
            except Exception as e:
                print(f"Error parsing question block: {e}")
                continue
        

        print("new Questions: ", questions)
        return questions 