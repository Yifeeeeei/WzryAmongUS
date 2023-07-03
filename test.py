from freshBox import FreshList, FreshDict

fl = FreshList(3)
fd = FreshDict(3)

for i in range(5):
    fd[i] = i
    print(fd)
