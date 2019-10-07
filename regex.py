# -*- coding:utf-8 -*-
'''
 author: 邵伟洁 Jared Shaw
 Github: JackShaw2333
 from: 计科170112
 No.: 20178000
'''

import nfa
import re


OPS = ['|', '.',  '*', '(', ')']    # 允许的运算符
# | 或
# . 连接
# * 闭包

# EPS = 'eps'

def regex2post(input):
    '''
    使用调度场算法将正规式转换为逆波兰式，
    :param input: str 正规式
    :return: list 正规式的逆波兰式
    '''
    input = re.sub('\s', '', input) # 去除空格、制表符、换行符

    # 调度场算法
    output, ops = [], []
    for ch in input:
        if ch in OPS:
            while len(ops) and ops[-1] != '(' and ch != ')' and OPS.index(ops[-1]) >= OPS.index(ch):
                output.append(ops.pop())
            if ch == ')':
                while ops[-1] != '(':
                    output.append(ops.pop())
                ops.pop()
            else:
                ops.append(ch)
        else:
            output.append(ch)
    while len(ops):
        output.append(ops.pop())

    return output

class Graph:
    '''
    暂时生成的NFA
    '''
    def __init__(self, id, start, end):
        self.id = id
        self.start = start
        self.end = end


def post2nfa(input, eps):
    '''
    将逆波兰式转化为NFA
    :param input: str 正规式的逆波兰式
    :param eps: str “空”的表示符，由用户定义
    :return: NFA 返回生成的NFA
    '''
    VN, VT, S, T = set(), set(), set(), set()
    # start, end = None, None # 指示当前NFA的初始符号和终结符号
    f = {}  # 存储NFA的关系转换图
    graph_stack = []    # 存储当前生成的NFA-Graph的栈
    vn = 0  # 用0开始的自然数表示vn的非终结符
    for ch in input:
        if ch not in OPS:   # 若当前符号不是运算符
            if ch not in VT:    # 若是新的终结符，则加入终结符集
                VT.add(ch)

            # 形成一个子NFA，非终结符vn经过终结符ch后到达非终结符vn+1，并将子NFA入栈
            VN.add(vn)
            f[vn] = {ch: {vn + 1}}
            VN.add(vn + 1)
            # start, end = vn, vn + 1
            graph_stack.append(Graph(ch, vn, vn+1))

            vn += 2

        elif ch == '|': # 若当前符号为|（或）运算符
            t, s = graph_stack.pop(), graph_stack.pop()

            VN.add(vn)
            f[vn] = {eps: {s.start, t.start}}
            VN.add(vn + 1)
            f[s.end], f[t.end] = {eps: {vn + 1}}, {eps: {vn + 1}}
            graph_stack.append(Graph(s.id+'|'+t.id, vn, vn+1))

            vn += 2

        elif ch == '.':
            t, s = graph_stack.pop(), graph_stack.pop()

            # VN.add(vn)
            f[s.end] = {eps: {t.start}}
            graph_stack.append(Graph(s.id+'.'+t.id, s.start, t.end))

        elif ch == '*':
            s = graph_stack.pop()

            VN.add(vn)
            f[vn] = {eps: {s.start, vn+1}}
            f[s.end] = {eps: {s.start, vn+1}}
            VN.add(vn+1)
            graph_stack.append(Graph('('+s.id+')*', vn, vn+1))

            vn += 2

    graph = graph_stack.pop()
    S.add(graph.start)
    T.add(graph.end)
    for vn in VN:
        f.setdefault(vn, {eps: {vn}})
    return nfa.NFA(VN, VT, f, S, T, eps)





if __name__ == '__main__':
    # (a|b)*.a.b.b
    # regex = input('请输入正规式：')
    regex = '(a|b)*.a.b.b'
    # print(regex)
    post = regex2post(regex)
    # print(post)
    nfa = post2nfa(post, 'eps')
    print(nfa.VN)
    print(nfa.VT)
    for k, v in nfa.f.items():
        print(k, v)
    print(nfa.S)
    print(nfa.T)

    '''
    0 {'a': {1}}
2 {'b': {3}}
4 {'eps': {0, 2}}
1 {'eps': {5}}
3 {'eps': {5}}
6 {'eps': {4, 7}}
5 {'eps': {4, 7}}
8 {'a': {9}}
7 {'eps': {8}}
10 {'b': {11}}
9 {'eps': {10}}
12 {'b': {13}}
11 {'eps': {12}}
    '''