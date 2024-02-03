#!/usr/bin/python

from markupwriter.common.referencetag import (
    RefTagManager,
)


class EditorParser(object):
    def __init__(self) -> None:
        self.prevTokens: dict[str, dict[str, list[str]]] = dict()
        
        self.prevHandlers: dict[str, function] = {
            "@tag": self._handleRemoveTag,
        }
        
        self.currHandlers: dict[str, function] = {
            "@tag": self._handleAddTag,
        }

    def popPrevUUID(self, uuid: str, refManager: RefTagManager):
        if not uuid in self.prevTokens:
            return
        self._handlePrevTokens(uuid, refManager)
        self.prevTokens.pop(uuid)

    def run(self, uuid: str, tokens: dict[str, list[str]], refManager: RefTagManager):
        self._handlePrevTokens(uuid, refManager)
        self._handleCurrTokens(uuid, tokens, refManager)

        self.prevTokens[uuid] = tokens

    # --- Previous Tokens --- #
    def _handlePrevTokens(self, uuid: str, refManager: RefTagManager):
        prevTokens = self.prevTokens.get(uuid)
        if prevTokens is None:
            return

        for token in prevTokens:
            for tlist in prevTokens[token]:
                self.prevHandlers[token](uuid, tlist, refManager)

    def _handleRemoveTag(self, uuid: str, names: list[str], refManager: RefTagManager):
        for tag in names:
            refManager.removeTag(tag, uuid)

    # --- Current tokens --- #
    def _handleCurrTokens(
        self, uuid: str, tokens: dict[str, list[str]], refManager: RefTagManager
    ):
        for token in tokens:
            for tlist in tokens[token]:
                self.currHandlers[token](uuid, tlist, refManager)

    def _handleAddTag(self, uuid: str, names: list[str], refManager: RefTagManager):
        for tag in names:
            refManager.addTag(tag, uuid)
