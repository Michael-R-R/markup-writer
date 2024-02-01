#!/usr/bin/python

import os

from markupwriter.config import AppConfig
from markupwriter.common.util import File
from markupwriter.common.tokenizers import EditorTokenizer
from markupwriter.common.parsers import EditorParser
import markupwriter.mvc.controller.core.central_widget_controller as cwc


class StartupParser(object):
    def run(cwc: cwc.CentralWidgetController):
        cpath = AppConfig.projectContentPath()
        if cpath is None:
            return
        
        dec = cwc.model.docEditorController
        refManager = dec.model.refManager
        
        for uuid in File.findAllFiles(cpath):
            fpath = os.path.join(cpath, uuid)
            content = File.read(fpath)
            if content is None:
                continue
            
            tokenizer = EditorTokenizer(uuid, content, None)
            tokenizer.run()
            
            parser = EditorParser(None)
            parser.run(uuid, tokenizer.tokens, refManager)
