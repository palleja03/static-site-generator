class HTMLNode:
    def __init__(self, tag = None, value = None, children = [], props = {}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props 

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
    def __eq__(self, other):
        return (self.tag == other.tag and
        self.value == other.value and
        self.children == other.children and
        self.props == other.props
        )

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        for k,v in self.props.items():
            result += f' {k}="{v}"'
        return result
    
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props={}):
        if value is None:
            raise ValueError("LeafNode requires a non-empty value.")
        super().__init__(tag=tag, value=value, children=[], props=props)
    
    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode requires a non-empty value.")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props={}):
        if children is None or children == []:
            raise ValueError("PrentNode requires a non-empty children list.")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("PrentNode requires a non-empty tag to be converted to html.")
        children_html = ""
        for child in self.children:
            children_html =  children_html + child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        