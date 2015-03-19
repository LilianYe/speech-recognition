import os
import sys
import time
import matplotlib.pyplot as plt

#main directory
m = 'models'

#config file for training 
config = 'cfgs/config_tr'
#Feature type
targetkind = "MFCC_E_D_A"
#Number of parameters
numbpar=39

#Exist before script is run
trainlist = 'scp/trainlist'
MLF_nosp = 'label/train.nosp.mlf'
MLF = 'label/train.all.mlf'
mlist = 'word.nosp.list'
mlist_sp = 'word.list'

#Made in script
proto_word = 'proto5'
tmpmixhed = 'scp/tmpmixhed.hed'
silfile = 'scp/sil.hed'

#Vocabulary
voc = ['eight','five','four','nine','oh','one','seven','sil','six','three','two','zero']

#Final number of mixtures
nummix   = 4
nummix_sp = 64

def main():
    Makedir(m+'/hmm0')
    MakeProto(proto_word)
    #Update the means and variances of the proto file using the training data
    os.popen('HCompV -C '+config+' -f 0.10 -m -S '+trainlist+' -M '+m+' '+proto_word) 
    
    newproto=m+"/"+proto_word
    
    #Convert the updated proto files to a hmm model file "hmmdefs" and a macro file "macros"   
    MakeHmmdefs(voc,newproto,targetkind,str(numbpar),m+'/hmm0')
    
    # nosp mode
    for mix in range(4,nummix+1,4):
        olddir = m+'/hmm'+str(mix-4)
        newdir = m+'/hmm'+str(mix)
        Makedir(newdir)
        MakeEditFile(mix,tmpmixhed)
        #Retrain models
        os.popen('HERest -A -T 1 -D -C '+config+' -I '+MLF_nosp+' -t 250.0 150.0 1000.0 -S '+trainlist+' -H '+olddir+'/hmmdefs -M '+newdir+' '+mlist)
        os.popen('HERest -A -T 1 -D -C '+config+' -I '+MLF_nosp+' -t 250.0 150.0 1000.0 -S '+trainlist+' -H '+newdir+'/hmmdefs -M '+newdir+' '+mlist)
        os.popen('HERest -A -T 1 -D -C '+config+' -I '+MLF_nosp+' -t 250.0 150.0 1000.0 -S '+trainlist+' -H '+newdir+'/hmmdefs -M '+newdir+' '+mlist)
    
    
    oldhmm = m+'/hmm'+str(nummix)+'/hmmdefs'
    newhmm = m+'/hmm'+str(nummix)+'/hmmdefs_sp'
    MakeNewHmmdefs(newhmm, oldhmm)
    Makesil(silfile)
    Makedir(m+'/hmm10')
    os.popen('HHEd -D -A -T 2 -H '+ newhmm+ ' -w models/hmm10/hmmdefs '+silfile+' '+mlist_sp)
    
    # sp mode  
    for i in range(11, 17):
	j = i - 1
	olddir = m+'/hmm'+str(j)
	newdir = m+'/hmm'+str(i)
	Makedir(newdir)	
	os.popen('HERest -A -T 1 -D -C '+config +' -I '+MLF+' -t 250.0 150.0 1000.0 -S '+ trainlist+' -H '+olddir+'/hmmdefs -M '+ newdir + ' ' + mlist_sp)
    
    for i in range(2, 19):
	edfile = 'edfiles/edfile.mu.'+str(i)
	Makedir('edfiles')
	MakeEditFile_sp(i,edfile)
    
    for i in range(2,19):
	print 'Expand to :'+str(i)+' mixtures'
	newdir = m+'/hmm'+str(i)+'0' 
	olddir = m+'/hmm'+str(i-1)+'6'
	Makedir(newdir)
	os.popen('HHEd -D -A -T 2 -H '+ olddir+ '/hmmdefs -w '+ newdir + '/hmmdefs edfiles/edfile.mu.'+str(i)+' '+mlist_sp)
	
	for j in range(10*i+1, 10*i+7):
	    newdir2 = m+'/hmm'+str(j)
	    olddir2 = m+'/hmm'+str(j-1)
	    Makedir(newdir2)
	    os.popen('HERest -A -T 1 -D -C '+ config+' -I '+MLF+' -t 250.0 150.0 1000.0 -S '+trainlist+' -H '+olddir2+'/hmmdefs -M '+ newdir2+' '+mlist_sp) 
	          
def Makedir(targetdir):
    if os.path.isdir(targetdir) is False:
        os.makedirs(targetdir)
        
def MakeMacro(target, number, dir):
    """Make macro file from vFloors"""
    vFloors=open(dir+'/vFloors').read()
    macro=open(dir+'/hmm0/macros','w')

    print >> macro, "~o\n<VECSIZE> "+number+"\n<"+target+">"
    print >> macro, vFloors,
    
