import numpy as np
import time
#生成一组测试数据
n=100
middle=int(n/2)
data=np.ones((n,6))
filenameA= 'd:\\user_special\\VSCODE_Python\\DaChuangGUI\\data\\dataA.txt'
filenameB= 'd:\\user_special\\VSCODE_Python\\DaChuangGUI\\data\\dataB.txt'
# 清空文件内容
file=open(filenameA,'w').close()
file=open(filenameB,'w').close()

start_time = time.time()

while True:
    data[:,0]=np.arange(0,n,1)
    data[:middle,1]=20+np.random.random([middle])*160
    data[middle:,1]=70+np.random.random([middle])*20
    data[:,2]=-2.465351
    data[:,3]=0.607373
    data[:,4]=50.00000
    data[:,5]=2400

    with open(filenameA, 'a+') as f:
        for i in range(middle):
            for j in range(6):
                f.write(str(data[i,j]))
                f.write(' ')
            f.write('\n')
    with open(filenameB, 'a+') as f:
        for i in range(middle):
            for j in range(6):
                f.write(str(data[i+middle,j]))
                f.write(' ')
            f.write('\n')
    now_time = time.time()
    # 若运行时间超过分钟
    if (now_time - start_time) >(5*60):
        break