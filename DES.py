# -*- coding: UTF-8 -*-

class DES:
    def __init__(self):
        self.PC1=[57,49,41,33,25,17,9,1,
        58,50,42,34,26,18,10,2,
        59,51,43,35,27,19,11,3,
        60,52,44,36,63,55,47,39,
        31,23,15,7,62,54,46,38,
        30,22,14,6,61,53,45,37,
        29,21,13,5,28,20,12,4] # 生成子密钥 PC-1 置换
        self.left_move=[1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1] # 每轮循环左移的位数
        self.PC2=[14,17,11,24,1,5,
        3,28,15,6,21,10,
        23,19,12,4,26,8,
        16,7,27,20,13,2,
        41,52,31,37,47,55,
        30,40,51,45,33,48,
        44,49,39,56,34,53,
        46,42,50,36,29,32] # 生成子密钥 PC-2 置换
        # 扩展置换规则，矩阵左右各加一列
        self.left_column=[32,4,8,12,16,20,24,28]
        self.right_column=[5,9,13,17,21,25,29,1]
        self.S=[
            [
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
            ],
            [
               [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
            ],
            [
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
            ],
            [
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
            ],
            [
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
            ],
            [
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
            ],
            [
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
            ],
            [
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
            ]
        ]
        self.P=[16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,
2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25] # P盒置换
        self.IP=[58,50,42,34,26,18,10,2,
        60,52,44,36,28,20,12,4,
        62,54,46,38,30,22,14,6,
        64,56,48,40,32,24,16,8,
        57,49,41,33,25,17, 9,1,
        59,51,43,35,27,19,11,3,
        61,53,45,37,29,21,13,5,
        63,55,47,39,31,23,15,7] # 明文 / 密文置换表
        self.IP1=[40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,
        38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,
        36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,
        34,2,42,10,50,18,58,26,33,1,41, 9,49,17,57,25] # 明文 / 密文逆置换表

    # 生成子密钥，K 为64位二进制
    def generate_subkeys(self, K):
        # 去掉密钥校验位
        kpc1=[]
        for i in self.PC1:
            kpc1.append(K[i-1])
        # 左右分组
        c0=kpc1[0:28]
        d0=kpc1[28:]
        k=[]
        for i in self.left_move:
            # 循环左移
            for j in range(i):
                c=c0.pop(0)
                c0.append(c)
                d=d0.pop(0)
                d0.append(d)
            # 再次置换
            cd=c0+d0
            k0=[]
            for j in self.PC2:
                k0.append(cd[j-1])
            k.append(k0)
            c0=cd[0:28]
            d0=cd[28:]
        return k # 返回16个48位的子密钥

    def func_f(self, R, K):
        left=[]
        right=[]
        for i in range(8):
            left.append(R[self.left_column[i]-1])
            right.append(R[self.right_column[i]-1])
        # 扩展置换 E
        k1, k2 = 0, 5
        for i in range(8):
            R.insert(k1,left[i])
            k1+=6
            R.insert(k2,right[i])
            k2+=6
        for i in range(48):
            R[i]=R[i]^K[i]
        # S盒代替
        rs=[]
        for i in range(8):
            r=R[i*6:(i+1)*6]
            row=int(str(r[0])+str(r[-1]),2)
            column=int(str(r[1])+str(r[2])+str(r[3])+str(r[4]),2)
            o=[]
            for j in bin(self.S[i][row][column]).replace('0b',''):
                o.append(j)
            while len(o)!=4:
                o.insert(0,'0')
            rs+=o
        # P盒置换
        rp=[]
        for i in self.P:
            rp.append(int(rs[i-1]))
        return rp

    # DES 64位明文加密
    def des_encryption(self, M, K):
        # 初始置换
        mip=[]
        for i in self.IP:
            mip.append(M[i-1])
        l0=mip[0:32]
        r0=mip[32:]
        # 16轮加密
        ks=self.generate_subkeys(K)
        for i in range(16):
            l=r0.copy() # 这里要注意，如果写成
            r=[]
            f=self.func_f(r0,ks[i])
            for j in range(32):
                r.append(l0[j]^f[j])
            l0=l
            r0=r
        # 逆置换
        mip1=r0+l0
        C=[]
        for i in self.IP1:
            C.append(mip1[i-1])
        return C

    # DES 明文加密
    def des_encrypt(self, M, K):
        print("DES encryption start.")
        C=[]
        for i in range(len(M)):
            c=self.des_encryption(M[i],K)
            s=""
            for j in c:
                s+=str(j)
            C.append(hex(int(s,2)).replace('0x',''))
        return C

    # DES 64位密文解密
    def des_decryption(self, C, K):
        # 初始置换
        cip = []
        for i in self.IP:
            cip.append(C[i - 1])
        l0 = cip[0:32]
        r0 = cip[32:]
        # 16轮解密
        ks = self.generate_subkeys(K)
        for i in range(16):
            l = r0.copy()
            r = []
            f = self.func_f(r0, ks[-(i+1)])
            for j in range(32):
                r.append(l0[j] ^ f[j])
            l0 = l
            r0 = r
        # 逆置换
        cip1 = r0+l0
        M = []
        for i in self.IP1:
            M.append(cip1[i - 1])
        return M

    # DES 密文解密
    def des_decrypt(self, C, K):
        print("DES decryption start.")
        M=[]
        for i in range(len(C)):
            m=self.des_decryption(C[i],K)
            s=""
            for j in m:
                s+=str(j)
            M.append(hex(int(s,2)).replace('0x',''))
        return M

if __name__ == '__main__':
    # M="Your lips are smoother than vaseline"
    M="596F7572206C6970 732061726520736D 6F6F746865722074 68616E2076617365 6C696E650D0A"
    K="0E329232EA6D0D73"
    C="C0999FDDE378D7ED 727DA00BCA5A84EE 47F269A4D6438190 9DD52F78F5358499 828AC9B453E0E653"
    # M="0123456789ABCDEF"
    # K="133457799BBCDFF1"

    if " " in M:
        # 处理 64位以上的明文 M
        M=M.split(' ')
        if len(M[-1])%16!=0:
            for i in range(16-len(M[-1])%16):
                M[-1]+="0"
        tmpM=[]
        for m in M:
            m=bin(int(m,16)).replace('0b','')
            if len(m)%64!=0:
                for i in range(64-len(m)%64):
                    m="0"+m
            tmpM.append(m)
        M=[]
        for b in tmpM:
            M.append([int(x) for x in b])
    else:
        # 处理64位明文
        M=bin(int(M,16)).replace('0b','')
        if len(M)!=64:
            for i in range(64-len(M)):
                M="0"+M
        M=[[int(x) for x in M]]
        print(M)

    if " " in C:
        # 处理 64位以上的密文 C
        C = C.split(' ')
        # if len(C[-1]) % 16 != 0:
        #     for i in range(16 - len(C[-1]) % 16):
        #         C[-1] += "0"
        tmpC = []
        for c in C:
            c = bin(int(c, 16)).replace('0b', '')
            if len(c) % 64 != 0:
                for i in range(64 - len(c) % 64):
                    c = "0" + c
            tmpC.append(c)
        C = []
        for b in tmpC:
            C.append([int(x) for x in b])
    else:
        # 处理64位密文
        C=bin(int(C,16)).replace('0b','')
        if len(C)!=64:
            for i in range(64-len(C)):
                C="0"+C
        C=[[int(x) for x in C]]
        print(C)

    # 处理密钥
    kb = bin(int(K, 16)).replace('0b', '')
    if len(kb)!=64:
        for i in range(64-len(kb)):
            kb="0"+kb
    K=[]
    for b in kb:
        K.append(int(b))
    # print(K)

    des=DES()
    C=des.des_encrypt(M,K)
    print(C)
    M=des.des_decrypt(C,K)
    print(M)