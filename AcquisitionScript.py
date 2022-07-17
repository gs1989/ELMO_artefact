import subprocess
import random
import numpy as np

def write_inputs(data):
   out=open('inputs.txt','w')
   for i in range(len(data)):
   	out.writelines("{0:2x}\n".format(data[i]))
   out.close();
def read_outputs(length):
    out=open("outputs.txt",'r');
    data=[0]*length
    for i in range(length):
       data[i]=int(out.readline(),16)
    return data
def read_trace(length):
    out=open("output/traces/trace00001.trc",'r');
    data=[0.0]*length
    for i in range(length):
       data[i]=float(out.readline())
    return data

if __name__ == '__main__':
    plain=[0x32, 0x43, 0xf6, 0xa8, 0x88, 0x5a, 0x30, 0x8d, 0x31, 0x31, 0x98, 0xa2, 0xe0, 0x37, 0x07, 0x34]
    N=1000
    maxlen=1000
    inputs=np.zeros((N,16),dtype='uint8')
    outputs=np.zeros((N,16),dtype='uint8')
    traces=np.zeros((N,maxlen))
    for k in range(N):
        if(k%100==0):
            print("Trace {0}".format(k))
        #Generate the inputs
        inputs[k,:]=[random.randint(0, 255) for i in range(0, 16)]
        write_inputs(inputs[k,:]);
        #Run ELMO once
        cmd="./elmo Examples/tinyAES/main.bin -noisestd 1 -randominterval 100 -randomdelay 5 >/dev/null  2>/dev/null"
        subprocess.run(cmd,shell=True)
        #Read back the outputs
        outputs[k,:]=read_outputs(16)
        #Read back one trace
        traces[k,:]=read_trace(maxlen)
    #Storing output npz
    np.savez("TinyAES_Traces.npz",input=inputs,output=outputs,trace=traces,noisestd=1,randominterval=100,randomdelay=5)
    r=np.load("TinyAES_Traces.npz")
    #for i in range(16):
    #    print("{0}\n".format(r['trace'][999,i]))
    #print("randominterval={0}\n".format(r['randominterval']))
    

