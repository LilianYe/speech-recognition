import os
import sys

#Main directory for database
wavedir = 'audio/train'
wavedir_dev = 'audio/dev'
wavedir_test = 'audio/test'
#Main directory for feature files
featuredir = 'features/train'
featuredir_dev = 'features/dev'
featuredir_test = 'features/test'

#Exist before script is run
config = 'cfgs/config_hcopy'
files = 'mapping/train.mapping'
files_dev = 'mapping/dev.mapping'
files_test = 'mapping/test.mapping'

#Made in script
hcopy = 'scp/hcopy.scp'
hcopy_dev = 'scp/hcopy_dev.scp'
hcopy_test = 'scp/hcopy_test.scp'

trainlist = 'scp/trainlist'
devlist = 'scp/devlist'
testlist = 'scp/testlist'


def main():
    Makedir('scp')
    Makedir(featuredir)
    Makedir(featuredir_dev)
    Makedir(featuredir_test)
    
    MakeListandDir(files,featuredir,wavedir,hcopy,trainlist)
    MakeListandDir(files_dev,featuredir_dev,wavedir_dev,hcopy_dev,devlist)
    MakeListandDir(files_test,featuredir_test,wavedir_test,hcopy_test,testlist)
    
    #FrontEnd with HCopy
    os.popen('HCopy -C '+config+' -S '+hcopy)
    os.popen('HCopy -C '+config+' -S '+hcopy_dev)
    os.popen('HCopy -C '+config+' -S '+hcopy_test)

def MakeListandDir(scriptfile,featuredir,wavdir,outfile_a, outfile_b):
    scriptfile = file(scriptfile,'r')
    filelist = scriptfile.readlines()
    scriptfile.close()
    out_a = []
    out_b = []
    for line in filelist:
        line = line.split()[0]
        sourcefile = wavdir+'/'+line
        targetfile = featuredir+'/'+line.replace('.08','.mfc')
        out_a.append(sourcefile+' '+targetfile+'\n')
        out_b.append(targetfile+'\n')
          
    #Writes outfile_a
    outfile_a = file(outfile_a, 'w')
    outfile_a.writelines(out_a)
    outfile_a.close()
    
    #Writes outfile_b
    outfile_b = file(outfile_b, 'w')
    outfile_b.writelines(out_b)
    outfile_b.close()
    return

# make a new directory if not exists
def Makedir(targetdir):
    if os.path.isdir(targetdir) is False:
        os.makedirs(targetdir)

if __name__ == "__main__":
    main()
