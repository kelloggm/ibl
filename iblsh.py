# @ Martin Kellogg, June 2016

# This file contains all of ibl's bash stuff
# Hopefully we can build one of these for each language we decide to support

# all the possible annotations that invoke the bash interpreter
rgslSh=["bash","sh"]

# the default location of the bash interpreter
inpSh = "/bin/bash"

def assign_sh(ln, rgvarToSave):
    if ln.strip().startswith("#"):
        return
    if "=" in ln:
        rgln = ln.strip().split("=")
        if " " not in rgln[0].strip():
            var = rgln[0]
            if var not in rgvarToSave:
                rgvarToSave.append(var)

def get_rgvar_sh(rgvarToGet):
    iln = 1
    st = "\n"
    for var in rgvarToGet:
        st += var.strip() + "=`sed '"+ str(iln) + "q;d' tmp-store`\n"
        iln += 1
        
    return st

def save_rgvar_sh(rgvarToSave):
    st = "\nrm tmp-store;touch tmp-store;"
    for var in rgvarToSave:
        st += "echo $" + var + " >> tmp-store;"

    return st

def inp_sh():
    return inpSh

def rgsl_sh():
    return rgslSh
