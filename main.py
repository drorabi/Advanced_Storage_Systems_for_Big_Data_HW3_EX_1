import random
import numpy as np
import matplotlib.pyplot as plt
from server import Server


def create_servers_list(upper_bound=2 ** 32 - 1, array_size=100):
    rnd_arr = random.sample(range(upper_bound + 1), array_size)
    servers_list = [Server(num) for num in rnd_arr]
    servers_list.sort(key=lambda x: x.get_address())
    return servers_list


def create_object_list(upper_bound=2 ** 32 - 1, array_size=10000):
    obj_list = list(random.sample(range(upper_bound + 1), array_size))
    obj_list.sort()
    return obj_list


def assign_loads(servers_list, obj_list):
    i = 0
    j = 0
    while i < len(obj_list) and j < len(servers_list):
        while j < len(servers_list) and obj_list[i] >= servers_list[j].get_address():
            j += 1
        while i < len(obj_list) and j < len(servers_list) and servers_list[j].get_address() > obj_list[i]:
            servers_list[j].get_objects().append(obj_list[i])
            i += 1
    while i < len(obj_list):
        servers_list[0].get_objects().append(obj_list[i])
        i += 1
    return


def compute_results(servers_load):
    median = np.median(servers_load)
    average = np.mean(servers_load)
    minimum = np.min(servers_load)
    maximum = np.max(servers_load)
    percentile_25 = np.percentile(servers_load, 25)
    percentile_75 = np.percentile(servers_load, 75)

    return median, average, minimum, maximum, percentile_25, percentile_75


def print_results(median, average, minimum, maximum, percentile_25, percentile_75, servers_list, servers_type="regular", g_color="springgreen"):
    server_load = [server.get_load() for server in servers_list]
    server_load.sort()

    plt.plot(range(1, len(server_load) + 1), server_load, color=g_color, marker='o', linestyle='-')
    plt.xlabel('servers')
    plt.ylabel('load')
    plt.title('Load Distributions of {} servers'.format(len(server_load)))
    plt.axhline(y=median, color='red', linestyle='--', label='Median of {} = {}'.format(servers_type, median))
    plt.axhline(y=average, color='green', linestyle='--', label='Average of {} = {}'.format(servers_type, average))
    plt.axhline(y=minimum, color='orange', linestyle='--', label='Minimum of {} = {}'.format(servers_type, minimum))
    plt.axhline(y=maximum, color='purple', linestyle='--', label='Maximum of {} = {}'.format(servers_type, maximum))
    plt.axhline(y=percentile_25, color='brown', linestyle='--', label='25th Percentile of {} = {}'.format(servers_type, percentile_25))
    plt.axhline(y=percentile_75, color='pink', linestyle='--', label='75th Percentile of {} = {}'.format(servers_type, percentile_75))
    plt.legend()

    print(
        "Log printing:\nmedian = {0}\naverage = {1}\nminimum_load = {2}\nmaximum_load = {3}\npercentile_25 = {4}\npercentile_75 = {5}"
        .format(median, average, minimum, maximum, percentile_25, percentile_75))
    print("======================")
    print("======================")


def create_servers_virtual_ids(servers_list, virtual_num, upper_bound=2 ** 32 - 1):
    virtual_addresses = list(random.sample(range(upper_bound + 1), len(servers_list) * virtual_num))
    virtual_addresses.sort()
    partitions_list = virtual_addresses.copy()
    random.shuffle(partitions_list)
    map_virtual = {}

    for server in servers_list:
        new_vir = partitions_list[:4]
        server.set_virtual_addresses(new_vir)
        partitions_list = partitions_list[4:]
        for vir in new_vir:
            map_virtual[vir] = server

    return virtual_addresses, map_virtual


def assign_loads_virtual_addresses(obj_list, virtual_addresses, map_virtual):
    i = 0
    j = 0
    while i < len(obj_list) and j < len(virtual_addresses):
        while j < len(virtual_addresses) and obj_list[i] >= virtual_addresses[j]:
            j += 1
        while i < len(obj_list) and j < len(virtual_addresses) and virtual_addresses[j] > obj_list[i]:
            map_virtual[virtual_addresses[j]].get_objects().append(obj_list[i])
            i += 1
    while i < len(obj_list):
        map_virtual[virtual_addresses[0]].get_objects().append(obj_list[i])
        i += 1
    return


def ex1():
    obj_list = create_object_list(array_size=10000)
    servers_list = create_servers_list(array_size=100)
    assign_loads(servers_list, obj_list)

    median, average, minimum, maximum, percentile_25, percentile_75 = compute_results(
        [server.get_load() for server in servers_list])
    print_results(median, average, minimum, maximum, percentile_25, percentile_75, servers_list, servers_type="regular", g_color="springgreen")

    virtual_servers_list = create_servers_list(array_size=100)
    virtual_addresses, map_virtual = create_servers_virtual_ids(virtual_servers_list, virtual_num=4)
    assign_loads_virtual_addresses(obj_list, virtual_addresses, map_virtual)

    median, average, minimum, maximum, percentile_25, percentile_75 = compute_results(
        [server.get_load() for server in virtual_servers_list])
    print_results(median, average, minimum, maximum, percentile_25, percentile_75, virtual_servers_list, servers_type="virtual", g_color="royalblue")

    plt.show()


if __name__ == '__main__':
    ex1()
