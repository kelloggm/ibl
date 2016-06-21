#!/usr/bin/python

#@ Martin Kellogg, June 2016

# this is a stupid project to make a "meta interpreter" that lets you
# write code in multiple scripting languages in the same file at your
# convenience. While it would be strictly better to just pick a
# scripting language that didn't suck, this does give some flexibility
# if it works and it seems like a fun thing to waste some time on so
# why the hell not???

# for now we won't read from stdin. That would be far too reasonable

# also for now we're going to only handle annotations at the very top
# level -> basically, annotations inside loops/other control
# structures might be hard, so we're going to ignore them.
# actually more accurately we just aren't going to support them
# at all.

import sys
import subprocess

import iblsh
import iblpy

FDEBUG=True

try:
    fl = sys.argv[1]
except:
    print "you should probably give me a file to read"
    exit(1)

slCur = "bash" # default to bash if the user doesn't say what type of script this is

inpSh=iblsh.inp_sh()
rgslSh=iblsh.rgsl_sh()

inpPy=iblpy.inp_py()
rgslPy=iblpy.rgsl_py()

mpsl_inp = {}

for sl in rgslPy:
    mpsl_inp[sl] = inpPy
    
for sl in rgslSh:
    mpsl_inp[sl] = inpSh

rgvarToSave = []
rgvarToGet = []

def assign(ln, sl):
    if sl in rgslPy:
        iblpy.assign_py(ln, rgvarToSave)
    elif sl in rgslSh:
        iblsh.assign_sh(ln, rgvarToSave)
        
def get_rgvar(sl):
    if len(rgvarToGet) == 0:
        return ""

    if sl in rgslPy:
        return iblpy.get_rgvar_py(rgvarToGet)
    elif sl in rgslSh:
        return iblsh.get_rgvar_sh(rgvarToGet)
    else:
        print "usl doesn't support " + sl + " yet!"
        exit(1)

def save_rgvar(sl):
    if len(rgvarToSave) == 0:
        return ""
    
    if sl in rgslPy:
        return iblpy.save_rgvar_py(rgvarToSave)
    elif sl in rgslSh:
        return iblsh.save_rgvar_sh(rgvarToSave)
    else:
        print "ibl doesn't support " + sl + " yet!"
        exit(1)
    
def run_code(sl, stToRun):

    stToRun = get_rgvar(sl) + stToRun + save_rgvar(sl)
    inp = mpsl_inp[sl]
    
    subprocess.call("rm tmp", shell=True)
    with open("tmp", "w") as fd2:
        fd2.write(stToRun)

    subprocess.call(inp + " tmp " + reduce(lambda a,b: a + b + " ", sys.argv[2:], ""), shell=True)

with open(fl) as fd:

    stToRun = ""
    
    for ln in fd:
        assign(ln, slCur)
        if ln.strip().startswith("#"):
            sl = slCur
            slCur = ln[1:].strip()
            
            try:
                run_code(sl,stToRun)
                stToRun = ""
                rgvarToGet = rgvarToSave[:] # just python things...
                
            except KeyError:
                # this means this is a comment...
                stToRun += ln

        
        stToRun += ln

    run_code(slCur, stToRun)

        
if not FDEBUG:
    subprocess.call("rm -f tmp; rm -f tmp-store", shell=True)
