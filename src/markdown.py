from blocks_markdown import BlockType, block_to_block_type, markdown_to_blocks
from inline_markdown import text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


def text_to_children(text):
    children = []
    for node in text_to_textnodes(text):
        children.append(text_node_to_html_node(node))
    return children


def markdown_to_html_node(markdown):
    children_nodes = []
    for block in markdown_to_blocks(markdown):
        match block_to_block_type(block):
            case BlockType.HEADING:
                level = block.count("#")
                title = block[level:].strip()
                children_nodes.append(ParentNode(f"h{level}", text_to_children(title)))
            case BlockType.PARAGRAPH:
                block = block.replace("\n", " ").strip()
                children_nodes.append(ParentNode("p", text_to_children(block)))
            case BlockType.QUOTE:
                block = "\n".join(l.removeprefix('> ') for l in block.splitlines())
                children_nodes.append(ParentNode("blockquote", text_to_children(block)))
            case BlockType.ULIST:
                items = block.splitlines()
                list_items = []
                for item in items:
                    item = item.removeprefix('- ').strip()
                    list_items.append(ParentNode("li", text_to_children(item)))
                children_nodes.append(ParentNode("ul", list_items))
            case BlockType.OLIST:
                items = block.splitlines()
                list_items = []
                for item in items:
                    item = item[2:].strip()
                    list_items.append(ParentNode("li", text_to_children(item)))
                children_nodes.append(ParentNode("ol", list_items))
            case BlockType.CODE:
                block = block.removeprefix('```').removesuffix('```').lstrip()
                children_nodes.append(ParentNode("pre", [text_node_to_html_node(TextNode(block, TextType.CODE))]))
    return ParentNode("div", children_nodes)


def extract_title(markdown):
    for block in markdown_to_blocks(markdown):
        if block_to_block_type(block) == BlockType.HEADING:
            level = block.count("#")
            if level == 1:
                return block[level:].strip()
    raise ValueError("No level 1 heading found in the markdown content.")
