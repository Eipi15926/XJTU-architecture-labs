NULL = -1
class InstructionList():
    def __init__(self):
        self.IL = []
        self.IL.append(Inst())
        self.beginpoint = 1
        self.breakpoint = NULL
        # self.load_program()
        return

    def set_breakpoint(self,bp):
        self.breakpoint =bp

    def load_program(self,filepath):
        f = open('input.txt')
        # f = open(filepath)
        txt = []
        for line in f:
            txt.append(line.strip())
            word = line.split()
            print("word is ", word)
            tmpinst = Inst()
            tmpinst.form_inst(word)
            self.IL.append(tmpinst)
        print(txt)
        return



class Inst():
    alltype = ['load','store','add','beqz']
    Regname_dict = {'zero':0,'at':1,'v0':2,'v1':3,'a0':4,'a1':5,'a2':6,'a3':7,
                    't0':8,'t1':9,'t2':10,'t3':11,'t4':12,'t5':13,'t6':14, 't7':15,
                    's0':16,'s1':17,'s2':18,'s3':19,'s4':20,'s5':21,'s6':22,'s7':23,
                    't8':24,'t9':25,'k0':26,'k1':27,'gp':28,'sp':29,'s8':30,'fp':30,'ra':31}
    def __init__(self,type = 'add',op1=0,op2=0,oop=0):
        self.type = type
        self.op1 = op1
        self.op2 = op2
        self.oop = oop
        return

    def get_str(self, word):
        lfb = word[2].find('(')
        rtb = word[2].find(')')
        str1 = word[:lfb+1]
        str2 = word[lfb+1:rtb+1]
        return str1, str2

    def form_inst(self, word):
        ans = Inst(word[0],word[1],word[2],word[3])
        self.type = word[0].lower()
        if self.type == 'add':
            self.op1 = self.Regname_dict[word[1].strip(',')[1:]]
            self.op2 = self.Regname_dict[word[2].strip(',')[1:]]
            self.oop = self.Regname_dict[word[3].strip(',')[1:]]
        elif self.type == 'load' or self.type == 'store':
            self.op1 = self.Regname_dict[word[1].strip(',')[1:]]
            self.op2,self.oop = self.get_str(word[2])
        elif self.type == 'beqz':
            self.op1, self.op2 = self.get_str(word[1])
        return ans

    def show(self):
        # print(self.type,self.oop,self.op1,self.op2)
        if self.type == 'add':
            return str(self.type)+': R'+str(self.oop)+' <- R'+str(self.op1)+' + R'+str(self.op2)
        elif self.type == 'load':
            return str(self.type)+': R'+str(self.oop)+' <- R'+str(self.op1)+' + ofst('+str(self.op2)+')'
        elif self.type == 'store':
            return str(self.type) + ': R' + str(self.oop) + ' -> R' + str(self.op1) + ' + ofst(' + str(self.op2) + ')'
        elif self.type == 'beqz':
            return str(self.type) + ': PC <- PC + ofst(' + str(self.op2) +')'