import random


class CacheBlock():
    def __init__(self,size):
        self.empty = True
        self.size = size
        self.current_use = -1
        self.tag = 2147483647
        return


class Cache():
    def __init__(self,cs,cb,ca,rp):
        # 均表示2的幂
        self.cache_size = cs
        self.cache_block = cb
        self.cache_ass = ca
        self.block_cnt = cs + 10 - cb
        self.grp_cnt = self.block_cnt - ca
        self.grp_mask = 0
        self.blk_addr_msk = 0
        self.replace = rp
        # self.replace = 'LRU'
        # self.replace = 'random'
        one = 1
        for i in range(0,self.cache_block):
            self.blk_addr_msk = self.blk_addr_msk | one
            one = one << 1
        for i in range(0,self.grp_cnt):
            self.grp_mask = self.grp_mask | one
            one = one << 1
        #print("grp_mask:",self.grp_mask)
        self.reset()
        return

    def reset(self):
        self.Cache = []
        self.miss_cnt = 0
        self.total_cnt = 0
        self.read_cnt = 0
        self.write_cnt = 0
        self.write_miss = 0
        self.read_miss = 0
        self.compulsory_miss_cnt = 0
        self.capacity_miss_cnt = 0
        self.conflict_miss_cnt = 0
        self.full_block_cnt = 0
        for i in range(0, 2**self.grp_cnt):
            grp = []
            for j in range(0, 2**self.cache_ass):
                grp.append(CacheBlock(self.cache_size))
            self.Cache.append(grp)
        return

    def input_request(self,op,addr,size):
        if op == 0 or op == 2:
            self.read_cnt = self.read_cnt + 1
        elif op == 1:
            self.write_cnt = self.write_cnt + 1
        self.handle_addr(addr,op)
        return

    def handle_addr(self,addr,op):
        block_addr = addr & self.blk_addr_msk
        grp_number = (addr & self.grp_mask) >> self.cache_block
        tag = (addr & ~(self.grp_mask & self.blk_addr_msk)) >> (self.grp_cnt + self.cache_block)
        #print("self.grp_cnt = {}, grp_number = {}\n".format(self.grp_cnt, grp_number))
        current_grp = self.Cache[grp_number]
        for cache_block in current_grp:
            if cache_block.empty == False and cache_block.tag == tag:
                # print("Cache hits.\n")
                cache_block.current_use = self.total_cnt
                self.total_cnt = self.total_cnt + 1
                return
        # print("Cache misses.\n")
        self.miss_cnt = self.miss_cnt + 1
        if op ==1:
            self.write_miss = self.write_miss + 1
        else:
            self.read_miss = self.read_miss + 1
        self.handle_miss(grp_number,tag)
        self.total_cnt = self.total_cnt + 1
        return

    def handle_miss(self,grp_number,tag):
        current_grp = self.Cache[grp_number]
        sac_cache = CacheBlock(1)
        sac_cache.current_use = -1
        for cache_block in current_grp:
            if cache_block.empty == True:
                cache_block.empty = False
                cache_block.current_use = self.total_cnt
                cache_block.tag = tag
                self.compulsory_miss_cnt = self.compulsory_miss_cnt + 1
                self.full_block_cnt = self.full_block_cnt + 1
                # print("Cold-miss happend.\n")
                return
            else:
                if cache_block.current_use < sac_cache.current_use or sac_cache.current_use == -1:
                    sac_cache.tag = cache_block.tag

        if self.full_block_cnt == self.block_cnt:
            self.capacity_miss_cnt = self.capacity_miss_cnt + 1
            # print("Capacity miss happend.\n")
        else:
            self.conflict_miss_cnt = self.conflict_miss_cnt + 1
            # print("Conflict miss happend.\n")
        # print("tag",sac_cache.tag)
        if self.replace == 'random':
            rand_num = random.randint(0, 2**self.cache_ass-1)
            sac_cache.tag = current_grp[rand_num].tag
            # if self.cache_ass > 0:
                # print(rand_num,sac_cache.tag)
        for cache_block in current_grp:
            if cache_block.tag == sac_cache.tag:
                cache_block.tag = tag
                cache_block.current_use = self.total_cnt
                cache_block.empty = False
        return

    def show_efficiency(self):
        str = ""
        str = str + "\nThe size of Cache is {}KB, the size of each cache block is {}B, and the associativity of cache is {}.".format(2**self.cache_size,2**self.cache_block,2**self.cache_ass)
        str = str + "\nCache replacement policies is {}.".format(self.replace)
        str = str + "\nThere are {} requests in total. {} cache blocks were written and {} cache blocks were read".format(self.total_cnt,self.write_cnt,self.read_cnt)
        str = str + "\nReading miss rate is {:.2f}%, writing missing rate is {:.2f}%.".format(100*self.read_miss/self.read_cnt,100*self.write_miss/self.write_cnt)
        str = str + "\nThe missing rate is: {:.2f}%.\n".format(100 * self.miss_cnt/self.total_cnt)
        return 100 * self.miss_cnt/self.total_cnt, str

    def show_misstype(self):
        if self.miss_cnt != 0:
            compulsory = 100 * self.compulsory_miss_cnt/self.miss_cnt
            capacity = 100 * self.capacity_miss_cnt/self.miss_cnt
            conflict = 100 * self.conflict_miss_cnt/self.miss_cnt
            return compulsory,capacity,conflict
        else:
            return 0,0,0