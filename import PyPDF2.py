import shutil
import sys

d: dict = {}

with open("ukrf.txt", encoding='utf-8') as file:
    for i in file:
        cur: str = i.split()
        print(cur)
        if cur and cur[0] == "Статья":
            d[cur[0] + " " + cur[1]] = " ".join(cur[2:])
print(d)