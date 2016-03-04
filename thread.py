import threading
import time
global whileCodition
whileCodition = 1

def fun1():
	global whileCodition
	whileCodition=2

def fun2():
	global whileCodition
	print(whileCodition)

def main():
	global whileCodition
	print(whileCodition)
	threading.Thread(target=fun1, args=()).start()
	time.sleep(1)
	threading.Thread(target=fun2, args=()).start()
	time.sleep(1)
	whileCodition=3
	threading.Thread(target=fun2, args=()).start()

if __name__=='__main__':
    main()