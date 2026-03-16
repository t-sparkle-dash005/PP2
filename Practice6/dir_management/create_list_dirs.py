import os
from zipfile import Path

doc = "bsubdir"
parent_doc = "D:\\PP2\\Practice6\\dir_management"
path = os.path.join(parent_doc, doc)
#os.mkdir(path)

newdir = "dirdir"
nd2 = "dirdirdir"
parent_dir = "D:\\PP2\\Practice6\\dir_management\\bsubdir"
#os.makedirs(os.path.join(path, newdir, nd2))

pathlist = "D:\\PP2\\Practice6"
content = os.listdir(pathlist)
#print(content)

print(os.getcwd())
os.chdir("D:\\PP2\\Practice6\\dir_management")
print(os.getcwd())