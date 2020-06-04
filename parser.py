#!/usr/bin/python3

import os
import sys
import argparse
import re
import subprocess

kernel_dict = {
    'linux_version': re.compile(r'VERSION = (?P<linux_version>\d+)\n'),
    'patch_level': re.compile(r'PATCHLEVEL = (?P<patch_level>\d+)\n')
}

def line_parser(line):
    for key, rx in kernel_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None

def parse_kernel_makefile(target_file):
    
    rt=""

    if os.path.isfile(target_file):
      with open(target_file, 'r') as f:
          line = f.readline()
          while line:
            key, match = line_parser(line)
            if key == 'linux_version':
                linux_version = match.group('linux_version')
            if key == 'patch_level':
                patch_level = match.group('patch_level')
            line = f.readline()
      if linux_version == "3":
        rt="linux-quic_"+linux_version+"."+patch_level
      else:
        rt="linux-msm_"+linux_version+"."+patch_level
    else:
      rt="ERROR::The file %s doesn't exist"%(target_file)

    return rt


t = parse_kernel_makefile(str(sys.argv[1]))
print ("%s"%(t))

