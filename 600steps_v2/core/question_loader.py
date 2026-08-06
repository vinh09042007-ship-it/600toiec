import json
import os
import random
from pathlib import Path
from typing import List
from core.quiz import Question

class QuestionLoader:
    """
    Handles loading and parsing of question databases from JSON files.
    """
    
    DEFAULT_TEST_SIZE = 10
    
    @staticmethod
    def load_questions(category: str, limit: int | None = None) -> List[Question]:
        """
        Loads questions for a specific category.
        
        Args:
            category (str): The category name (e.g., 'grammar', 'reading').
            limit (int | None): Maximum number of questions to return.
            
        Returns:
            List[Question]: A list of validated Question objects.
        """
        # Resolve base directory (parent of core folder is 600steps_v2)
        base_dir = Path(__file__).resolve().parent.parent
        file_path = base_dir / "assets" / "questions" / f"{category}.json"
        
        print(f"Loading category: {category}")
        print(f"Looking for: {file_path}")
        print(f"Exists: {file_path.exists()}")
        
        try:
            # 1. Verify file exists
            if not file_path.exists():
                raise FileNotFoundError(f"Missing database for '{category}'.")
                
            # 2. Verify JSON is valid
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            if not isinstance(data, list):
                raise ValueError("JSON root must be an array.")
                
            if len(data) == 0:
                raise ValueError("Question list is empty.")
                
            questions = []
            
            # 3. Verify format and convert
            for item in data:
                if "question" not in item or "choices" not in item or "answer" not in item:
                    raise KeyError("Missing required keys ('question', 'choices', 'answer').")
                    
                if not isinstance(item["choices"], list) or len(item["choices"]) != 4:
                    raise ValueError("Choices must be an array of exactly 4 strings.")
                    
                # Convert 0-indexed JSON answer to 1-indexed Question correct_index
                correct_idx = int(item["answer"]) + 1
                if correct_idx < 1 or correct_idx > 4:
                    raise ValueError("Answer must be between 0 and 3.")
                    
                questions.append(
                    Question(
                        text=str(item["question"]),
                        choices=[str(c) for c in item["choices"]],
                        correct_index=correct_idx
                    )
                )
                
            total_db_size = len(questions)
            print(f"Database size: {total_db_size}")
            
            # Determine limit
            actual_limit = limit if limit is not None else QuestionLoader.DEFAULT_TEST_SIZE
            
            # Random selection
            if total_db_size <= actual_limit:
                selected_questions = questions
            else:
                selected_questions = random.sample(questions, actual_limit)
                
            # Shuffle the selected subset
            random.shuffle(selected_questions)
                
            print(f"Selected: {len(selected_questions)}")
            print("Question sequence:")
            for i, q in enumerate(selected_questions):
                print(f"{i+1}. {q.text}")
                
            return selected_questions
            
        except Exception as e:
            print(f"Error loading {file_path}:\n{type(e).__name__}: {e}")
            # Fallback question
            return [
                Question(
                    text="Question database could not be loaded.",
                    choices=["Return to Campus", "-", "-", "-"],
                    correct_index=1
                )
            ]
