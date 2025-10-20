

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None: return ""

        attrs = []
        for k in sorted(self.props.keys()):
            attrs.append(f" {k}=\"{self.props[k]}\"")
        
        return "".join(attrs)

    def __repr__(self):
        return f"{type(self).__name__}(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)
    
    def to_html(self):
        if self.value == None: raise ValueError("Leaf nodes must have a value.")
        if self.tag == None: return str(self.value)

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def find_tag(self, tag:str, limit=-1, nodes_found=None):

        # Workaround because python keeps using the same list object if [] is specified as the default value:
        if nodes_found == None: nodes_found = []

        if self.tag == tag:
            nodes_found.append(self)

        for child in self.children:
            if limit > 0 and limit <= len(nodes_found):
                return nodes_found

            if isinstance(child, ParentNode):
                child.find_tag(tag, limit, nodes_found)
                continue
            
            if child.tag == tag:
                nodes_found.append(child)
        
        return nodes_found

    def to_html(self):
        if self.tag == None: raise ValueError("parent nodes must have a tag name")
        if self.children == None: raise ValueError("parent nodes must have child nodes")
        
        child_strings = []
        for child in self.children:
            child_strings.append(child.to_html())
        child_string = "".join(child_strings)

        return f"<{self.tag}{self.props_to_html()}>{child_string}</{self.tag}>"
