# -*- coding: utf-8 -*-
# Routorule_byZz.py

import os
import re
import math

ip_ver = 'IPv4'
start_stop_key = '=='

if __name__ == '__main__':

    match_ver = False
    start = False

    tmp_file = open(os.getcwd() + '\\' + 'rule.txt', 'a', encoding='utf-8')

    for line in open(os.getcwd() + '\\' + 'route.txt', 'r'):

        if not match_ver & start:
            ip_ver_match_obj = re.match(ip_ver, line)
            start_match_obj = re.match(start_stop_key, line)

            if ip_ver_match_obj != None:
                match_ver = True

            if match_ver & (start_match_obj != None):
                start = True

        else:
            stop_match_obj = re.match(start_stop_key, line)
            if stop_match_obj != None:
                break

            route_match_obj = re.match('.*?(\d\S+).*?(\S+).*?(\S+).*?(\S+).*?(\S+)', line)
            if route_match_obj == None:
                continue
            try:
                ip_dst = route_match_obj.group(1).split('.')
                net_mask = route_match_obj.group(2).split('.')
                net_gate = route_match_obj.group(3)
                interface = route_match_obj.group(4)
                metric = route_match_obj.group(5)
            except:
                continue

            #ip_dst_d = int(ip_dst[0]) * 2 ^ 24 + int(ip_dst[1]) * 2 ^ 16 + int(ip_dst[2]) * 2 ^ 8 + int(ip_dst[3])

            if (ip_dst[0] == '0' or
                ip_dst[0] == '10' or
                (ip_dst[0] == '172') & (16 <= int(ip_dst[1]) < 32) or
                (ip_dst[0] == '192') & (ip_dst[1] == '168') or
                (224 <= int(ip_dst[0]))):
                continue

            prefix = str(32 - math.floor(math.log(256 - int(net_mask[0]), 2) + \
                math.log(256 - int(net_mask[1]), 2) + \
                math.log(256 - int(net_mask[2]), 2) + \
                math.log(256 - int(net_mask[3]), 2)))

            try:
                tmp_file.write(ip_dst[0] + '.' + ip_dst[1] + '.' + ip_dst[2] + '.' + ip_dst[3] + \
                    '/' + prefix + '\n')

            except:
                pass

    tmp_file.close()
