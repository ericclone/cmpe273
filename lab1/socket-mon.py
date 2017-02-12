#! /usr/bin/env python
import psutil

connection_list = psutil.net_connections()
attr_list = ['"pid"', '"laddr"', '"raddr"', '"status"']
print ",".join(attr_list)
result = {}
for connection in connection_list:
    if connection.laddr and connection.raddr:
        pid = connection.pid
        laddr = connection.laddr
        raddr = connection.raddr
        entry = '"{}@{}","{}@{}","{}"'.format(laddr[0], laddr[1], raddr[0], raddr[1], connection.status)
        # print entry
        if pid and pid in result:
            result[pid].append(entry)
        elif pid:
            result[pid] = [entry]
    # print [getattr(connection, attr) for attr in attr_list]
    # print ",".join(map(str, [getattr(connection, attr) for attr in attr_list]))
for pid in sorted(result, key = lambda k:len(result[k]), reverse=True):
    for entry in result[pid]:
        print '"{}",{}'.format(pid, entry)
