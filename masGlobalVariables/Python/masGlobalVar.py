vars={}
def setVar(var, value=None):
    vars[var]= value
def getVar(var):
    try:
        return vars[var]
    except:
        return None