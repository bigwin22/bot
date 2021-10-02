import re

a = re.compile(r'[^\s|^\d]*')

m = a.search("21321lkjfdslk")

print(m.group())