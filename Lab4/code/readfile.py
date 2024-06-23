class ReadFile():
    def __init__(self,path):
        f = open(path)
        self.request_list=[]
        for line in f:
            word = line.split()
            word[0] = int(word[0], 10)
            word[1] = int(word[1], 16)
            word[2] = int(word[2], 16)
            self.request_list.append(word)
        return
