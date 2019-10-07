# -*- coding:utf-8 -*-
'''
 author: 邵伟洁 Jared Shaw
 Github: JackShaw2333
 from: 计科170112
 No.: 20178000
'''

class DFA:
    def __init__(self, VN, VT, f, S, T):
        '''
        DFA初始化
        :param VN:  非终结符号集，必须为自然数组成的集合
        :param VT:  终结符号集
        :param f:   dict()  映射
        :param S:   初始状态，必须是自然数0
        :param T:   终结状态集
        :param EPSILON:     空标识符
        '''
        self.VN = set(VN)
        self.VT = set(VT)
        self.f = f
        self.S = S
        self.T = set(T)
        # self.EPSILON = EPSILON



    def minimize(self):
        '''
        DFA最小化
        :return:
        '''
        initial_partition = [self.T, self.VN - self.T]  # 初始划分
        final_partition, repre2block = self.pp(initial_partition)   # 调用一次pp过程
        while final_partition != initial_partition: # 若划分没有变化
            initial_partition = final_partition
            final_partition, repre2block = self.pp(initial_partition)   # 继续调用pp过程
        self.merge(final_partition, repre2block)    # 合并同一划分内的非终结符
        self.remove_unsearchable_vn()   # 去除不可达的非终结符



    def remove_unsearchable_vn(self):
        '''
        去除不可达的非终结符
        :return:
        '''
        VN = [self.S]   # 不含不可达状态的非终止状态集
        index = 0   # while循环中序号小于等于index的状态是已标记状态
        f = dict()
        while True:
            vn = VN[index]
            f[vn] = dict()
            for vt in self.VT:  # 对于终止符号集中的每个符号vt
                vn_ = self.f[vn].get(vt, None)
                if vn_ not in VN and vn_ is not None:
                    VN.append(vn_)
                f[vn][vt] = vn_

            if index + 1 == len(VN):
                break

            index += 1

        self.VN = set(VN)
        self.f = f
        self.T = self.T & self.VN



    def pp(self, partition):
        '''
        pp过程
        :param partition: list(set(), set(){, set()})  初始的划分
        :return: list(set(), set(){, set()})   调用pp过程的划分
        '''
        partition_ = []
        vn2block_partition = {}   # 存储当前所有非终止符号所在的block在partition中的索引号，即{非终结符: 该非终结符所在block在partition中的索引值}

        for i_block in range(len(partition)):
            for vn in partition[i_block]:
                vn2block_partition[vn] = i_block

        cur_i_block_partition_ = 0

        vn_vt2block_partition = {}  # 存储vn遇到vt转移到的非终结符所在的block，即{vn: {vt: vn_在partition中所在的block的索引值}}
        vn2block_partition_ = {}    # vn在partition_中所在block的索引值
        for vn in self.VN:
            # vn_vt2block_partition[vn] = {}
            t_dict = {vn:{}}
            for vt in self.VT:
                vn_ = self.f[vn].get(vt, None)  # vn_为vn遇到vt到达的状态
                if vn_ is not None:
                    # i_block_partition = vn2block_partition[vn_]
                    # vn_vt2block_partition[vn][vt] = i_block_partition
                    t_dict[vn][vt] = vn2block_partition[vn_]  # vn遇到vt到达的状态的block在partition中的索引值

            has_equ_vn = False  # 标志当前vn是否与之前出现过的vn在同一block
            is_vn_terminated = True if vn in self.T else False
            for k, v in vn_vt2block_partition.items():
                is_k_terminated = True if k in self.T else False
                if v == t_dict[vn] and is_k_terminated == is_vn_terminated:
                    i_block_partition_ = vn2block_partition_[k]
                    partition_[i_block_partition_].add(vn)
                    has_equ_vn = True
                    break

            if not has_equ_vn:
                vn_vt2block_partition[vn] = t_dict[vn]
                partition_.append({vn})
                vn2block_partition_[vn] = cur_i_block_partition_
                cur_i_block_partition_ += 1

        return partition_, vn2block_partition_



    def merge(self, partition, repre2block):
        '''
        合并非终结符，只保留代表非终结符
        :param partition: list(set(), set(){, set()}) 需要进行合并的划分
        :param repre2block: dict() {代表非终结符: 相应block在划分partition中的索引}
        :return:
        '''
        new_VN = set()
        for k in repre2block.keys():
            new_VN.add(k)
        new_T = self.T & new_VN
        # redundant_VN = self.VN - VN

        block2repre = {}    # {block索引值: 该block的代表vn}
        for k, v in repre2block.items():
            block2repre[v] = k

        # redundant_vn2repre = {} # {多余vn: 多余vn的代表vn}
        vn2repre = {}
        for i_block in range(len(partition)):
            block = partition[i_block]
            repre = block2repre[i_block]
            # redundant_vns = block.remove(repre)
            # for redundant_vn in redundant_vns:
            #     redundant_vn2repre[redundant_vn] = repre
            for vn in block:
                vn2repre[vn] = repre

        new_f = {}
        for repre in new_VN:
            new_f[repre] = {}
            for ch in self.VT:
                vn = self.f[repre].get(ch, None)
                if vn is not None:
                    vn_repre = vn2repre[vn]
                    new_f[repre][ch] = vn_repre

        self.VN = new_VN
        self.f = new_f
        self.T = new_T

# if __name__ == '__main__':
#
#     VN = {0, 1, 2, 3, 4}
#     VT = {'a', 'b'}
#     f = {
#         0: {'a': 1, 'b': 2},
#         1: {'a': 1, 'b': 3},
#         2: {'a': 1, 'b': 2},
#         3: {'a': 1, 'b': 4},
#         4: {'a': 1, 'b': 2},
#     }
#     S = 0
#     T = {4}
#
#     new_dfa = DFA(VN, VT, f, S, T)
#
#
#     new_dfa.minimize()
#
#     print(new_dfa.VN)
#     print(new_dfa.VT)
#     for k, v in new_dfa.f.items():
#         print(k, v)
#     print(new_dfa.S)
#     print(new_dfa.T)
#
#
#     import time
#     # LENGTH = 10000000
#     # a = []
#     # r = range(LENGTH)
#     # start = time.time()
#     # for i in range(len(r)):
#     #     pass
#     #     # a.append(i)
#     # end = time.time()
#     # print(end - start)
#     #
#     # # a = set()
#     # start = time.time()
#     # for i in range(LENGTH):
#     #     pass
#     #     # a.add(i)
#     # end = time.time()
#     # print(end - start)





