from sqlalchemy import create_engine, text
from config import DATABASE_URL
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        logger.info(f"Connecting to database with URL: {DATABASE_URL}")
        self.engine = create_engine(
            DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800
        )
    
    def get_clubs(self):
        """Get all clubs from the database"""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT id, name, icon, slug FROM clubs"))
                return [
                    {
                        "id": row[0],
                        "name": row[1],
                        "icon": row[2],
                        "slug": row[3]
                    } for row in result
                ]
        except Exception as e:
            logger.error(f"Error getting clubs: {e}")
            return []

    def get_existing_questions(self, club_id=1):
        try:
            with self.engine.connect() as connection:
                result = connection.execute(
                    text("SELECT question, correct_answer, options FROM quiz_questions WHERE club_id = :club_id"),
                    {"club_id": club_id}
                )
                return [
                    {
                        "question": row[0],
                        "correct_answer": row[1],
                        "options": row[2]
                    } for row in result
                ]
        except Exception as e:
            logger.error(f"Error getting questions for club {club_id}: {e}")
            return []

    def insert_question(self, question_data, club_id=1):
        try:
            with self.engine.begin() as connection:
                connection.execute(
                    text("""
                        INSERT INTO quiz_questions 
                        (club_id, question, correct_answer, options, difficulty, score) 
                        VALUES (:club_id, :question, :correct_answer, :options, :difficulty, :score)
                    """),
                    {
                        "club_id": club_id,
                        "question": question_data["question"],
                        "correct_answer": question_data["correct_answer"],
                        "options": question_data["options"],
                        "difficulty": question_data.get("difficulty", "medium"),  # default to medium if not provided
                        "score": question_data.get("score", 5)  # default to 5 if not provided
                    }
                )
            return True
        except Exception as e:
            logger.error(f"Error inserting question for club {club_id}: {e}")
            return False 