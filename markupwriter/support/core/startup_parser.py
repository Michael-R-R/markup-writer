#!/usr/bin/python

import os

from markupwriter.config import ProjectConfig
from markupwriter.common.util import File
from markupwriter.common.tokenizers import EditorTokenizer
from markupwriter.gui.widgets import DocumentEditorWidget
from markupwriter.common.parsers import EditorParser
from markupwriter.common.referencetag import RefTagManager

class StartupParser(object):
    def run(editor: DocumentEditorWidget):
        cpath = ProjectConfig.contentPath()
        if cpath is None:
            return
        
        for uuid in File.findAllFiles(cpath):
            fpath = os.path.join(cpath, uuid)
            content = File.read(fpath)
            if content is None:
                continue
            
            tokenizer = EditorTokenizer(uuid, content, None)
            tokenizer.run()
            
            parser = EditorParser()
            parser.run(uuid, tokenizer.tokens, editor.refManager)

        editor.highlighter.rehighlight()