# -*- coding: UTF-8 -*-
'''
GF(2^8)域，共有2^8个元素
表示为字节：b7b6b5b4b3b2b1b0 (8位二进制)
也是多项式：b7x^7 + b6x^6 + b5x^5 + b4x^4 + b3x^3 + b2x^2 + b1x + b0
本原多项式：x^8 + x^4 + x^3 + x + 1 即 100011101
'''
class GF():
    def __init__(self):
        self.modulus=(1 << 8) + 0b11011

    # 域中多项式加减等于多项式按位异或
    def poly_add(self, a, b):
        return a^b

    def poly_sub(self, a, b):
        return self.poly_add(a,b)

    def poly_mod(self, a):
        if a<(1 << 8): # 如果 a<2^8，模为它本身
            return a
        else:
            len_a=len(bin(a).replace('0b',''))
            while len_a>8:
                # 将模多项式与a高位对齐，然后异或
                m=self.modulus << (len_a-9)
                a ^= m
                len_a = len(bin(a).replace('0b', ''))
            return a

    def poly_mul(self, a, b):
        r=0
        for i in range(8):
            r ^= ((a<<i)*((b>>i)&0x1))
        return self.poly_mod(r)

    def poly_div(self, a, b):
        r0=a
        qn=0
        bitcnt=len(bin(a))-len(bin(b))
        while bitcnt>0:
            qn |= (1<<bitcnt)
            r0 ^= (b<<bitcnt)
            bitcnt=len(bin(r0))-len(bin(b))
        return self.poly_mod(qn)

    '''
    贝祖(Bezout)等式
        gcd(a,b) = xa + yb
    矩阵行初等变换求解贝祖(Bezout)等式
        将 a,b 写成如下矩阵，后面是个单位矩阵
        [
         [a, 1, 0],
         [b, 0, 1]
        ]
        将矩阵进行行初等变换，直到 a=0 (或 b=0)，则 b (或 a) 为 gcd(a,b)
        [
         [0, *, *],
         [gcd(a,b), x, y]
        ]
    '''
    # 乘法逆元
    def poly_mulinv(self, a):
        A=[self.modulus,1,0]
        B=[a,0,1]
        while A[0]!=0 and B[0]!=0: # a 或 b 为0都会跳出循环
            # 如果a的二进制长大于b，则a行变换，否则b行变换
            if len(bin(A[0]))>=len(bin(B[0])):
                bitcnt=len(bin(A[0]))-len(bin(B[0]))
                for i in range(3):
                    if i==0:
                        b = (B[i]<<bitcnt) # 对于a,b直接二进制左移
                    else:
                        b = B[i] * (1<<bitcnt) # 对于后面矩阵，乘x^k
                    A[i] ^= b # 行变换中加减为异或（GF域中加减）
            else:
                bitcnt = len(bin(B[0])) - len(bin(A[0]))
                for i in range(3):
                    if i==0:
                        a = (A[i]<<bitcnt)
                    else:
                        a = A[i] * (1<<bitcnt)
                    B[i] ^=a
        if A[0]==0:
            return self.poly_mod(B[-1])
        if B[0]==0:
            return self.poly_mod(A[-1])