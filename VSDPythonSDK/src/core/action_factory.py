import os
import importlib
import inspect
from typing import Dict, Type, Optional
from .action import Action
from .logger import Logger

class ActionFactory:
    """Action工厂类，负责管理和创建不同类型的Action实例
    
    该类维护action类型到具体Action类的映射关系，提供动态创建Action实例的功能。
    可以通过register_action方法注册新的Action类型，通过create_action方法创建Action实例。
    """
    
    _action_types: Dict[str, Type[Action]] = {}
    
    @classmethod
    def register_action(cls, action_type: str, action_class: Type[Action]):
        """注册一个新的Action类型
        
        Args:
            action_type: Action的类型标识符
            action_class: Action的具体实现类
        """
        cls._action_types[action_type] = action_class
    
    @classmethod
    def create_action(cls, action: str, context: str, settings: dict, plugin) -> Optional[Action]:
        """创建一个Action实例
        
        Args:
            action: Action的标识符，可以是完整的action字符串(如com.xxx.xxx.time)
            context: Action的上下文标识符
            settings: Action的设置
            
        Returns:
            如果action_type注册成工则返回对应的Action实例，否则返回None
        """
        try:
            # 从完整的action字符串中提取action名称
            action_name = action.split('.')[-1]
            
            action_class = cls._action_types.get(action_name)
            if action_class:
                action_instance = action_class(action, context, settings, plugin)
                if not isinstance(action_instance, Action):
                    Logger.error(f"Created instance is not an Action type: {action_name}")
                    return None
                return action_instance
            else:
                Logger.error(f"Action type not found: {action_name}")
            return None
        except Exception as e:
            Logger.error(f"Error creating action {action}: {str(e)}")
            return None

    @classmethod
    def scan_and_register_actions(cls):
        """扫描actions目录并自动注册所有Action类型"""
        import sys
        import traceback

        # 获取正确的actions目录路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的环境，使用sys._MEIPASS
            base_path = sys._MEIPASS
            # 在打包环境下，从src目录下查找actions目录
            actions_dir = os.path.join(base_path, 'src', 'actions')
        else:
            # 开发环境下使用相对路径
            actions_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'actions')
        if not os.path.exists(actions_dir):
            Logger.error(f"Actions directory not found: {actions_dir}")
            return

        # 将src目录添加到Python路径中
        src_dir = os.path.dirname(actions_dir)
        if src_dir not in sys.path:
            sys.path.insert(0, src_dir)

        for file_name in os.listdir(actions_dir):
            if file_name.endswith('.py') and not file_name.startswith('__'):
                module_name = file_name[:-3]  # 移除.py后缀
                
                try:
                    module = importlib.import_module(f'actions.{module_name}')
                    Logger.info(f"Loading action module: {module_name}")
                    for name, obj in inspect.getmembers(module):
                        if (inspect.isclass(obj) and 
                            issubclass(obj, Action) and 
                            obj != Action):
                            action_type = module_name.lower()
                            cls.register_action(action_type, obj)
                            Logger.info(f"Successfully registered action: {action_type} -> {obj.__name__}")
                            Logger.info(f"Registered action types: {cls._action_types}")
                except Exception as e:
                    import traceback
                    Logger.error(f"Error loading action module {module_name}: {str(e)}")
                    Logger.error(traceback.format_exc())

# 自动扫描并注册所有Action类型
ActionFactory.scan_and_register_actions()