from Pipline import Pipline
from Program import Inst
from Program import InstructionList
from Register import RegisterFile

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    pipline = Pipline()
    # 如何以这种语法输入一条指令：Inst('operation_name',src_op1,src_op2,dst_op)
    pipline.InstLst.IL = [Inst(),Inst('add',1,2,3),Inst('beqz',2,0,1),Inst('load',1,2,1),Inst('store',1,2,1)]
    # pipline.InstLst.IL = [Inst(), Inst('add',1,2,3), Inst('add',1,2,3),Inst('add',1,2,3)]
    # pipline.InstLst.IL = [Inst(), Inst('add', 1, 2, 3), Inst('add', 2, 3, 4), Inst('add', 3, 5, 6)]
    pipline.RegFile.PC = 1
    """pipline.Run(pc = 1,clk = 12)
    pipline.draw_stmap(clks = 12)"""
    cont = 1
    while(cont):
        cont = pipline.menu()
    print("\n-----Goodbye!-----\n")