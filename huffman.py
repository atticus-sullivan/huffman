# Copyright (c) 2024, Lukas Heindl
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
from queue import PriorityQueue
import graphviz as dot

identifier = 0

class TreeElem():
    cnt = 0
    def __init__(self, char:str, num:int, left=None, right=None):
        global identifier
        self.char = char
        self.num = num
        self.left = left
        self.right = right
        self.id = identifier
        identifier += 1

    @classmethod
    def combine(cls, t1, t2):
        return TreeElem("", t1.num + t2.num, t1, t2)
    
    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __str__(self):
        if self.left is not None and self.right is not None:
            return "{char:" + self.char + "num:" + str(self.num) + "left:" + str(self.left) + "right:" + str(self.right) + "}"
        elif self.left is not None:
            return "{char:" + self.char + "num:" + str(self.num) + "left:" + str(self.left) + "right:" +"}"
        elif self.right is not None:
            return "{char:" + self.char + "num:" + str(self.num) + "left:" + "right:" + str(self.right) + "}"
        else:
            return "{char:" + self.char + "num:" + str(self.num) + "left:" "right:" + "}"
    def __repr__(self):
        return self.__str__()

    def toDot(self, acc:dot.Digraph=None):
        if acc is None:
            acc = dot.Digraph('g', filename='huffman.dot', node_attr={'shape': 'record', 'height': '.1'})

        if self.char != "":
            acc.node(str(id(self)), label=(f'"{self.char}"'))
        else:
            acc.node(str(id(self)), label=(f'{self.num}/{TreeElem.cnt}'))
        if self.left is not None:
            self.left.toDot(acc)
            acc.edge(str(id(self)), str(id(self.left)), label="0")
        if self.right is not None:
            self.right.toDot(acc)
            acc.edge(str(id(self)), str(id(self.right)), label="1")

        return acc

    def lookup(self, c:str, acc:str=""):
        if self.char == c:
            return (True,acc)
        
        if self.left is not None:
            r = self.left.lookup(c, acc + "0")
            if r[0]:
                return r
        if self.right is not None:
            r = self.right.lookup(c, acc + "1")
            if r[0]:
                return r
        return (False,)

class Huffman():
    def __init__(self, init:str):
        self.input = init
        self._update()

    def update(self, n:str):
        self.input += n
        self._update()

    def _update(self):
        q = PriorityQueue()
        TreeElem.cnt = len(self.input)
        init = {x:self.input.count(x) for x in self.input}

        for k,v in init.items():
            q.put((v, TreeElem(k, v)))

        while not q.empty():
            x1 = q.get()
            if q.empty():
                # tree is built
                self.head = x1[1]
                break
            x2 = q.get()
            n = TreeElem.combine(x1[1], x2[1])
            q.put((n.num, n))

        self.head.toDot().render()
        print("Updated")

    def lookup(self, i:str):
        o = ""
        for c in i:
            r = self.head.lookup(c)
            if r[0]:
                o += r[1]
            else:
                print("'%s' not known to the tree, skipping" % c)
        return o

parser = argparse.ArgumentParser()
parser.add_argument("initial", help="Initial string from which the huffman tree is built")

args = parser.parse_args()

h = Huffman(args.initial)

print("'u <string>' to append to the string from which the huffman tree is generated\n'l <string>' to get the string encoded with the current huffman tree\n")
while True:
    print("u(pdate)/l(ookup)/q(uit)", end=": ")
    i = input()
    if i.startswith("u "):
        h.update(i[2:])
    elif i.startswith("l "):
        print(h.lookup(i[2:]))
    elif i.startswith("q"):
        break
    else:
        print("Wrong selection")
        continue
