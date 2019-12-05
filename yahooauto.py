import os
import argparse
from tqdm import tqdm


def parse_arguments():

    p = argparse.ArgumentParser()

    pa = p.add_argument_group(title='Authentication Options')
    pa.add_argument('-ct', '--cookie_t', type=str,
                    help='T authentication cookie from yahoo.com')
    pa.add_argument('-cy', '--cookie_y', type=str,
                    help='Y authentication cookie from yahoo.com')
    pa.add_argument('-ce', '--cookie_e', type=str, default='',
                    help='Additional EuConsent cookie is required in EU')

    return p.parse_args()


args = parse_arguments()
cookie_t = cookie_y = cookie_e = ""

if args.cookie_t:
    cookie_t = args.cookie_t
if args.cookie_y:
    cookie_y = args.cookie_y
if args.cookie_e:
    cookie_e = args.cookie_e

existingdirs = set()
with os.scandir() as it:
    for entry in it:
        if not entry.name.startswith('.') and entry.is_dir():
            existingdirs.add(entry.name)

with open('groupids.txt', 'r') as gfile:
    gfiletext = gfile.readlines()
groupids = list()
for line in gfiletext:
    group_id = line.rstrip()
    if group_id not in existingdirs:
        groupids.append(group_id)

for group_id in tqdm(groupids):
    tqdm.write("Processing {}".format(group_id))
    os.system('python yahoo.py -ct "{t}" -cy "{y}" -ce "{e}" -f -i -d -l -q -p -a -m "{g}"'.format(t=cookie_t,
                                                                                                   y=cookie_y,
                                                                                                   e=cookie_e,
                                                                                                   g=group_id))
