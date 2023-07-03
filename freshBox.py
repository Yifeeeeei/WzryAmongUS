"""
FreshList is a kind of data structure which has a fixed max size.
It works like a list,
but if the new appended element makes it exceed its max size,
it will delete the oldest element within,
leaving only the most 'fresh' elements.
"""


class FreshList:
    def __init__(self, box_size):
        self.box_size = box_size
        self.box = []

    def __getitem__(self, index):
        return self.box[index]

    def __setitem__(self, index, value):
        self.box[index] = value

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


"""
FreshDict is a kind of data structure which has a fixed max size.
It works like a dict,
but if the new appended element makes it exceed its max size,
it will delete the oldest element within,
leaving only the most 'fresh' elements.
"""


class FreshDict:
    def __init__(self, box_size):
        self.box_size = box_size
        self.box = {}

    def __setitem__(self, key, value):
        if len(self.box) >= self.box_size:
            self.box.pop(list(self.box.keys())[0])
        self.box[key] = value

    def __getitem__(self, key):
        return self.box[key]

    def __len__(self):
        return len(self.box)

    def __repr__(self):
        return str(self.box)

    def __iter__(self):
        return iter(self.box)

    def keys(self):
        return self.box.keys()
