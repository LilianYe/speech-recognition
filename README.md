# speech-recognition


This is a digit recognition experiment. You will build a system from scratch,
i.e. from feature extraction to decoding, using the HTK toolkit HTK.
All binary needed are in the directory "bin/"

1. The audios in "audio/train/" are used to train acoustic models  and in "audio/dev" 
   are used to test the performance of your model. You can evaluate the decoding result 
   by comparing your output text with "labels/dev.ref.mlf" using HResults in HTK.

2. "labels/train.all.mlf" and "labels/train.nosp.mlf" are the label files of training 
   audios and their differences lie in whether there is "sp" which means short pause 
   between digits.The mapping files between audio names and their corresponding label 
   names can be found in "mapping".

3. The file "wordlist" is the list of words appeared in the "labels/train.all.mlf".

4. The configure files you may need in the training process are in "cfgs/"

5. Attention! You need to record the procedure of your experiment. So create a README 
   file to record the commands you used and your annotations according to which the 
   teacher and TA will check if you are doing the right procedure. By the way, you can 
   save the information output by the command executing process with command "tee".
   eg. HCopy -A -D -T 1 -C config -S scp | tee hcopy.log

6. Please email your project report to the TA.
   The project report should include:

   * Detailed description of how you choose the model parameters and relevant dev results.
   * Results of the files in "audio/test/" using your best model.

