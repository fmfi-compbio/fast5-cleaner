#! /usr/bin/python3
import h5py
import os
import sys

if len(sys.argv)<3:
    print("Usage: %s source_tree dest_tree" % sys.argv[0],file=sys.stderr)
    sys.exit(1)
    
sourcedir = sys.argv[1]
targetdir = sys.argv[2]

def remove_analysis(source, target):
    if not source.endswith('.fast5'):
        return

    try:
        f = h5py.File(source,"r")
        g = h5py.File(target,"w")

        for key in list(f.keys()):
            if key != 'Analyses':
                f.copy(key,g)

        for item in f.attrs.items():
            g.attrs.create(item[0],item[1])

        f.close()
        g.close()


    except:
        print('bad file?',file=sys.stderr)
                
    
##############

for dir, subdirs, files in os.walk(sourcedir):
    for file in files:
        rel = os.path.relpath(dir, sourcedir)
        targetpath = os.path.join(targetdir, rel)
        os.makedirs(targetpath, exist_ok=True)
        print('%s' % os.path.join(targetpath,file),file=sys.stderr)
        remove_analysis(os.path.join(dir, file), 
                        os.path.join(targetpath, file))



