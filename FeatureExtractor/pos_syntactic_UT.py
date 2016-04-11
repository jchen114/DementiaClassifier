import unittest
import parser as psr
import pos_syntactic as ps


class Test_POS_Syntactic(unittest.TestCase):

    def test_tree_height(self):
        # Building test tree
        root_node = ps.tree_node('Blah')
        ch_1 = ps.tree_node('Blah')
        ch_2 = ps.tree_node('Blah')
        ch_2_1 = ps.tree_node('Blah')
        ch_2_2 = ps.tree_node('Blah')
        ch_2_2_1 = ps.tree_node('Blah')

        ch_2_2.addChild(ch_2_2_1)
        ch_2.addChild(ch_2_1)
        ch_2.addChild(ch_2_2)
        root_node.addChild(ch_1)
        root_node.addChild(ch_2)
        self.assertEqual(ps.get_height_of_tree(root_node), 4)

    def test_build_parse_tree(self):
        trees = psr.get_parse_tree("My friends and I went to New York City for a weekend.")
        node = ps.build_tree(trees[0])

if __name__ == '__main__':
    unittest.main()