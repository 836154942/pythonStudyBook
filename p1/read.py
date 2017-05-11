import os
from os.path import join, getsize     

def fun():
        with open("D:\\sslkeylogout.log","r") as f:
                count =0
                s=0
                size = getsize("D:\\sslkeylogout.log")
                print("size是 %s" %  size)
                while count < size:
                        print(f.read(1024*512))
                        print(str(s) +"读取了一次@#￥￥%*~@￥……&（&……*￥&￥%……*￥%……*￥%……*￥%*￥%*……￥%")

                        s+=1
                        count +=1024*512


                print("最后的结果是" +str(s))
                f.close()

fun()
