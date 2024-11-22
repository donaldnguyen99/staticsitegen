class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        attr = ""
        if self.props:
            for k in self.props:
                attr += f' {k}="{self.props[k]}"'
        return attr
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        prop_text = self.props_to_html()
        return f"<{self.tag}{prop_text}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        if children is None:
            raise ValueError
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag required")
        if self.children is None:
            raise ValueError("List of HTMLNode children required")
        
        html = f"<{self.tag}>"

        child: HTMLNode
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html
        