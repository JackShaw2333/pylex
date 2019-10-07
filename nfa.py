# -*- coding:utf-8 -*-
'''
 author: 邵伟洁 Jared Shaw
 Github: JackShaw2333
 from: 计科170112
 No.: 20178000
'''
import dfa


class NFA:
    def __init__(self, VN, VT, f, S, T, EPSILON):
        '''
        NFA初始化
        :param VN: set() 终结符号
        :param VT: set() 非终结符号
        :param f: dict() 映射函数
        :param S: set() 初始符号集
        :param T: set() 终止符号集
        :param EPSILON: --- 空的符号表示
        '''

        self.VN = VN
        self.VT = VT
        self.f = f
        self.S = S
        self.T = T
        self.EPSILON = EPSILON
        self.C = [] # list() 记录了转化后的DFA的非终止状态（自然数）和NFA的非终止状态集的子集的映射关系


    def to_dfa(self):
        '''
        将NFA转化为DFA
        :return: dfa.DFA对象
        设置DFA的非终结符为自然数
        DFA的终结符号集与NFA相同
        '''
        DFA_index = 0   # 设置DFA的非终结符为自然数
        # DFA_VN = dict()  # DFA的非终结符号集
        DFA_f = dict()  # DFA的映射函数
        DFA_S = self.epsilon_closure(self.S)    # DFA的初始状态
        DFA_T = []   # DFA的终止状态集

        self.C.append(DFA_S)
        while True:
            T = self.C[DFA_index]
            # DFA_VN[DFA_index] = T
            if not T.isdisjoint(self.T):    # 如果T包含NFA终止状态集的元素，则T为DFA的终止状态
                DFA_T.append(DFA_index)

            DFA_f[DFA_index] = dict()

            for ch in self.VT:
                U = self.epsilon_closure(self.move(T, ch))
                if len(U) == 0: # 如果为空集，处理下一个终结符
                    continue
                if U not in self.C:
                    self.C.append(U)
                self.set_dfa_f(DFA_index, ch, U, DFA_f) # 利用当前self.C的数据，将NFA非终止状态的子集映射到表示非终止状态的自然数

            if DFA_index + 1 == len(self.C):    # 若没有新的DFA状态可扩展，则转化过程结束
                break

            DFA_index += 1  # 准备进行下一个DFA状态的转化


        new_dfa = dfa.DFA([i for i in range(len(self.C))], self.VT, DFA_f, 0, DFA_T)  # 生成的新DFA
        return new_dfa



    def epsilon_closure(self, I):
        '''
        返回I的ε闭包
        :param I: set() 非终结状态集的一个子集
        :return: set() I的ε闭包
        '''
        res = I
        q = list(I)

        while len(q):
            front = q.pop()
            t = self.f[front].get(self.EPSILON, set())  # front通过一条ε弧到达的状态集
            if len(t):
                for i in t:
                    if i not in res:
                        q.append(i)
                res = res | t

        return res


    def move(self, T, ch):
        '''
        move(T, ch)函数
        :param T: set() 非终结符集合的一个子集
        :param ch: 单个字符 某个终结符
        :return: set() move(T, ch)
        '''
        res = set()
        T = self.epsilon_closure(T)
        for i in T:
            res = res | self.f[i].get(ch, set())
        return res


    def set_dfa_f(self, vn, vt, subset, f):
        '''
        利用当前self.C的数据，将NFA非终止状态的子集映射到表示非终止状态的自然数
        :param vn: 自然数 DFA的非终结符
        :param vt: str 终结符
        :param subset: set() DFA的非终结符所对应在NFA中的非终结符集
        :param f: dict() 描述DFA图的数据结构
        '''
        for i in range(len(self.C)-1, -1, -1):
            if self.C[i] == subset:
                f[vn][vt] = i



if __name__ == '__main__':


    # EPS = 'eps'
    # VN = {'i','1', '2', '3', '4', '5', '6', 'f'}
    #
    # VT = {'a', 'b'}
    #
    # f = {
    #     'i': {EPS: {'1'}},
    #     '1': {'a': {'1'}, 'b': {'1'}, EPS: {'2'}},
    #     '2': {'a': {'3'}, 'b': {'4'}},
    #     '3': {'a': {'5'}},
    #     '4': {'b': {'5'}},
    #     '5': {EPS: {'6'}},
    #     '6': {'a': {'6'}, 'b': {'6'}, EPS: {'f'}},
    #     'f': {}
    # }
    # # print([f.keys()])
    # # for i in f.keys():
    # #     print(i)
    # S = {'i'}
    # T = {'f'}
    #
    # nfa = NFA(VN, VT, f, S, T, EPS)
    # new_dfa = nfa.to_dfa()


    VN = {0, 1, 2, 3, 4, 5, 6}
    VT = {'a', 'b'}
    f = {
        0: {'a': 5, 'b': 2},
        1: {'a': 6, 'b': 2},
        2: {'a': 0, 'b': 4},
        3: {'a': 3, 'b': 5},
        4: {'a': 6, 'b': 2},
        5: {'a': 3, 'b': 0},
        6: {'a': 3, 'b': 1},
    }
    S = 0
    T = {4, 5, 6}


    new_dfa = dfa.DFA(VN, VT, f, S, T)

    new_dfa.minimize()

    print(new_dfa.VN)
    print(new_dfa.VT)
    for k, v in new_dfa.f.items():
        print(k, v)
    print(new_dfa.S)
    print(new_dfa.T)


