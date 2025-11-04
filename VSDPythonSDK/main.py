from src.core.plugin import Plugin
import argparse
import sys
import threading
from src.core.logger import Logger
import time

def main():
    Logger.info("Plugin Start")
    parser = argparse.ArgumentParser(description='Stream Dock Plugin')
    parser.add_argument('-port', type=int, required=True, help='WebSocket port number')
    parser.add_argument('-pluginUUID', type=str, required=True, help='Unique identifier for the plugin')
    parser.add_argument('-registerEvent', type=str, required=True, help='Event type for plugin registration')
    parser.add_argument('-info', type=str, required=True, help='JSON string containing Stream Dock and device information')
    args = parser.parse_args()

    try:
        # Logger.info(f"Plugin parameters - Port: {args.port}, UUID: {args.pluginUUID}, Event: {args.registerEvent}, Info: {args.info}")
        time.sleep(1)
        plugin = Plugin(args.port, args.pluginUUID, args.registerEvent, args.info)
        stop_event = threading.Event()
        def on_close(ws, close_status_code, close_msg):
            plugin.stop()
            stop_event.set()
            Logger.info('Plugin stopped')
        
        plugin.ws.on_close = on_close
        stop_event.wait()
            
    except Exception as e:
        Logger.info(e)
        sys.exit(0)

if __name__ == '__main__':
    main()