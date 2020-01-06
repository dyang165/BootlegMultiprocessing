#!/bin/python3
import os
import time
import subprocess
import random
import sys
random.seed(100)
basepath = "/pylon5/ir5phqp/dhyang/imslp/"
#basepath = "/data1/dbashir/Project/"
filelist = "/home/dhyang/imslp_convert/filelist.txt"
tmpbasepath = "/pylon5/ir5phqp/dhyang/tmp_dir/"
#tmpbasepath = "/home/dyang/tmp_dir/"
#outdirbasepath = "/pylon5/ir5phqp/dhyang/imslp_bootleg_dir/"
#outdirbasepath = "/home/dhyang/imslp_bootleg_dir/"
outdirbasepath = "/pylon5/ir5phqp/dhyang/imslp_bootleg_dir/"
errorbasepath = "/pylon5/ir5phqp/dhyang/error_dir/"
count = 1
with open(filelist, 'r') as f:
    numFiles = 2
    maxJobs = 200
    lines = f.read().splitlines()
    lineList = []
    running_id = []
    for i in range(numFiles):
        lineList.append(random.choice(lines))
    for line in lineList:
        input_pdf_file = basepath+line.strip()
        fname = line.strip()
        tmp_file = tmpbasepath+fname[30:-4]+"/page.png"
        output_pkl_file = outdirbasepath+fname[30:-4]+'.pkl'
        error_file = errorbasepath+fname[30:-4]+'.txt'
        if os.path.exists(output_pkl_file):
            continue
        subprocess.call("source /home/dhyang/MIR4/bin/activate", shell=True)
        subprocess.call("source activate MIR4", shell=True)
        subprocess.call("rm -r /home/dhyang/imslp_convert/slurm*", shell=True)
        if len(running_id) == maxJobs:
            check = True
            while(check):
                subprocess.call(
                    "rm -r /home/dhyang/imslp_convert/slurm*", shell=True)
                firstID = running_id[0]
                process = subprocess.Popen(
                    ['sacct', '--jobs='+firstID], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = process.communicate()
                out = str(out)
                if "completed" in out.lower():
                    running_id.pop(0)
                    check = False
                time.sleep(.1)
        f = open("/home/dhyang/tmp.txt", 'w')
        subprocess.call(['sbatch', 'bootlegWrapper.sh',
                         input_pdf_file, tmp_file, output_pkl_file, error_file], stdout=f)
        f.close()
        with open("/home/dhyang/tmp.txt", 'r') as f:
            out = f.readline()
        out = str(out)
        outIdx = out.split(" ")[-1][:-1].strip()
        running_id.append(outIdx)
        print("Running ", outIdx)
        print("Ran ", count)
        count += 1
