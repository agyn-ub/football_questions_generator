from sqlalchemy import create_engine, text
from config import DATABASE_URL
import json

class Database:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
    
    def get_existing_questions(self):
        with self.engine.connect() as connection:
            result = connection.execute(text("SELECT question, correct_answer, options FROM quiz_questions"))
            questions = [
                {
                    "question": row[0],
                    "correct_answer": row[1],
                    "options": row[2]
                } for row in result
            ]
        return questions
    
    def insert_question(self, question_data):
        try:
            with self.engine.connect() as connection:
                connection.execute(
                    text("""
                        INSERT INTO quiz_questions (question, correct_answer, options) 
                        VALUES (:question, :correct_answer, :options)
                    """),
                    {
                        "question": question_data["question"],
                        "correct_answer": question_data["correct_answer"],
                        "options": question_data["options"]
                    }
                )
                connection.commit()
            return True
        except Exception as e:
            print(f"Error inserting question: {e}")
            return False 