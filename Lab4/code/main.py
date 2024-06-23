from Cache import Cache
from readfile import ReadFile


def main(path,cache_size,cache_ass,cache_blocksize,replace):
    reqs = ReadFile(path).request_list
    cache = Cache(cs = cache_size, cb = cache_blocksize, ca = cache_ass, rp = replace)
    for request in reqs:
        cache.input_request(op=request[0], addr=request[1], size= request[2])
    ans, str = cache.show_efficiency()
    c1,c2,c3 = cache.show_misstype()
    threec = "\t({:.2f}%, {:.2f}%, {:.2f}%)\t".format(c1,c2,c3)
    return ans, str, threec


#path = './trace files/022.li.din'
#path = './trace files/047.tomcatv.din'
#path = './trace files/078.swm256.din'
path = './trace files/085.gcc.din'
output_path = 'outputs/ReplacePolicyLRU-file022.li.txt'
of = open(output_path)
cache_size_list = [3,4,5,6]
cache_ass_list = [0,1,2,3]
cache_blocksize_list = [4,5,6,7]
replace = 'LRU'
#replace = 'random'
ostr1 = "Cache_size,block, ass\t"
ostr2 = ""
ostr3 = ""
for cache_size in cache_size_list:
    ostr1 = ostr1 + "\n{}KB:\n".format(2**cache_size)
    ostr3 = ostr3 + "\n{}KB:\n".format(2 ** cache_size)
    for cache_blocksize in cache_blocksize_list:
        ostr1 = ostr1 + " {}B ".format(2**cache_blocksize)
        ostr3 = ostr3 + " {}B ".format(2 ** cache_blocksize)
        for cache_ass in cache_ass_list:
            rate, strr, threec = main(path,cache_size,cache_ass,cache_blocksize,replace)
            ostr1 = ostr1 + "\t{:.2f}%\t".format(rate)
            ostr2 = ostr2 + strr
            ostr3 = ostr3 + threec
        ostr1 = ostr1 + "\n"
        ostr3 = ostr3 + "\n"
print(ostr1 + "\n\n" + ostr2 + "\n\n" + ostr3)