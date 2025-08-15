from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


# def markdown_to_blocks(markdown):
#     return [b.strip() for b in markdown.split("\n\n") if len(b.strip()) > 0]

# def is_markdown_quote(block):
#     for line in block.splitlines():
#         if not line.startswith("> "):
#             return False
#     return True

# def is_markdown_unordered_list(block):
#     for line in block.splitlines():
#         if not (line.startswith("- ") or line.startswith("* ")):
#             return False
#     return True

# def is_markdown_ordered_list(block):
#     return all(
#         True if line.startswith(f"{i+1}. ") else False
#         for i, line in enumerate(block.splitlines()) 
#     )

# def block_to_block_type(block):
#     """Determine the type of a markdown block."""
#     heading_re = re.compile(r"^#{1,6} .*$")
#     if re.match(heading_re, block):
#         return BlockType.HEADING
#     elif block.startswith("```") and block.endswith("```"):
#         return BlockType.CODE
#     elif is_markdown_quote(block):
#         return BlockType.QUOTE
#     elif is_markdown_unordered_list:
#         return BlockType.UNORDERED_LIST
#     elif is_markdown_ordered_list(block):
#         return BlockType.ORDERED_LIST
#     else:
#         return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH
