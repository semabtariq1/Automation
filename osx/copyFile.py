from distutils.dir_util import copy_tree


class CopyFile:
    def copy(self, src, dest):
        copy_tree(src, dest)