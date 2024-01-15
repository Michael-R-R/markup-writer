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
        refManager: RefTagManager,
        parent: QObject | None,
    ) -> None:
        super().__init__(parent)
        self.refManager = refManager
        self.prevTokens: dict[str, dict[str, list[str]]] = dict()

    def run(self, uuid: str, tokens: dict[str, list[str]]):
        self._handlePrevTokens(uuid)
        self._handleCurrTokens(uuid, tokens)

        self.prevTokens[uuid] = tokens
        
    def popPrevUUID(self, uuid: str):
        self._handlePrevTokens(uuid)
        self.prevTokens.pop(uuid)

    def _handlePrevTokens(self, uuid: str):
        tempDict = self.prevTokens.get(uuid)
        if tempDict is None:
            return

        func: dict[str, function] = {
            "@tag": self._handleRemoveTag,
        }

        for key in tempDict:
            for t in tempDict[key]:
                func[key](t)

    def _handleRemoveTag(self, names: list[str]):
        for n in names:
            self.refManager.removeTag(n)

    def _handleCurrTokens(self, uuid: str, tokens: dict[str, list[str]]):
        func: dict[str, function] = {
            "@tag": self._handleAddTag,
        }

        for key in tokens:
            for t in tokens[key]:
                func[key](uuid, t)

    def _handleAddTag(self, uuid: str, names: list[str]):
        for n in names:
            self.refManager.addTag(n, uuid)
