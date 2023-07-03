"""
FreshBox is a kind of data structure which has a fixed max size.
It works like a list,
but if the new appended element makes it exceed its max size,
it will delete the oldest element within,
leaving only the most 'fresh' elements.
"""


class FreshBox:
    def __init__(self, box_size):
        self.box_size = box_size
        self.box = []

    def __getitem__(self, index):
        return self.box[index]

    def __len__(self):
        return len(self.box)

    def __repr__(self):
        return str(self.box)

    def __iter__(self):
        return iter(self.box)

    def __reversed__(self):
        return reversed(self.box)

    def append(self, new_ele):
        if len(self.box) >= self.box_size:
            self.box.pop(0)
        self.box.append(new_ele)

    def pop(self):
        return self.box.pop()

    def clear(self):
        self.box.clear()
