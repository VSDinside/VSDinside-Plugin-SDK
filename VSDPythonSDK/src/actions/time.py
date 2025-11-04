import json
import time
from src.core.action import Action
from src.core.logger import Logger

class Time(Action):
    def __init__(self, action: str, context: str, settings: dict, plugin):
        super().__init__(action, context, settings, plugin)
        # Set up timer to update time every second
        # 已验证
        self.plugin.timer.set_interval(
            f'time_update_{context}',
            1000,
            lambda: self.set_title(time.strftime('%H:%M:%S'))
        )
        Logger.info(f"[TimeAction] Initialized with context {context}")
    
    def on_will_disappear(self):
        # 已验证
        # Clear the timer when action disappears
        self.plugin.timer.clear_interval(f'time_update_{self.context}')
        Logger.info(f"[TimeAction] Will disappear for context {self.context}")
    
    def on_did_receive_global_settings(self, settings: dict):
        # 已验证
        # Handle global settings update
        Logger.info(f"[TimeAction] Received global settings: {settings}")

    def on_key_down(self, payload: dict):
        # 已验证
        Logger.info(f"[TimeAction] Key down event with payload: {payload}")

    def on_key_up(self, payload: dict):
        # 已验证
        self.set_state(1)
        Logger.info(f"[TimeAction] Key up event with payload: {payload}")

    def on_dial_down(self, payload: dict):
        # 已验证
        Logger.info(f"[TimeAction] Dial down event with payload: {payload}")

    def on_dial_up(self, payload: dict):
        # 已验证
        Logger.info(f"[TimeAction] Dial up event with payload: {payload}")

    def on_dial_rotate(self, payload: dict):
        # 已验证
        Logger.info(f"[TimeAction] Dial rotate event with payload: {payload}")

    def on_device_did_connect(self, payload: dict):
        # 已验证
        Logger.info(f"[TimeAction] Device connected with payload: {payload}")

    def on_device_did_disconnect(self, data: dict):
        # 已验证
        Logger.info(f"[TimeAction] Device disconnected with data: {data}")

    def on_application_did_launch(self, data: dict):
        # 已验证
        Logger.info(f"[TimeAction] Application launched with data: {data}")

    def on_application_did_terminate(self, data: dict):
        # 已验证
        Logger.info(f"[TimeAction] Application terminated with data: {data}")

    def on_system_did_wake_up(self, data: dict):
        # 已验证
        Logger.info(f"[TimeAction] System woke up with data: {data}")

    def on_property_inspector_did_appear(self, data: dict):
        # 已验证
        Logger.info(f"[TimeAction] Property inspector appeared with data: {data}")

    def on_property_inspector_did_disappear(self, data: dict):
        # 已验证
        Logger.info(f"[TimeAction] Property inspector disappeared with data: {data}")

    def on_send_to_plugin(self, payload: dict):
        # 已验证
        Logger.info(f"[TimeAction] Received message from property inspector with payload: {payload}")