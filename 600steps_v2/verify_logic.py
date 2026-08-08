import sys
import os
sys.path.append(os.path.abspath('c:/600toiec/600steps_v2'))

from player.profile import PlayerProfile
from core.quest_manager import QuestManager

class MockEventBus:
    def subscribe(self, *args): pass
    def emit(self, *args, **kwargs): pass

print("--- STARTING VERIFICATION ---")

profile = PlayerProfile("Test")
qm = QuestManager(profile, MockEventBus())

def simulate_building_finish(building_name, correct_answers):
    passed = correct_answers >= 5
    if passed:
        setattr(profile, f"{building_name.lower()}_passed", True)
        qm.add_progress(1, building_name)
        
        active_q = qm.get_active_quest()
        if active_q and active_q.target_building.lower() == building_name.lower():
            qm.profile.quest_progress = active_q.target_amount
            qm._complete_active_quest()

# 1. Start with Grammar
profile.active_quest_id = "grammar_lesson"

# 2. Verify 4/10 is NOT passed
print(f"Testing Grammar with 4/10...")
simulate_building_finish("Grammar", 4)
print(f"Grammar Passed? {profile.grammar_passed} (Expected: False)")
print(f"Active Quest: {profile.active_quest_id} (Expected: grammar_lesson)")

# 3. Verify 5/10 IS passed
print(f"\nTesting Grammar with 5/10...")
simulate_building_finish("Grammar", 5)
print(f"Grammar Passed? {profile.grammar_passed} (Expected: True)")
print(f"Active Quest: {profile.active_quest_id} (Expected: vocabulary_lesson)")

# 4. Verify 3/4 passed buildings still keep Final Exam locked
simulate_building_finish("Vocabulary", 10)
simulate_building_finish("Listening", 10)
print(f"\n3/4 Buildings Passed. Final Exam Unlocked? {qm.is_building_unlocked('exam')} (Expected: False)")
print(f"Reading Passed? {profile.reading_passed} (Expected: False)")
print(f"Active Quest: {profile.active_quest_id} (Expected: reading_lesson)")

# 6. Verify Reading participates correctly
simulate_building_finish("Reading", 7)
print(f"\nTesting Reading with 7/10...")
print(f"Reading Passed? {profile.reading_passed} (Expected: True)")
print(f"Active Quest: {profile.active_quest_id} (Expected: exam_quest)")

# 5. Verify 4/4 passed buildings unlock Final Exam
print(f"\n4/4 Buildings Passed. Final Exam Unlocked? {qm.is_building_unlocked('exam')} (Expected: True)")

# 7. Persistence is handled by SaveManager which we mocked out of this test, but we can verify profile dict
print(f"\nProfile Dict Dump (Persistence Check):")
building_stats = profile.to_dict()["building_stats"]
print(f"Grammar passed in dict: {building_stats['Grammar']['passed']}")
print(f"Reading passed in dict: {building_stats['Reading']['passed']}")
