# coding=utf-8
#  代码文件：ch07/ch7_5.py

#  一篇文章文本
wordstring = """
    it was the best of times it was the world of times.
    it wss the age of wisdom it was the age of foolishness.
"""

wordstring = wordstring.replace('.', '')

wordlist = wordstring.split()

wordfreq = []

for w in wordlist:
    wordfreq.append(wordlist.count(w))
d = dict(zip(wordlist, wordfreq))

print(d)
