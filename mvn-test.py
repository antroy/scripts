#!/usr/bin/env python3

import argparse
import re
import subprocess

completion_enabled = False
try:
    import argcomplete
    completion_enabled = True
except:
    print("For autocompletion: pip install argcomplete")


def opts():
    parser = argparse.ArgumentParser(description='Run Senerity tests for a project')
    parser.add_argument('-t', '--test', help='Test to run')
    parser.add_argument('-i', '--it', help='Test to run')

    if completion_enabled:
        argcomplete.autocomplete(parser)

    return parser.parse_args()

def fix_pasted_test(test):
    return re.sub(':.*$', '', test.replace('.','#'))

options = opts()

command = ['mvn', 'clean', 'verify']

if options.test:
    command.append("-Dtest=%s" % fix_pasted_test(options.test))
    command.append("-Dit.test=NONE")
elif options.it:
    command.append("-Dtest=NONE")
    command.append("-DfailIfNoTests=false")
    command.append("-Dit.test=%s" % fix_pasted_test(options.it))

print("Running: %s" % " ".join(command))
subprocess.run(command)

