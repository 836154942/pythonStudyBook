def move(n,f,t):
    print("把第%d个盘子从第%s 移动到 %s "%(n,f,t))

#from to  help
def change(n,f,t,h):
    if n==1:
        move(n,f,t)
    else :
        change(n-1,f,h,t)
        move(n,f,t)
        change(n-1,h,t,f)

    
    
def start():
    res =input("请输入有几个盘子")
    number = int(res)
    change(number,f="A",t="C",h="B")
