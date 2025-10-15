from textnode import TextNode, TextType

def main():
    node = TextNode(
        "This is some anchor text",
        TextType.LINK,
        "http://0.0.0.0:8888"
    )
    print(node)

if __name__ == "__main__":
    main()
