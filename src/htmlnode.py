class HTMLNode:
    def __init__(self, tag = None, value = None, children = [], props = {}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props 

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
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