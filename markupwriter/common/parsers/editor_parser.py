#!/usr/bin/python

from PyQt6.QtCore import (
    QObject,
)

from markupwriter.common.referencetag import (
    RefTagManager,
)


class EditorParser(QObject):
    def __init__(
        self,
        parent: QObject | None,
    ) -> None:
        super().__init__(parent)

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
        tempDict = self.prevTokens.get(uuid)
        if tempDict is None:
            return

        for key in tempDict:
            for t in tempDict[key]:
                self.prevHandlers[key](t, refManager)

    def _handleRemoveTag(self, names: list[str], refManager: RefTagManager):
        for n in names:
            refManager.removeTag(n)

    # --- Current tokens --- #
    def _handleCurrTokens(
        self, uuid: str, tokens: dict[str, list[str]], refManager: RefTagManager
    ):
        for key in tokens:
            for t in tokens[key]:
                self.currHandlers[key](uuid, t, refManager)

    def _handleAddTag(self, uuid: str, names: list[str], refManager: RefTagManager):
        for n in names:
            refManager.addTag(n, uuid)
