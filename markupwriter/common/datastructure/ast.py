#!/usr/bin/python


class Node(object):
    def __init__(self, data: str) -> None:
        self.data = data
        self.parent: Node = None
        self.children: list[Node] = list()


class AST(object):
    def __init__(self, uuid: str) -> None:
        self.root = Node(uuid)
        
    def addAtExpression(self, tokens: list[str]):
        count = len(tokens)
        if count < 2:
            return
        
        # @ token
        atNode = Node(tokens[0])
        atNode.parent = self.root
        self.root.children.append(atNode)
        
        # ref name token
        refNode = Node(tokens[1])
        refNode.parent = atNode
        atNode.children.append(refNode)
        
        # alias tokens
        if count < 3:
            return
        asNode = Node(tokens[2])
        asNode.parent = atNode
        for i in range(3, count):
            aliasNode = Node(tokens[i])
            aliasNode.parent = asNode
            asNode.children.append(aliasNode)
        atNode.children.append(asNode)
            
    def prettyPrint(self, node: Node, newline: str = "\n"):
        print(node.data, end=newline)
        
        for n in node.children:
            self.prettyPrint(n, " ")
            
        if node.parent == self.root:
            print("")
        