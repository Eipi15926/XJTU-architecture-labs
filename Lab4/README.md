本次实验我自己实现了一个Cache模拟器。模拟器运行环境为Python3，实验结果在命令行以表格形式输出。

- 将代码文件夹解压，打开`main.py`，修改path、cache_size_list、cache_ass_list，cache_blocksize_list，替换策略为需要的值。注意这里的cache_size表示的是2的幂，如cache_size=3表示Cache的大小为 23=8KB2^3=8KB23=8KB；
- 打开命令行，切换到代码文件夹，输入命令：`python3 main.py`；
- 等待代码运行完毕即可在命令行看到输出结果。