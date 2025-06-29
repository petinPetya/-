import shutil
import sys

d: dict = {}
texts: list = [None] * 361
num: int = 0
stati: dict = dict()
prev: str = ""

with open("ukrf.txt", encoding='utf-8') as file:
    for i in file:
        cur: str = i.split()
        #print(cur)
        if cur and cur[0] == "Статья":
            stati[cur[1]] = num
            #print(int(cur[1].strip('.')))
            d[cur[0] + " " + cur[1]] = " ".join(cur[2:])
            texts[num] = prev
            prev = ""
            num += 1
        else:
            prev = prev + str(i)

def get_full(s: str):
    return texts[stati[s] + 1]

print(stati)
