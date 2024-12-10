sample_input = """
2333133121414131402
"""

sample_result = (1928, 2858)

def solve(input_string):
    disk_map = [(i//2 if i%2 == 0 else -1,  int(x)) for i, x in enumerate(input_string.strip())]
    compacted_disk_v1 = compact_disk_v1(disk_map)
    compacted_disk_v2 = compact_disk_v2(disk_map)
    compacted_checksum_v1 = compute_disk_checksum(compacted_disk_v1)
    compacted_checksum_v2 = compute_disk_checksum(compacted_disk_v2)
    return compacted_checksum_v1, compacted_checksum_v2

def compact_disk_v1(disk_map):
    disk = expand_disk_map(disk_map)
    head = 0
    tail = len(disk)-1
    while head < tail:
        while disk[head] != -1:
            head += 1
        while disk[tail] == -1:
            tail -= 1
        while head < tail:
            disk[head] = disk[tail]
            disk[tail] = -1
            head += 1
            tail -= 1
            if disk[head] != -1 or disk[tail] == -1:
                break
    return disk

def compact_disk_v2(disk_map):
    tail = len(disk_map)-1
    target_id, tail_length = disk_map[tail]
    while target_id != 0:
        while disk_map[tail][0] != target_id:
            tail -= 1
            tail_id, tail_length = disk_map[tail]
        if debug:
            pretty_print_disk_map(disk_map, target_id)
        for head in range(tail):
            head_id, head_length = disk_map[head]
            if head_id == -1 and head_length >= tail_length:
                disk_map[head] = (-1, head_length - tail_length)
                disk_map[tail] = (-1, tail_length)
                disk_map.insert(head, (target_id, tail_length))
                if disk_map[tail][0] == disk_map[tail+1][0] == -1:
                    disk_map[tail] = (-1, disk_map[tail][1] + disk_map[tail+1][1])
                    disk_map.pop(tail+1)
                break
        target_id -= 1
    disk = expand_disk_map(disk_map)
    return disk

def expand_disk_map(disk_map):
    disk = []
    for file_id, length in disk_map:
        disk += [file_id]*length
    return disk

def compute_disk_checksum(disk):
    disk_checksum = 0
    for i, file_id in enumerate(disk):
        if file_id != -1:
            disk_checksum += i*file_id
    return disk_checksum

def pretty_print_disk_map(disk_map, target_id):
    disk = ["." if i == -1 else
            str(i) if i != target_id else f"\033[4m{str(i)}\033[0m"
            for i in expand_disk_map(disk_map)]
    print(" ".join(disk))
