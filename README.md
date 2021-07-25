Needs `pip install graphviz` and graphviz installed (`sudo apt install graphviz`).

Start as `python3 huffman.py "input string"`. The input string will be used to create the huffman code.

The script then goes into an interavtive mode where you can update the input string (only add to the input, not replace it) or encode a string with the current huffman tree (see the prompt).

E.g. (for interactive mode)
- `u abc` to append `abc` to the input string and update the huffman tree
- `e hij` to get the representation of the string `hij` with the current huffman tree

On each update the `huffman.dot.pdf` will be updated, so you can see live the changes in the tree when having this file open (and if yor pdf-viewer updates the view when the souce-pdf changes).
