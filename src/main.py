from database import Database
from question_generator import QuestionGenerator

def main():
    try:
        # Initialize components
        db = Database()
        generator = QuestionGenerator()
        
        print("Fetching existing questions...")
        existing_questions = db.get_existing_questions()
        print(f"Found {len(existing_questions)} existing questions")
        
        # Number of new questions to generate
        num_new_questions = 5
        
        # Generate new questions
        new_questions = generator.generate_questions(existing_questions, num_new_questions)
        
        # Debug output
        print(f"\nNumber of generated questions: {len(new_questions)}")
        print("\nGenerated questions (raw format):")
        for q in new_questions:
            print(f"Question object: {q}")
            print(f"Type: {type(q)}")
            print(f"Keys: {q.keys() if isinstance(q, dict) else 'N/A'}")
            print("-" * 50)
        
        # Insert new questions
        successful_inserts = 0
        print("\nInserting new questions into database:")
        for question in new_questions:
            success = db.insert_question(question)
            print(f"Insert attempt result: {success}")
            if success:
                successful_inserts += 1
                print(f"✓ Added: {question['question']}")
            else:
                print(f"✗ Failed to add: {question['question']}")
                print(f"Question data: {question}")
        
        print(f"\nSuccessfully added {successful_inserts} new questions!")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 