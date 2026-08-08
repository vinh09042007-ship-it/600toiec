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
            questions = []
            
            if category == "exam":
                # For exam, load all available json files in the directory
                questions_dir = base_dir / "assets" / "questions"
                if not questions_dir.exists():
                    raise FileNotFoundError("Questions directory not found.")
                
                for json_file in questions_dir.glob("*.json"):
                    questions.extend(QuestionLoader._parse_json_file(json_file))
                
                if not questions:
                    raise ValueError("No questions found in any database for exam.")
            else:
                # 1. Verify file exists
                if not file_path.exists():
                    raise FileNotFoundError(f"Missing database for '{category}'.")
                    
                questions = QuestionLoader._parse_json_file(file_path)
                
            total_db_size = len(questions)
            print(f"Database size: {total_db_size}")
            
            # Determine limit
            if limit is not None:
                actual_limit = limit
            else:
                actual_limit = QuestionLoader.DEFAULT_TEST_SIZE
            
            # Random selection to exactly match actual_limit
            selected_questions = []
            while len(selected_questions) < actual_limit:
                needed = actual_limit - len(selected_questions)
                if total_db_size <= needed:
                    subset = list(questions)
                    random.shuffle(subset)
                    selected_questions.extend(subset)
                else:
                    subset = random.sample(questions, needed)
                    selected_questions.extend(subset)
                
            print(f"Selected: {len(selected_questions)}")
            print("Question sequence:")
            for i, q in enumerate(selected_questions):
                print(f"{i+1}. {q.text}")
                
            return selected_questions
            
        except Exception as e:
            # Print real exception for debugging
            import traceback
            traceback.print_exc()
            print(f"Error loading {category}:\n{type(e).__name__}: {e}")
            # Fallback question
            return [
                Question(
                    text="Question database could not be loaded.",
                    choices=["Return to Campus", "-", "-", "-"],
                    correct_index=1
                )
            ]

    @staticmethod
    def _parse_json_file(file_path: Path) -> List[Question]:
        """Helper to parse a single JSON file into a list of Questions."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if not isinstance(data, list):
            raise ValueError(f"JSON root must be an array in {file_path.name}.")
            
        if len(data) == 0:
            raise ValueError(f"Question list is empty in {file_path.name}.")
            
        questions = []
        for item in data:
            try:
                if "question" not in item or "choices" not in item or "answer" not in item:
                    print(f"Skipping invalid question in {file_path.name}: Missing required keys.")
                    continue
                    
                if not isinstance(item["choices"], list) or len(item["choices"]) != 4:
                    print(f"Skipping invalid question in {file_path.name}: Choices must be an array of exactly 4 strings.")
                    continue
                    
                correct_idx = int(item["answer"]) + 1
                if correct_idx < 1 or correct_idx > 4:
                    print(f"Skipping invalid question in {file_path.name}: Answer must be between 0 and 3.")
                    continue
                
                # Extract optional context
                context_text = None
                if "passage" in item:
                    context_text = str(item["passage"])
                elif "script" in item:
                    context_text = str(item["script"])
                elif "context" in item:
                    context_text = str(item["context"])
                    
                # Extract optional audio
                audio_file = None
                if "audio" in item:
                    audio_file = str(item["audio"])
                    
                q = Question(
                    text=str(item["question"]),
                    choices=[str(c) for c in item["choices"]],
                    correct_index=correct_idx,
                    context=context_text
                )
                q.audio = audio_file
                questions.append(q)
            
            except Exception as e:
                print(f"Skipping invalid question in {file_path.name}: {e}")
                continue

        return questions
