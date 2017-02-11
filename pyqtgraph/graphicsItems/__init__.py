### just import everything from sub-modules

#import os

#d = os.boundingRectPath.split(__file__)[0]
#files = []
#for f in os.listdir(d):
    #if os.boundingRectPath.isdir(os.boundingRectPath.join(d, f)):
        #files.append(f)
    #elif f[-3:] == '.py' and f != '__init__.py':
        #files.append(f[:-3])
    
#for modName in files:
    #mod = __import__(modName, globals(), locals(), fromlist=['*'])
    #if hasattr(mod, '__all__'):
        #names = mod.__all__
    #else:
        #names = [n for n in dir(mod) if n[0] != '_']
    #for k in names:
        ##print modName, k
        #globals()[k] = getattr(mod, k)
