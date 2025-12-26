import sys
sys.path.append("src")
from analysis.iparse_vq import IParser

iparse = IParser("en_label_gpt2_medium_cat256")
# dev_treebank = iparse.load_dev()

tree, code = iparse.parse_sentence("I knocked the man off his .")

# type(t) = nltk.tree.tree.Tree
tree.pretty_print()