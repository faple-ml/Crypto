# -*- coding: UTF-8 -*-
'''
引用文件如果报错，需要从最外层python路径开始引用，比如
.GF_field 报错，则改为 AES.GF_field
'''
from .GF_field import GF

class AES():
    def __init__(self):
        self.gf=GF()
        self.S=None
        self.inv_S=None
        self.Rcon = [0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000, 0x20000000, 0x40000000, 0x80000000,0x1b000000, 0x36000000]

    def construct_SBox(self):
        S=[]
        # 初始化S盒
        for i in range(16):
            s=[]
            for j in range(16):
                a=((i<<4)&0xf0)+(j&0xf)
                # 映射字节为GF域中的逆
                a=self.gf.poly_mulinv(a)
                c=0b1100011
                r=0
                # 每个字节做位变换
                for k in range(8):
                    r+=((((a>>k)&0x1)^(a>>((k+4)%8)&0x1)^(a>>((k+5)%8)&0x1)^(a>>((k+6)%8)&0x1)^(a>>((k+7)%8)&0x1)^((c>>k)&0x1))<<k)
                s.append(r)
            S.append(s)
        self.S=S

    def construct_inv_SBox(self):
        inv_S=[]
        # 初始化逆S盒
        for i in range(16):
            s=[]
            for j in range(16):
                a=((i<<4)&0xf0)+(j&0xf)
                c=0b101
                r=0
                # 每个字节做位变换
                for k in range(8):
                    r+=(((a>>((k+2)%8)&0x1)^(a>>((k+5)%8)&0x1)^(a>>((k+7)%8)&0x1)^((c>>k)&0x1))<<k)
                # 映射字节为GF域中的逆
                a = self.gf.poly_mulinv(r)
                s.append(a)
            inv_S.append(s)
        self.inv_S=inv_S

    def func_T(self, Ki,r):
        # 字循环
        k=Ki.pop(0)
        Ki.append(k)
        # 字节代换
        for i in range(4):
            k=Ki[i]
            column = k & 0xf
            row = (k >> 4) & 0xf
            Ki[i]=self.S[row][column]
        # 轮常量异或
        for i in range(4):
            ron=(self.Rcon[r]>>(8*i))&0xff
            Ki[-(i+1)] ^= ron
        return Ki

    # 密钥扩展
    def ExtendKey(self, K):
        for i in range(4,44):
            if i%4==0:
                r=(i//4)-1
                Ki=self.func_T([K[0][i-1],K[1][i-1],K[2][i-1],K[3][i-1]],r)
                for j in range(4):
                    K[j].append(K[j][i-4]^Ki[j])
            else:
                for j in range(4):
                    K[j].append(K[j][i-4]^K[j][i-1])
        return K

    # 字节代替
    def SubBytes(self, M):
        for i in range(4):
            for j in range(4):
                a=M[i][j]
                column=a&0xf
                row=(a>>4)&0xf
                M[i][j]=self.S[row][column]
        return M

    # 逆字节代替
    def inv_SubBytes(self, C):
        for i in range(4):
            for j in range(4):
                a=C[i][j]
                column=a&0xf
                row=(a>>4)&0xf
                C[i][j]=self.inv_S[row][column]
        return C

    # 行位移
    def ShiftRows(self, M):
        for i in range(1,4):
            for j in range(i):
                a=M[i].pop(0)
                M[i].append(a)
        return M

    # 逆行位移
    def inv_ShiftRows(self, C):
        for i in range(1, 4):
            for j in range(i):
                a = C[i].pop(-1)
                C[i].insert(0,a)
        return C

    # 列混淆
    def MixColumns(self, M):
        m=[]
        for j in range(4):
            m0=self.gf.poly_mul(2,M[0][j])^self.gf.poly_mul(3,M[1][j])^M[2][j]^M[3][j]
            m1=M[0][j]^self.gf.poly_mul(2,M[1][j])^self.gf.poly_mul(3,M[2][j])^M[3][j]
            m2=M[0][j]^M[1][j]^self.gf.poly_mul(2,M[2][j])^self.gf.poly_mul(3,M[3][j])
            m3=self.gf.poly_mul(3,M[0][j])^M[1][j]^M[2][j]^self.gf.poly_mul(2,M[3][j])
            m+=[m0,m1,m2,m3]
        MC=[]
        for i in range(4):
            MC.append([m[i],m[i+4],m[i+8],m[i+12]])
        return MC

    # 逆列混淆
    def inv_MixColumns(self,C):
        c=[]
        for j in range(4):
            c0=self.gf.poly_mul(0xe,C[0][j])^self.gf.poly_mul(0xb,C[1][j])^self.gf.poly_mul(0xd,C[2][j])^self.gf.poly_mul(0x9,C[3][j])
            c1=self.gf.poly_mul(0x9,C[0][j])^self.gf.poly_mul(0xe,C[1][j])^self.gf.poly_mul(0xb,C[2][j])^self.gf.poly_mul(0xd,C[3][j])
            c2=self.gf.poly_mul(0xd,C[0][j])^self.gf.poly_mul(0x9,C[1][j])^self.gf.poly_mul(0xe,C[2][j])^self.gf.poly_mul(0xb,C[3][j])
            c3=self.gf.poly_mul(0xb,C[0][j])^self.gf.poly_mul(0xd,C[1][j])^self.gf.poly_mul(0x9,C[2][j])^self.gf.poly_mul(0xe,C[3][j])
            c+=[c0,c1,c2,c3]
        CM=[]
        for i in range(4):
            CM.append([c[i],c[i+4],c[i+8],c[i+12]])
        return CM

    # 轮密钥加
    def AddRoundKey(self, M, K):
        for j in range(4):
            for i in range(4):
                M[i][j] ^= K[i][j]
        return M

    def get_keys(self, K, m):
        Km=[]
        for j in range(4):
            k=[]
            for i in range(m,m+4):
                k.append(K[j][i])
            Km.append(k)
        return Km

    # 128位明文加密
    def aes_encryption(self, M, K, round):
        self.construct_SBox()
        K=self.ExtendKey(K)
        M=self.AddRoundKey(M,self.get_keys(K,0))
        for i in range(round):
            M=self.SubBytes(M)
            M=self.ShiftRows(M)
            if i<round-1:
                M=self.MixColumns(M)
            M=self.AddRoundKey(M,self.get_keys(K,(i+1)*4))
        return M

    # 128位密文解密
    def aes_decryption(self, C, K, round):
        self.construct_inv_SBox()
        K = self.ExtendKey(K)
        C=self.AddRoundKey(C,self.get_keys(K,40))
        for i in range(round):
            C=self.inv_ShiftRows(C)
            C=self.inv_SubBytes(C)
            C=self.AddRoundKey(C,self.get_keys(K,40-((i+1)*4)))
            if i<round-1:
                C=self.inv_MixColumns(C)
        return C

if __name__ == '__main__':
    aes=AES()

    # 处理明文
    M="32 43 f6 a8 88 5a 30 8d 31 31 98 a2 e0 37 07 34"
    tmpM=[int(x,16) for x in M.split(" ")]
    M=[]
    for i in range(4):
        M.append([tmpM[i],tmpM[4+i],tmpM[8+i],tmpM[12+i]])

    # 处理密文
    C = "39 25 84 1d 02 dc 09 fb dc 11 85 97 19 6a 0b 32"
    tmpC = [int(x, 16) for x in C.split(" ")]
    C = []
    for i in range(4):
        C.append([tmpC[i], tmpC[4 + i], tmpC[8 + i], tmpC[12 + i]])

    # 处理密钥
    K="2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c"
    tmpK=[int(x,16) for x in K.split(" ")]
    K=[]
    for i in range(4):
        K.append([tmpK[i],tmpK[4+i],tmpK[8+i],tmpK[12+i]])

    C=aes.aes_encryption(M,K,10)
    for i in range(4):
        for j in range(4):
            print(hex(C[i][j]),end=' ')
        print()

    M=aes.aes_decryption(C,K,10)
    for i in range(4):
        for j in range(4):
            print(hex(M[i][j]),end=' ')
        print()