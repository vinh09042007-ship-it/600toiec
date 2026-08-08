from ursina import Entity
import config
from core.events import Events

class DebugMenu(Entity):
    """
    Developer Debug Menu mapping F6-F12 to specific progression shortcuts.
    Only enabled if config.DEBUG_MODE is True.
    """
    def __init__(self, game, **kwargs):
        super().__init__(ignore_paused=True, **kwargs)
        self.game = game
        
    def input(self, key: str) -> None:
        if not getattr(config, 'DEBUG_MODE', False):
            return
            
        if key == 'f6':
            self._complete_specific_quest('tutorial_grammar')
        elif key == 'f7':
            self._complete_specific_quest('vocab_lesson')
        elif key == 'f8':
            self._complete_specific_quest('listening_lesson')
        elif key == 'f9':
            self._complete_specific_quest('reading_lesson')
        elif key == 'f10':
            print("[TRACE] DebugMenu: F10 pressed: Passing Final Exam with score 650")
            self._complete_specific_quest('exam_quest')
            print("[TRACE] DebugMenu: Calling switch_scene to campus with game_completed=True")
            self.game.scene_manager.switch_scene("campus", final_score=650, game_completed=True)
            print("[TRACE] DebugMenu: switch_scene returned")
        elif key == 'f11':
            print("[DEBUG] F11 pressed: Triggering Victory Overlay on Campus")
            self.game.scene_manager.switch_scene("campus", final_score=650, game_completed=True)
        elif key == 'f12':
            print("[DEBUG] F12 pressed: Resetting Progress")
            self._reset_progress()
            
    def _complete_specific_quest(self, quest_id: str) -> None:
        qm = self.game.quest_manager
        quest = qm.get_quest(quest_id)
        if not quest:
            return
            
        print(f"[DEBUG] Completing quest: {quest.title}")
        
        if quest_id in qm.profile.completed_quests:
            print(f"[DEBUG] Quest {quest_id} already completed.")
            return
            
        if qm.profile.active_quest_id != quest_id:
            qm._accept_quest(quest_id)
            
        qm.add_progress(quest.target_amount, quest.target_building)
        qm._complete_active_quest()
        
    def _reset_progress(self) -> None:
        qm = self.game.quest_manager
        qm.profile.completed_quests.clear()
        qm.profile.active_quest_id = None
        qm.profile.quest_progress = 0
        qm.profile.total_coins = 0
        qm.profile.total_exp = 0
        qm.event_bus.emit(Events.QUEST_STATE_CHANGED)
        
        from core.save_manager import SaveManager
        SaveManager.save_profile(qm.profile)
        
        # Reload campus to reflect changes
        self.game.scene_manager.switch_scene("campus")
