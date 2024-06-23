from Program import Inst
Regname_enum = ['zero','at','v0','v1','a0','a1','a2','a3',
                    't0','t1','t2','t3','t4','t5','t6','t7',
                    's0','s1','s2','s3','s4','s5','s6','s7',
                    't8','t9','k0','k1','gp','sp','fp(s8)','ra']
class RegisterFile():
    GnralReg = 32
    def __init__(self):
        self.PC = 0
        self.IR = Inst()
        self.Reglist = []
        self.regReady = []
        self.regDReady = []
        for i in range(0,self.GnralReg):
            self.Reglist.append(0)
            self.regReady.append(1)
            self.regDReady.append(0)
    def show_reg(self):
        print("Showing 32 general regs in MIPS32...")
        print('Reg\t\t\tValue\n------------------')
        for i in range(0,len(self.Reglist)):
            reg_str = Regname_enum[i]
            reg_val = self.Reglist[i]
            str = "{0:8}".format(reg_str)
            str = str + '\t{}'.format(reg_val)
            print(str)
        print('\n')
        return

class Mem():
    def __init__(self,size):
        self.value = []
        for i in range(0,size):
            self.value.append(0)