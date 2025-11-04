import logging
import os
import sys
from typing import Optional

class Logger:
    """全局日志管理类
    
    使用单例模式实现的日志管理器，提供统一的日志记录接口。
    可以在应用的任何位置使用该类记录日志。
    """
    
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'Logger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._setup_logger()
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> 'Logger':
        """获取Logger单例实例
        
        Returns:
            Logger实例
        """
        if cls._instance is None:
            cls._instance = Logger()
        return cls._instance
    
    @classmethod
    def _setup_logger(cls):
        """设置日志记录器
        
        配置日志记录器的输出格式、日志级别和输出文件。
        """
        if cls._logger is None:
            cls._logger = logging.getLogger('StreamDock')
            cls._logger.setLevel(logging.INFO)
            
            # 获取日志目录路径
            if getattr(sys, 'frozen', False):
                # 如果是打包后的exe
                base_path = os.path.join(os.path.dirname(sys.executable), 'logs')
            else:
                # 如果是开发环境
                base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
            
            # 确保日志目录存在
            try:
                os.makedirs(base_path, exist_ok=True)
                
                # 设置日志文件路径
                log_file = os.path.join(base_path, 'plugin.log')
                
                # 创建文件处理器
                handler = logging.FileHandler(log_file, encoding='utf-8')
                handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
                cls._logger.addHandler(handler)
                
                # 添加控制台输出
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
                cls._logger.addHandler(console_handler)
            except Exception as e:
                print(f"Failed to setup file handler: {e}")
                # 如果文件处理器设置失败，至少确保控制台输出正常工作
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
                cls._logger.addHandler(console_handler)
    
    @classmethod
    def get_logger(cls) -> logging.Logger:
        """获取日志记录器实例
        
        Returns:
            配置好的日志记录器实例
        """
        if cls._logger is None:
            cls._setup_logger()
        return cls._logger
    
    @classmethod
    def info(cls, message: str):
        """记录INFO级别的日志
        
        Args:
            message: 日志消息
        """
        cls.get_instance().get_logger().info(message)
    
    @classmethod
    def error(cls, message: str):
        """记录ERROR级别的日志
        
        Args:
            message: 日志消息
        """
        cls.get_instance().get_logger().error(message)
    
    @classmethod
    def warning(cls, message: str):
        """记录WARNING级别的日志
        
        Args:
            message: 日志消息
        """
        cls.get_instance().get_logger().warning(message)
    
    @classmethod
    def debug(cls, message: str):
        """记录DEBUG级别的日志
        
        Args:
            message: 日志消息
        """
        cls.get_instance().get_logger().debug(message)