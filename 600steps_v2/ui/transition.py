from ursina import Entity, color, invoke, destroy

class TransitionManager(Entity):
    """
    Manages screen fade transitions between scenes.
    """
    def __init__(self, camera_ui):
        super().__init__(parent=camera_ui)
        self.camera_ui = camera_ui
        self.fade_overlay = Entity(
            parent=self.camera_ui,
            model='quad',
            color=color.rgba(0, 0, 0, 0),
            scale=(2, 1),
            z=-10, # Render on top of everything
            enabled=False
        )
        self.is_transitioning = False

    def transition_to(self, scene_manager, scene_name: str, **kwargs):
        """
        Triggers a fade-out to black, switches the scene, and fades back in.
        """
        if self.is_transitioning:
            return
            
        self.is_transitioning = True
        self.fade_overlay.enabled = True
        
        # Fade to black
        self.fade_overlay.animate_color(color.rgba(0, 0, 0, 1), duration=0.3)
        
        # Execute scene switch in the middle
        invoke(self._execute_switch, scene_manager, scene_name, kwargs, delay=0.35)

    def _execute_switch(self, scene_manager, scene_name, kwargs):
        scene_manager.switch_scene(scene_name, **kwargs)
        
        # Fade back in
        self.fade_overlay.animate_color(color.rgba(0, 0, 0, 0), duration=0.3)
        
        # Disable overlay completely
        invoke(self._finish_transition, delay=0.35)
        
    def _finish_transition(self):
        self.fade_overlay.enabled = False
        self.is_transitioning = False
