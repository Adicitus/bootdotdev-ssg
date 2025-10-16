from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type:TextType):
    new_nodes = []

    for node in old_nodes:
        parts = node.text.split(delimiter)
        
        n = len(parts)
        if n == 1:
            # node is already as granular as we can make it, keeping it.
            new_nodes.append(node)
            continue
        # We found the delimiters in the text, so we have more 
        # than 1 potential text nodes: every 2 part should correspond
        # to a node of text_type.
        for i in range(0, n):
            part = parts[i]
            if part == "": continue
            if i % 2 == 1:
                new_nodes.append(TextNode(part, text_type))
            else:
                new_nodes.append(TextNode(part, node.text_type))
    
    return new_nodes

        