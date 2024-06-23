from Program import Inst
from Program import InstructionList
from Register import RegisterFile
from Register import Mem
class PiplineSection():
    def __init__(self):
        self.inst_idx = 0
        self.ready = 0
        self.stall = 0
    def show_ps_section(self, namestr, Instlst, inr):
        # print("self.instidx",self.inst_idx)
        if self.inst_idx == 'stall':
            print("Pipline section {} is frozen.\n".format(namestr))
            return
        elif self.inst_idx == 0:
            print("Pipline section {} is empty.\n".format(namestr))
        else:
            print("Showing pipline section {}\nCurrent instruction in this section is {}\n".format(namestr,Instlst.IL[inr[self.inst_idx]].show()))
        return


class Buffer():
    def __init__(self,i,a,b,c,d,e,ii,ans,reg_id):
        self.i =i
        self.a=a
        self.b=b
        self.c=c
        self.d=d
        self.e=e
        self.ii=ii
        self.ans=ans
        self.reg_id = reg_id

class Pipline():
    def __init__(self):
        self.clock = 0
        self.ps1 = PiplineSection()
        self.ps2 = PiplineSection()
        self.ps3 = PiplineSection()
        self.ps4 = PiplineSection()
        self.ps5 = PiplineSection()
        self.RegFile = RegisterFile()
        self.InstLst = InstructionList()
        self.Memory = Mem(16)
        self.stmap = [] # (inst_idx,clk,pipline_segment)
        self.insidx_ran = [] # record inst's index has been run
        self.insidx_ran.append(0)
        self.buffer = Buffer(0,0,0,0,0,0,0,0,0)
        self.freeze = 0
        self.direct = True # True--use direction; False--not use direction


    def reset(self):
        self.__init__()

    def IF(self):
        if self.freeze:
            return 0
        if self.ps1.stall:
            inst = self.InstLst.IL[self.insidx_ran[self.ps1.inst_idx]]
            self.stmap.append((self.ps1.inst_idx, self.clock, 'IF'))
            self.RegFile.regReady[inst.oop] = 0
        elif self.RegFile.PC < len(self.InstLst.IL) and self.RegFile.PC > 0:
            self.insidx_ran.append(self.RegFile.PC)
            inst_index = len(self.insidx_ran)-1
            self.ps1.inst_idx = inst_index
            inst = self.InstLst.IL[self.RegFile.PC]
            self.RegFile.PC = self.RegFile.PC + 1
            self.RegFile.IR = inst
            self.stmap.append((self.ps1.inst_idx, self.clock, 'IF'))
            if inst.type == 'add':
                self.RegFile.regReady[inst.oop]=0
        else:
            self.ps1.inst_idx = 0
        print("IF SEGMENT, inst_idx = ",self.ps1.inst_idx)
        return self.ps1.inst_idx

    def ID(self, inst_index,reg_id,reg_val):
        self.ps2.inst_idx = inst_index
        inst = self.InstLst.IL[self.insidx_ran[inst_index]]
        if inst_index == 0:
            op1_val = 0
            op2_val = 0
        elif inst.type == 'load' or inst.type == 'store':
            op1_val = self.RegFile.Reglist[inst.op1]
            op2_val = inst.op2
        elif inst.type == 'add':
            willbe_reg = 0
            print("self.buffer.a = ",self.buffer.a)
            if self.buffer.a != 'stall':
                willbe_reg = self.InstLst.IL[self.insidx_ran[self.buffer.a]].oop
                print("willbrg",willbe_reg)
            if self.RegFile.regReady[inst.op1] and self.RegFile.regReady[inst.op2]:
                op1_val = self.RegFile.Reglist[inst.op1]
                op2_val = self.RegFile.Reglist[inst.op2]
            elif (self.direct
                  and (self.RegFile.regReady[inst.op1] or self.RegFile.regDReady[inst.op1] or inst.op1 == willbe_reg)
                  and (self.RegFile.regReady[inst.op2] or self.RegFile.regDReady[inst.op2] or inst.op2 == willbe_reg)):
                op1_val = self.RegFile.Reglist[inst.op1]
                op2_val = self.RegFile.Reglist[inst.op2]
                if reg_id == inst.op1:
                    op1_val = reg_val
                if reg_id == inst.op2:
                    op2_val = reg_val
            else:
                op1_val = 0
                op2_val = 0
                self.stall = 1
                inst_index = 'stall'
                print("In clock {}, ID stall, inst_idx in ID = {}".format(self.clock,self.ps2.inst_idx))
        elif inst.type == 'beqz':
            self.freeze = 1
            op1_val = self.RegFile.Reglist[inst.op1]
            op2_val = (op1_val == 0) # modified
            self.buffer.i = 0
        if self.ps2.inst_idx != 0:
            self.stmap.append((self.ps2.inst_idx, self.clock,'ID'))

        return inst_index, op1_val, op2_val

    def EX(self,inst_index,opv1,opv2):
        reg_id = -1
        if inst_index == 'stall':
            return 0,0,0
        self.ps3.inst_idx = inst_index
        inst = self.InstLst.IL[self.insidx_ran[inst_index]]
        ans = opv1+opv2
        if inst_index == 0:
            opv1 = 0
            opv2 = 0
        elif inst.type == 'load' or inst.type == 'store':
            ans = opv1 + opv2
            reg_id = inst.oop
            self.RegFile.regDReady[inst.oop] = 1
        elif inst.type == 'add':
            opv1 = self.RegFile.Reglist[inst.op1]
            opv2 = self.RegFile.Reglist[inst.op2]
            if self.buffer.reg_id == inst.op1:
                op1_val = self.buffer.e
            if self.buffer.reg_id == inst.op2:
                op2_val = self.buffer.e
            ans = opv1+opv2
            reg_id = inst.oop
            self.RegFile.regDReady[inst.oop] = 1
        elif inst.type == 'beqz':
            if opv2:
                ans = self.insidx_ran[inst_index] + opv1
            else:
                ans = self.insidx_ran[inst_index]
        if self.ps3.inst_idx != 0:
            self.stmap.append((self.ps3.inst_idx, self.clock,'EX'))
        return inst_index,ans,reg_id

    def MEM(self,inst_index,ans):
        self.ps4.inst_idx = inst_index
        inst = self.InstLst.IL[self.insidx_ran[inst_index]]
        # TO BE FINISHED
        if inst_index == 0:
            return inst_index, ans
        elif inst.type == 'load':
            ans = self.Memory.value[ans]
        elif inst.type == 'store':
            self.Memory.value[ans] = self.RegFile.Reglist[inst.oop]
        elif inst.type == 'beqz':
            self.RegFile.PC = ans
            self.freeze = 0
            print("new PC = ",self.RegFile.PC)
        if self.ps4.inst_idx != 0:
            self.stmap.append((self.ps4.inst_idx, self.clock,'MEM'))
        return inst_index,ans

    def WB(self,inst_index,ans):
        self.ps5.inst_idx = inst_index
        inst = self.InstLst.IL[self.insidx_ran[inst_index]]
        if inst.type =='add' or inst.type == 'load':
            self.RegFile.Reglist[inst.oop]=ans
            self.RegFile.regReady[inst.oop]=1
        if self.ps5.inst_idx != 0:
            self.stmap.append((self.ps5.inst_idx, self.clock,'WB'))
        return

    def show_ps(self):
        self.ps1.show_ps_section('IF',self.InstLst,self.insidx_ran)
        self.ps2.show_ps_section('ID',self.InstLst,self.insidx_ran)
        self.ps3.show_ps_section('EX',self.InstLst,self.insidx_ran)
        self.ps4.show_ps_section('MEM',self.InstLst,self.insidx_ran)
        self.ps5.show_ps_section('WB',self.InstLst,self.insidx_ran)

    def run_pipline(self):
        i = self.IF()
        a,b,c = self.ID(self.buffer.i,self.buffer.e,self.buffer.reg_id)
        d,e, reg_id = self.EX(self.buffer.a,self.buffer.b,self.buffer.c)
        ii,ans = self.MEM(self.buffer.d,self.buffer.e)
        self.WB(self.buffer.ii,self.buffer.ans)
        if self.freeze:
            i=0
        if a == 'stall':
            i = self.buffer.i
            self.ps1.stall = 1
            self.ps2.stall = 1
        else:
            self.ps1.stall = 0
            self.ps2.stall = 0
        self.buffer = Buffer(i, a, b, c, d, e, ii, ans,reg_id)
        self.clock = self.clock + 1
        return

    def Run(self,pc,clk):
        self.clock = 1
        self.RegFile.PC = pc
        self.buffer.pc = pc
        while self.clock<=clk:
            print("\n---clock: {}---".format(self.clock))
            self.run_pipline()

    def draw_stmap(self,clks):
        prtarr = []
        # print(self.insidx_ran)
        num_inst = len(self.insidx_ran) - 1
        sum = clks * num_inst
        for i in range(0,sum):
            prtarr.append(' ')
        # print(prtarr)
        for key in self.stmap:
            iid = key[0]
            clk = key[1]
            position = (iid-1) * clks + clk-1
            # print("position = ",position)
            if position < sum:
                prtarr[position] = key[2]
        print("all ins",self.insidx_ran)
        str = "\n----Instructions\clocks----"
        for column in range(1, clks+1):
            str = str + "\t{}\t".format(column)
        print(str)
        for line in range(1,num_inst+1):
            str = "{0:27}".format(self.InstLst.IL[self.insidx_ran[line]].show())
            for column in range(0,clks):
                position = (line-1) * clks + column
                str = str + "\t{}\t".format(prtarr[position])
            print(str)
        print("stmap",self.stmap)
        self.evaluate()

    def evaluate(self):
        sze = len(self.stmap)
        all = len(self.insidx_ran)
        print("流水线的效率：{}".format(sze / (self.clock * 5)))
        print("流水线加速比：{}".format(all*5/self.clock))
    def menu(self):
        print("\n\n...请将程序置于input.txt中，保证每行一条指令...")
        print("1-设置程序断点\t2-查看流水器部件状态\t3-查看寄存器的值\t4-单步执行\t5-执行到断点\t6-流水线性能分析\n7-退出")
        # self.InstLst.load_program()
        tmp = input("\n请输入操作序号：")
        if tmp == '1':
            bp=input("请输入断点值：")
            self.InstLst.breakpoint = int(bp)
            print(self.InstLst.breakpoint)
            return 1
        elif tmp == '2':
            self.show_ps()
            return 1
        elif tmp == '3':
            self.RegFile.show_reg()
            return 1
        elif tmp == '4':
            self.run_pipline()
            self.draw_stmap(self.clock)
            return 1
        elif tmp == '5':
            self.Run(1,self.InstLst.breakpoint)
            self.draw_stmap(self.clock)
            return 1
        elif tmp == '6':
            self.evaluate()
            return 1
        elif tmp == '7':
            return 0
        print("输入不合法，请重试\n")
        return 0
