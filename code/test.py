import os
import matplotlib.pyplot as plt
import time


#path to recognition results
r = 'Result/dev'

#Exist before script is run
config = 'cfgs/config_tr'

mlist_sp = 'word.list'
MLF = 'label/dev.ref.mlf'
devlist = 'scp/devlist'
testlist = 'scp/testlist'

#Made in script
grammar = 'grammar'
lexicon = 'scp/lexicon.dct'
wordnet = 'wordnet'
devout = r+'/devout.mlf'
testout = 'Result/testout.mlf'
result = r+'/result.res'
res_list = r+'/res_list'
res_arr = []

def main():
    Makedir(r)
    Makegra(grammar)
    Makedct(lexicon)
    #make grammar file in htk format
    os.popen("HParse %s %s" % (grammar, wordnet))
    
    '''
    #uncomment this part if you want to tune t
    res_arr = []
    for i  in range(0, 300, 20):
	print i
	os.popen('HVite -T 1 -A -D -H models/hmm164/hmmdefs -S '+devlist+' -C '+config+' -w '+wordnet+" -l '*' -i "+devout+' -p 0.0 -s 0.0 -t '+str(i)+' ' +lexicon+' '+ mlist_sp)
	os.popen('HResults -h -e "???" sil -e "???" sp -I '+ MLF +' '+ mlist_sp+' '+ devout+' >'+result)  
	res_arr.append([str(i)] + sent_err(result))
    save_res(res_arr)  
    plot_res(res_arr)
    '''    
    
    '''
    #uncomment this part if you want to tune s
    res_arr = []
    for i  in range(0, 20, 1):
	print i
	os.popen('HVite -T 1 -A -D -H models/hmm164/hmmdefs -S '+devlist+' -C '+config+' -w '+wordnet+" -l '*' -i "+devout+' -p 0.0 -t 0.0 -s '+str(i)+' ' +lexicon+' '+ mlist_sp)
	os.popen('HResults -h -e "???" sil -e "???" sp -I '+ MLF +' '+ mlist_sp+' '+ devout+' >'+result)  
	res_arr.append([str(i)] + sent_err(result))
    save_res(res_arr)  
    plot_res(res_arr)
    '''
    
    '''
    #uncomment this part if you want to tune p
    #different p
    res_arr = []
    for i  in range(0, -150, -10): 
	print i
	os.popen('HVite -T 1 -A -D -H models/hmm164/hmmdefs -S '+devlist+' -C '+config+' -w '+wordnet+" -l '*' -i "+devout+' -p '+str(i)+' -s 0.0 -t 0.0 '+lexicon+' '+ mlist_sp)
	os.popen('HResults -h -e "???" sil -e "???" sp -I '+ MLF +' '+ mlist_sp+' '+ devout+' >'+result)
	
	res_arr.append([str(i)] + sent_err(result))
    save_res(res_arr)
    plot_res(res_arr)
    '''
    
    '''
    #uncomment this part if you want to tune the number of mixs
    print ' ...run recogniser'    
    for i in range(2, 19):
	print i
	os.popen('HVite -T 1 -A -D -H models/hmm'+str(10*i+6)+'/hmmdefs -S '+devlist+' -C '+config+' -w '+wordnet+" -l '*' -i "+devout+' -p -100.0 -s 0.0 '+ lexicon+' ' +mlist_sp)
	os.popen('HResults -h -e "???" sil -e "???" sp -I '+ MLF +' '+ mlist_sp+' '+ devout+' >'+result)     
	res_arr.append([str(i)] + sent_err(result))       
    save_res(res_arr)	
    plot_res(res_arr)
    '''    
    
    os.popen('HVite -T 1 -A -D -H models/hmm164/hmmdefs -S '+testlist+' -C '+config+' -w '+wordnet+" -l '*' -i "+testout+' -p -100.0 -s 0.0 '+lexicon+' '+ mlist_sp)
    
    
def Makedir(targetdir):
    if os.path.isdir(targetdir) is False:
        os.makedirs(targetdir)
 
def MakeList(innfile, outfile):
    #Read list of all dev files
    innfile = file(innfile, 'r')
    filelist = innfile.readlines()
    innfile.close()
    out = []
    for line in filelist:
        line = line.split()[1]
        out.append(line+'\n')
        
        
    #write outfile
    outfile = file(outfile, 'w')
    outfile.writelines(out)
    outfile.close()
   
def Makegra(grafile):
    innfile = file(grafile, 'w')
    innfile.write('$digit=one | two | three | four | five | six | seven | eight | nine | oh | zero;\n')
    innfile.write('(sil < ( <$digit> ) [sp]> sil)\n')
    innfile.close()
    return 

def Makedct(lexfile):
    file_read = file(mlist_sp, 'r')
    filelist = file_read.readlines()
    file_read.close()
    innfile = file(lexfile, 'w')
    for line in filelist:
	innfile.write(line[:-1] +' ' + line)
    innfile.close()
    return 

def sent_err(res_file):
    res = file(res_file, 'r')
    flist = res.readlines()
    res.close()
    serr = flist[7].split()[-2]
    err = flist[7].split()[-3]
    return [err, serr]

def save_res(res_array):
    innfile = file(res_list, 'w')
    for t in res_array:
	innfile.write(' '.join(t) +'\n')
    innfile.close()
    return 

def plot_res(res_array):
    fig = plt.figure()
    ax = plt.subplot(111)
    x = []
    y = []
    z = []
    for t in res_array:
	x.append(int(t[0]))
	y.append(float(t[1]))
	z.append(float(t[2]))	
    ax.plot(x, y,label='$word$',color = 'r')
    ax.plot(x, z, label='$sent$',color = 'g') 
    
    ax.set_xlabel('Number of mixs')
    ax.set_ylabel('Error (%)')   
    ax.legend()
    plt.show()
    return 

def plot_res2(res_array):
    fig = plt.figure()
    ax = plt.subplot(111)
    colors = ['r', 'g', 'b', 'k']
    for i in range(2,6):
	x1 = []
	y1 = []
	for j in range(6*(i-2), 6*(i-1)):
	    x1.append(int(res_array[j][0]))
	    y1.append(float(res_array[j][1]))	
	
	ax.plot(x1, y1, label=str(i+4)+'-mix', color = colors[i-2])

    ax.set_xlabel('Iteration')
    ax.set_ylabel('Error (%)')
    ax.legend()
    plt.show()
    return 
    
if __name__ == "__main__":
    main()
