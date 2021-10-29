import os
# from os import path
from django.apps import AppConfig
from django.conf import settings

import sys
import time
import logging

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler



class MainConfig(AppConfig):
    name = 'main'
    
    def ready(self):
        if not os.path.exists(settings.MEDIA_ROOT): 
            os.makedirs(settings.MEDIA_ROOT) 
        
        path = settings.MEDIA_ROOT
        event_handler = MyEventHandler()
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        # try:
        #     while True:
        #         print(1)
        #         time.sleep(1)
        # finally:
        #     observer.stop()
        #     observer.join()

class MyEventHandler(PatternMatchingEventHandler):
    
       
    # def on_moved(self, event):
    #     super(MyEventHandler, self).on_moved(event)
    #     logging.info("File %s was just moved" % event.src_path)

    def on_created(self, event):
        from .parser import Parser

        super(MyEventHandler, self).on_created(event)
        parser = Parser(event)
        logging.info("File %s was just created" % event.src_path)

    # def on_deleted(self, event):
    #     super(MyEventHandler, self).on_deleted(event)
    #     logging.info("File %s was just deleted" % event.src_path)

    # def on_modified(self, event):
    #     super(MyEventHandler, self).on_modified(event)
    #     logging.info("File %s was just modified" % event.src_path)