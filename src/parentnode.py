from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag == None: raise ValueError("parent nodes must have a tag name")
        if self.children == None: raise ValueError("parent nodes must have child nodes")
        
        child_strings = []
        for child in self.children:
            child_strings.append(child.to_html())
        child_string = "".join(child_strings)

        return f"<{self.tag}{self.props_to_html()}>{child_string}</{self.tag}>"

