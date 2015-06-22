# -*- coding: utf-8 -*-


if __name__ == '__main__':
    L1 = [[1,2,3], [1,2,3], [3,2,1], [2,3,1]]
    L2 = [[1,2,3], [2,3,4]]
    set([tuple(sorted(l)) for l in L1])