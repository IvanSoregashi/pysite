import unittest

from src.blocknode import block_to_block_type, BlockType
from src.markdown import markdown_to_blocks, markdown_to_html_node
from src.textnode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, \
    split_nodes_image, text_to_textnodes, TextNode, TextType


class TestBlockType(unittest.TestCase):
    def test_block(self):
        blocks_and_types = [
            ("""
1. dfsgkjdksj
2. dfsgfjdkl 3. kgfjmlkdsghlk
3. dkhblkdm ;fbdk;vbm d;fmlvbkdmv;k
4. 4. 4. 4. 4. 4.
5. 
""".strip(),
                BlockType.ORDERED_LIST
             ),
            (
                """1. dfsgkjdksj""".strip(),
                BlockType.ORDERED_LIST
            ),
            (
                """0. dfsgkjdksj""".strip(),
                BlockType.PARAGRAPH
            ),
            (
                """2. dfsgkjdksj""".strip(),
                BlockType.PARAGRAPH
            ),
            ("""
        1. dfsgkjdksj
        2. dfsgfjdkl 3. kgfjmlkdsghlk
        3. dkhblkdm ;fbdk;vbm d;fmlvbkdmv;k
        4. 4. 4. 4. 4. 4.
        6. 
        """.strip(),
             BlockType.PARAGRAPH
             ),
            (
                """# l;bngkmfdl,""".strip(),
                BlockType.HEADING
            ),
            (
                """## l;bngkmfdl,""".strip(),
                BlockType.HEADING
            ),
            (
                """### l;bngkmfdl,""".strip(),
                BlockType.HEADING
            ),
            (
                """#### l;bngkmfdl,""".strip(),
                BlockType.HEADING
            ),
            (
                """##### l;bngkmfdl,""".strip(),
                BlockType.HEADING
            ),
            (
                """###### l;bngkmfdl,""".strip(),
                BlockType.HEADING
            ),
            (
                """######l;bngkmfdl,""".strip(),
                BlockType.PARAGRAPH
            ),
            ("""
- dfsgkjdksj
- dfsgfjdkl 3. kgfjmlkdsghlk
- dkhblkdm ;fbdk;vbm d;fmlvbkdmv;k
- 4. 4. 4. 4. 4.
- 1
        """.strip(),
             BlockType.UNORDERED_LIST
             ),
            ("""
- dfsgkjdksj
- dfsgfjdkl 3. kgfjmlkdsghlk
- dkhblkdm ;fbdk;vbm d;fmlvbkdmv;k
- 4. 4. 4. 4. 4.
- 
        """.strip(),
             BlockType.UNORDERED_LIST
             ),
            ("""
        - dfsgkjdksj
        """.strip(),
             BlockType.UNORDERED_LIST
             ),
            ("""
        -dfsgkjdksj
        """.strip(),
             BlockType.PARAGRAPH
             ),
            ("""
```
print("hello world")
```
        """.strip(),
             BlockType.CODE
             ),
            ("""
```python
print("hello world")
```
        """.strip(),
             BlockType.CODE
             ),
            ("""
>ikdfjmhbikjmfdgbik
        """.strip(),
             BlockType.QUOTE
             ),
            ("""
> ![note] fbd,
        """.strip(),
             BlockType.QUOTE
             ),
            ("""
> ![note] fbd,
> ikdfjmhbikjmfdgbik
>ikdfjmhbikjmfdgbik

        """.strip(),
             BlockType.QUOTE
             ),
        ]

        print()
        for i, (block, expected_type) in enumerate(blocks_and_types):
            print(f"{i}. {expected_type=}, \n{block}\n\t-------------------------")
            self.assertEqual(expected_type, block_to_block_type(block))

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quoteblock(self):
        md = """
> This is **bolded** paragraph
> text in a blockquote
> tag here
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is <b>bolded</b> paragraph\ntext in a blockquote\ntag here</blockquote></div>",
        )

    def test_quoteblock2(self):
        md = """
> This is **bolded** paragraph
>text in a blockquote
>tag here
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is <b>bolded</b> paragraph\ntext in a blockquote\ntag here</blockquote></div>",
        )

    def test_ul(self):
        md = """
- This is **bolded** paragraph
- text in a blockquote
- tag here
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is <b>bolded</b> paragraph</li><li>text in a blockquote</li><li>tag here</li></ul></div>",
        )

    def test_bad_ul(self):
        md = """
- This is **bolded** paragraph
-text in a blockquote
- tag here
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>- This is <b>bolded</b> paragraph -text in a blockquote - tag here</p></div>",
        )

    def test_ol(self):
        md = """
1. This is **bolded** paragraph
2. text in a blockquote
3. tag here
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is <b>bolded</b> paragraph</li><li>text in a blockquote</li><li>tag here</li></ol></div>",
        )

    def test_bad_ol(self):
        md = """
1. This is **bolded** paragraph
2. text in a blockquote
4. tag here
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>1. This is <b>bolded</b> paragraph 2. text in a blockquote 4. tag here</p></div>",
        )

    def test_h_ol(self):
        md = """
### This is an ordered list        

1. This is **bolded** paragraph
2. text in a blockquote
3. tag here
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is an ordered list</h3><ol><li>This is <b>bolded</b> paragraph</li><li>text in a blockquote</li><li>tag here</li></ol></div>",
        )

    def test_h_ol_p(self):
        md = """


## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>My favorite characters (in order)</h2><ol><li>Gandalf</li><li>Bilbo</li><li>Sam</li><li>Glorfindel</li><li>Galadriel</li><li>Elrond</li><li>Thorin</li><li>Sauron</li><li>Aragorn</li></ol><p>Here's what <code>elflang</code> looks like (the perfect coding language):</p></div>",
        )