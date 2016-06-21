# @ Martin Kellogg, June 2016

import iblsh

# default python interpreter
inpPy = "/usr/bin/python"
# list of legal annotations that indicate we should use this language
rgslPy=["py","python"]

# the sh and python versions here happen to be the same, but this won't work for
# every language; it needs to be parameterized
def assign_py(ln, rgvarToSave):
    iblsh.assign_sh(ln, rgvarToSave)

def get_rgvar_py(rgvarToGet):
    st = "\nwith open(\".tmp-store\") as fd:\n"
    st += "\trgln=[]\n\tfor ln in fd:\n\t\trgln.append(ln)\n"
    iln = 0
    for var in rgvarToGet:
        st += var + " = rgln[" + str(iln) + "].strip()\n" # should we be keeping type info?
        iln += 1
        
    return st

def save_rgvar_py(rgvarToSave):
    st = "\nwith open(\".tmp-store\", \"w\") as fd:\n"
    for var in rgvarToSave:
        st += "\t"
        st += "fd.write(str(" + var + ") + \"\\n\")"
        st += "\n"

    return st
        
def inp_py():
    return inpPy

def rgsl_py():
    return rgslPy
