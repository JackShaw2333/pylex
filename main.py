# -*- coding:utf-8 -*-
'''
 author: 邵伟洁 Jared Shaw
 Github: JackShaw2333
 from: 计科170112
 No.: 20178000
'''

from regex import regex2post, post2nfa

if __name__ == '__main__':
    # regex = '(a|b)*.a.b.b'
    regex = input("请输入正规式（“|”为“或”，“.”为“连接”，“*”为“闭包”）：")
    # eps = input("请输入“空”的标识符：")
    eps = 'eps'
    post = regex2post(regex)
    mynfa = post2nfa(post, eps)
    mydfa = mynfa.to_dfa()
    mydfa.minimize()

    print(mydfa.VN) # DFA的非终结符集
    print(mydfa.VT) # DFA的终结符集
    # for k, v in mydfa.f.items():
    #     print(k, v)
    print(mydfa.f)  # 描述DFA图非终结符转换关系的数据结构
    print(mydfa.S)  # DFA的初始状态
    print(mydfa.T)  # DFA的终止状态集