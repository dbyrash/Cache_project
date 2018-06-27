import math
import textwrap


def main_memory_mapping():
    dic = {}
    dic1 = {}
    main_memory = []
    rev = []
    main_memory_arr = []

    with open("inst_mem_hex_16byte_wide.txt") as f:
        read_memory = f.readlines()
        for i in range(0, len(read_memory)):
            rev.append(read_memory[i][::-1])
            rev[i] = rev[i][1:]

        for i in range(0, len(rev)):
            z = textwrap.wrap(rev[i], 2)
            dic = dict(enumerate(z))
            dic1.update(dic)
            main_memory.append(dict(dic1))

        for i in range(0, len(main_memory)):
            for j in range(0, 16):
                main_memory[i][j] = main_memory[i][j][::-1]

        for i in range(0, len(main_memory)):
            for j in range(0, 16):
                main_memory_arr.append(main_memory[i][j])
        return main_memory_arr


def address_request():
    with open('inst_addr_trace_hex_project_1.txt', "r") as f:
        fcount = f.readlines()

        for i in range(len(fcount)):
            fcount[i] = fcount[i].strip('\n')
            fcount[i] = (bin(int(fcount[i], 16))[2:]).zfill(32)
        cache_access = len(fcount)
        return fcount, cache_access


def hex_to_dec():
    with open('inst_addr_trace_hex_project_1.txt', "r") as f:
        hex_dec = f.readlines()

        for i in range(len(hex_dec)):
            hex_dec[i] = hex_dec[i].strip('\n')
            hex_dec[i] = int(hex_dec[i], 16)
    return hex_dec


def hex_to_32_bit():
    x = []
    x, y = address_request()
    for i in range(len(x)):
        x[i] = x[i][::-1]
    return x,y


def temp():

    y, cache_accesses = hex_to_32_bit()
    cache_size = int(input("Enter cache size:"))
    block_size = int(input("Enter block size:"))
    associativity = int(input("Enter associativity:"))
    cache = [[]] * associativity
    miss = 0
    cycles = 0
    hit = 0
    main_array = main_memory_mapping()
    ent = entries(cache_size, block_size)


    for i in range(associativity):
        for j in range(int(ent/associativity)):
            cache[i].append({'data': [], 'tag': '-1', 'valid': '0'})

    dec_address = hex_to_dec()

    cache_bits = bits_for_cache(cache_size)
    set_bits = bits_for_associativity(associativity)
    tag_bits = bits_for_tag(cache_bits, set_bits)
    index_bits = bits_for_index(block_size, cache_size, associativity)
    offset_bits = bits_for_offset(block_size)


    for j in range(len(y)):
        tag = y[j][-tag_bits:]
        tag_str = reversed_string(tag)
        tag_dec = int(tag_str, 2)

        index = y[j][offset_bits:index_bits + 1]
        index_str = reversed_string(index)
        index_dec = int(index_str, 2)

        offset = y[j][0:offset_bits]
        offset_str = reversed_string(offset)
        offset_dec = int(offset_str, 2)  # offset_dec

        block_number = (dec_address[j] // block_size) * block_size


        for i in range(associativity):
            if cache[i][index_dec]['valid'] == '0':
                cache[i][index_dec]['valid'] = '1'
                cache[i][index_dec]['tag'] = tag_dec
                cache[i][index_dec]['data'].append(main_array[block_number:(block_number + block_size)])
                miss = miss + 1
                cycles = cycles + 15
            elif cache[i][index_dec]['tag'] == tag_dec and cache[i][index_dec]['valid'] == '1':
                hit = hit + 1
                cycles = cycles + 1
                break;
            elif cache[i][index_dec]['tag'] != tag_dec and cache[i][index_dec]['valid'] == '1':
                val = cycles % associativity
                cache[val][index_dec]['tag'] = tag_dec
                cache[val][index_dec]['data'].append((main_array[block_number:(block_number + block_size)]))
                miss = miss + 1
                cycles = cycles + 15

    hit_ratio = hit/cache_accesses

    print ("No. of cache accesses are:",cache_accesses)
    print ("No. of hits are:", hit)
    print ("Hit Ratio is:", hit_ratio)
    print("No. of cycles are:", cycles)
    print ("IPC = ", cache_accesses/cycles)





def bits_for_cache(cache_size):
    return int((math.log(cache_size) / math.log(2)))


def bits_for_index(block_size, cache_size, ass):
    enteries = cache_size / block_size
    enteries1 = enteries/ass
    return int(math.log(enteries1) / math.log(2))


def bits_for_tag(cache_bits, set_bits):
    return 32 - cache_bits + set_bits


def bits_for_offset(block_size):
    return int((math.log(block_size) / math.log(2)))


def reversed_string(a_string):
    return a_string[::-1]


def entries(cache_size, block_size):
    entries = int(cache_size / block_size)
    return entries


def bits_for_associativity(associativity):
    set_bits = int((math.log(associativity) / math.log(2)))
    return set_bits

temp()
