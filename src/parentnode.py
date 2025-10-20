from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)


    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        elif self.children is None:
            raise ValueError("All parent nodes must have a children")

        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"


    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