def MakeHmmdefs(voclist, newproto, target, number, dir):
    """Make hmmdefs from proto file and a vocabulary list"""
    hmmdefs=open(dir+"/hmmdefs","w")
    print >> hmmdefs, "~o\n<STREAMINFO> 1 "+number+"\n<VECSIZE> "+number+"<NULLD><"+target+"><DIAGC>"
    for word in voclist:
        proto=open(newproto)
        for i,line in enumerate(proto):
            if i<3: continue
            elif i==3:
                print >> hmmdefs, "~h \""+word+"\""
            else:
                print >> hmmdefs, line,
        proto.close()
        
def MakeEditFile(nummix,mixhed):
    mixhed = file(mixhed, 'w')
    mixhed.write('\
    MU '+str(nummix)+'{eight.state[2-4].mix}\n\
    MU '+str(nummix)+'{five.state[2-4].mix}\n\
    MU '+str(nummix)+'{four.state[2-4].mix}\n\
    MU '+str(nummix)+'{nine.state[2-4].mix}\n\
    MU '+str(nummix)+'{oh.state[2-4].mix}\n\
    MU '+str(nummix)+'{one.state[2-4].mix}\n\
    MU '+str(nummix)+'{seven.state[2-4].mix}\n\
    MU '+str(nummix)+'{sil.state[2-4].mix}\n\
    MU '+str(nummix)+'{six.state[2-4].mix}\n\
    MU '+str(nummix)+'{three.state[2-4].mix}\n\
    MU '+str(nummix)+'{two.state[2-4].mix}\n\
    MU '+str(nummix)+'{zero.state[2-4].mix}\n\
    ')
    mixhed.close()
    return

def MakeEditFile_sp(nummix,mixhed):
    mixhed = file(mixhed, 'w')
    mixhed.write('\
    MU '+str(nummix)+'{*.state[2-17].mix}\n\
    MU '+str(nummix*2)+ '{sil.state[2-4].mix}\n\
    MU '+str(nummix*2)+ '{sp.state[2].mix}\n\
    ')
    mixhed.close()
    return

def MakeProto(protofile):
    proto = file(protofile, 'w')
    repeat = '<Mean> 39\n' + '0.0 '*38+'0.0\n'+'<Variance> 39\n'+'1.0 '*38+'1.0\n'
    proto.write('\
    <BeginHMM>\n' +'\
    <VECSIZE> 39 <MFCC_E_D_A>\n' + '\
    <NumStates> 5\n' + '\
    <State> 2\n' + repeat +  '\
    <State> 3\n' + repeat +  '\
    <State> 4\n' + repeat +  '\
    <TransP> 5\n' + '\
    0.00 1.00 0.00 0.00 0.00\n' + '\
    0.00 0.60 0.40 0.00 0.00\n' + '\
    0.00 0.00 0.60 0.40 0.00\n' + '\
    0.00 0.00 0.00 0.70 0.30\n' + '\
    0.00 0.00 0.00 0.00 0.00\n' +'\
    <EndHMM>\n')
    proto.close()
    return

def Makesil(sil_file):
    sil = file(sil_file, 'w')
    sil.write('MU 2 {sil.state[2-4].mix}\n')
    sil.write('AT 2 4 0.2 {sil.transP}\n')
    sil.write('AT 4 2 0.2 {sil.transP}\n')
    sil.write('AT 1 3 0.3 {sp.transP}\n')
    sil.write('TI silst {sil.state[3],sp.state[2]}\n\n')
    sil.close()
    return 

def MakeNewHmmdefs(newfile, oldfile):
    fileread = file(oldfile, 'r')
    filewrite = file(newfile, 'w')
    filelist = fileread.readlines()
    fileread.close()
    writeout = []
    writemode = False
    
    for line in filelist:
        filewrite.write(line)
        if line == '~h "sil"\n':
            writemode = True
        if writemode == True:
            writeout.append(line)
        if writemode == True and line == '<ENDHMM>\n':
            writemode =False
    out = []
    out.append('~h "sp"\n')
    out.append(writeout[1])
    out.append('<NUMSTATES> 3\n')
    
    for line in writeout:
        if line == '<STATE> 4\n':
            writemode = False
        if writemode == True:
            out.append(line)        
        if line == '<STATE> 3\n':
            writemode = True
            out.append('<STATE> 2\n')
    
    out.append('<TRANSP> 3\n')
    out.append(' '.join(writeout[-6].split()[:3])+'\n')
    out.append(' '.join(writeout[-5].split()[:3])+'\n')
    out.append(' '.join(writeout[-2].split()[:3])+'\n')
    out.append('<ENDHMM>\n')
    filewrite.writelines(out)
    filewrite.close()
    return 
    
if __name__ == "__main__":
    main()
