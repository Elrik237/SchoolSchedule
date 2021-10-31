import os
# from os import path
from django.apps import AppConfig
from django.conf import settings

import sys
import time
import logging
from numpy import fabs

from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler, FileSystemEventHandler, LoggingEventHandler

import threading


class MainConfig(AppConfig):
    name = 'main'
    
    def ready(self):
        background_thread = threading.Thread(target = self.start_parser, args=())
        background_thread.daemon = True
        background_thread.start()
        
        

    def start_parser(self):
        if not os.path.exists(settings.MEDIA_ROOT): 
            os.makedirs(settings.MEDIA_ROOT) 

        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
        
        path = settings.MEDIA_ROOT
        event_handler = MyEventHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=False)
        observer.start()

        try:
            while observer.is_alive():
                observer.join(1)
        except KeyboardInterrupt:
            observer.stop()
        finally:
            observer.stop()
            observer.join()


class MyEventHandler(RegexMatchingEventHandler):

    try:
        def on_created(self, event):
            from .parser import Parser
            prser = Parser().start(event)
    except Exception as e:
        print(e)

