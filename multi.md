# 多进程介绍

由于CPython实现中的GIL的限制，python中的多线程其实并不是真正的多线程，如果想要充分地使用多核CPU的资源，在python中大部分情况我们需要使用多进程。 这也许就是python中多进程类库如此简洁好用的原因所在。在python中可以向多线程一样简单地使用多进程。

##简单多进程程序

我们先看一个简单的例子，从而对多进程有一个直观的认识：

```python
import multiprocessing as mp
import os, time, random
 
# 子进程要执行的代码
def run_work(ID):
    print('Run process %s (%s)...' % (ID, os.getpid()))
    print('process %s is done' %(ID))
 
if __name__=='__main__':
    print 'Parent process %s.' % os.getpid()
    print 'Process will start.'
    record=[]
    for i in range(3):
    	p = mp.Process(target=run_proc, args=(i,))
    	p.start()
    	record.append(p)
    for p in record:
        p.join()
    print 'Process end.'

#### 结果为####

Parent process 6848.
Process will start.

Run process 0 (4900)...
process 0 is done
Run process 1 (5720)...
process 1 is done
Run process 2 (6508)...
process 2 is done

Process end.


```

multiprocessing 是Python下面支持多进程的模块。进程任务的编类似线程操作，首先是定义一个工作函数(work_fun)，接着是对进程的声明，利用multiprocessing.Process([group[, target[, name[, args[, kargs]]]]])创建新的进程。其中重要的参数如下：

* target:   函数名
* name:     进程名
* args:     函数的参数
* kargs:   	keywords参数
这里，target = work_fun , work_fun函数有ID这个参数，那么args=(i,) 只有一个参数的时候要加上,（tuple形式的参数传入）。声明好进程后，就可以启动进程运行了。启动进程采用 .start()函数。其余Process主要函数有：

* run()                  默认的run()函数调用target的函数，可以在子类中覆盖该函数，重写如何启动
* start()                启动该进程
* join([timeout])        父进程被停止，直到子进程被执行完毕。当timeout为None时没有超时，否则有超时。进程可以被join很多次，但不能join自己

**注意：由于各种问题，python multiprocessing在windows下面编写的时候需要放在if __name__=='__main__': 下避免各种各样的错误 **

run函数时默认执行的，如果不是写子类(class）不需要关注。start函数目的在于启动进程，进程运行完work_fun后自动结束。但不同进程结束时间未必相同，这就需要最后来一个同步：.join()方法，保证子进程全部结束，主进程退出。程序运行完毕。这样一个简单的多进程运行框架就构建完毕了。

### 主进程和子进程的关系
一般来说，主进程运行结束后，子进程未必运行结束，这时候就存在选择，等待所有进程结束，或者主进程结束后子进程也随之结束。所以python多进程中设置了daemon方法，目的在于是否执行主进程结束后，子进程结束的命令。下面两个例子可以直观的告诉我们主进程和子进程的关系：

```python
## daemon 为false ##

import multiprocessing
import time

def worker(interval):
    print("work start:{0}".format(time.ctime()));
    time.sleep(interval)
    print("work end:{0}".format(time.ctime()));

if __name__ == "__main__":
    p = multiprocessing.Process(target = worker, args = (1,))
    p.start()
    print "end of the main process!"


### 结果 ###
#end!
#work start:Tue Apr 21 21:29:10 2015
#work end:Tue Apr 21 21:29:13 2015



import multiprocessing
import time

def worker(interval):
    print("work start:{0}".format(time.ctime()));
    time.sleep(interval)
    print("work end:{0}".format(time.ctime()));

if __name__ == "__main__":
    p = multiprocessing.Process(target = worker, args = (3,))
    p.daemon = True
    p.start()
    print "end of the main process!"

### 结果 ###
#end!

```

主进程结束，子进程随之结束是一个比较安全的做法，但很多时候子进程运行与主进程运行乃至各个子进程间运行速度不一致，如何让主进程最后结束呢？添加join命令即可：

```python
import multiprocessing
import time

def worker(interval):
    print("work start:{0}".format(time.ctime()));
    time.sleep(interval)
    print("work end:{0}".format(time.ctime()));

if __name__ == "__main__":
    p = multiprocessing.Process(target = worker, args = (3,))
    p.daemon = True
    p.start()
    p.join()
    print "end!"

### 结果 ###
#work start:Tue Apr 21 22:16:32 2015
#work end:Tue Apr 21 22:16:35 2015
#end!
```






接下来将会介绍如何将多进程程序写成类的形式。
## 转换为类

```python
import multiprocessing
import time

class ClockProcess(multiprocessing.Process):
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval

    def run(self):
        n = 5
        while n > 0:
            print("the time is {0}".format(time.ctime()))
            time.sleep(self.interval)
            n -= 1

if __name__ == '__main__':
    p = ClockProcess(3)
    p.start()  

#### 结果 ####
#the time is Sat Sep 26 11:10:38 2015
#the time is Sat Sep 26 11:10:41 2015
#the time is Sat Sep 26 11:10:44 2015
#the time is Sat Sep 26 11:10:47 2015
#the time is Sat Sep 26 11:10:50 2015

```

从上面的例子中可以看到，编写子类，需要继承multiprocessing.Process，然后可以重写run函数进行编辑。接下来将会介绍如何利用进程池来操作


## 进程的同步 
进程间运行不可避免会涉及到同步问题，防止进程同时访问某个存储空间造成读写冲突是编写多进程程序一个一个核心问题。multiprocessing 提供了多种方法来帮助我们实现进程间的同步问题：

### lock
利用“锁”（lock）方式来限制同时访问某个内存空间避免出错的方式是多进程操作中常用的同步方法。下面一个例子就是简单的使用lock来限制访问：

```python
from multiprocessing import Process, Lock  
  
def l(lock, num):  
    lock.acquire()  
    print "Hello Num: %s" % (num)  
    lock.release()  
  
if __name__ == '__main__':  
    lock = Lock()  
  
    for num in range(20):  
        Process(target=l, args=(lock, num)).start()  
```

### Semaphore

Semaphore用来控制对共享资源的访问数量，例如池的最大连接数

```python
import multiprocessing
import time

def worker(s, i):
    s.acquire()
    print(multiprocessing.current_process().name + "acquire");
    time.sleep(i)
    print(multiprocessing.current_process().name + "release\n");
    s.release()

if __name__ == "__main__":
    s = multiprocessing.Semaphore(2)
    for i in range(5):
        p = multiprocessing.Process(target = worker, args=(s, i*2))
        p.start()

```


### Event 

Event用来实现进程间同步通信。同步的方式可以利用设定时间来等待同步，也可以利用set函数来进行同步
下面的例子说明了这一点：

```python
import multiprocessing
import time

def wait_for_event(e):
    print("wait_for_event: starting")
    e.wait()
    print("wairt_for_event: e.is_set()->" + str(e.is_set()))

def wait_for_event_timeout(e, t):
    print("wait_for_event_timeout:starting")
    e.wait(t)
    print("wait_for_event_timeout:e.is_set->" + str(e.is_set()))

if __name__ == "__main__":
    e = multiprocessing.Event()
    w1 = multiprocessing.Process(name = "block",
            target = wait_for_event,
            args = (e,))

    w2 = multiprocessing.Process(name = "non-block",
            target = wait_for_event_timeout,
            args = (e, 2))
    w1.start()
    w2.start()

    time.sleep(3)

    e.set()
    print("main: event is set")


### 结果 ###

#wait_for_event: starting
#wait_for_event_timeout:starting
#wait_for_event_timeout:e.is_set->False
#main: event is set
#wairt_for_event: e.is_set()->True
```

### pip
Pipe方法返回(conn1, conn2)代表一个管道的两个端。Pipe方法有duplex参数，如果duplex参数为True(默认值)，那么这个管道是全双工模式，也就是说conn1和conn2均可收发。duplex为False，conn1只负责接受消息，conn2只负责发送消息。
 
send和recv方法分别是发送和接受消息的方法。例如，在全双工模式下，可以调用conn1.send发送消息，conn1.recv接收消息。如果没有消息可接收，recv方法会一直阻塞。如果管道已经被关闭，那么recv方法会抛出EOFError。


```python

import multiprocessing
import time

def proc1(pipe):
    while True:
        for i in range(10):
            print "send: %s" %(i)
            pipe.send(i)
            time.sleep(1)

def proc2(pipe):
    while True:
        print "proc2 rev:", pipe.recv()
        time.sleep(1)

def proc3(pipe):
    while True:
        print "PROC3 rev:", pipe.recv()
        time.sleep(1)

if __name__ == "__main__":
    pipe = multiprocessing.Pipe()
    p1 = multiprocessing.Process(target=proc1, args=(pipe[0],))
    p2 = multiprocessing.Process(target=proc2, args=(pipe[1],))
    #p3 = multiprocessing.Process(target=proc3, args=(pipe[1],))

    p1.start()
    p2.start()
    #p3.start()

    p1.join()
    p2.join()
    #p3.join()


```
### Queue

Queue是多进程安全的队列，可以使用Queue实现多进程之间的数据传递。put方法用以插入数据到队列中，put方法还有两个可选参数：blocked和timeout。如果blocked为True（默认值），并且timeout为正值，该方法会阻塞timeout指定的时间，直到该队列有剩余的空间。如果超时，会抛出Queue. Full异常。如果blocked为False，但该Queue已满，会立即抛出Queue.Full异常。
 
get方法可以从队列读取并且删除一个元素。同样，get方法有两个可选参数：blocked和timeout。如果blocked为True（默认值），并且timeout为正值，那么在等待时间内没有取到任何元素，会抛出Queue.Empty异常。如果blocked为False，有两种情况存在，如果Queue有一个值可用，则立即返回该值，否则，如果队列为空，则立即抛出Queue.Empty异常。 

```python

import multiprocessing

def writer_proc(q):      
    try:         
        q.put(111, block = False) 
    except:         
        pass   

def reader_proc(q):      
    try:         
        print q.get(block = False) 
    except:         
        pass

if __name__ == "__main__":
    q = multiprocessing.Queue()
    writer = multiprocessing.Process(target=writer_proc, args=(q,))  
    writer.start()   

    reader = multiprocessing.Process(target=reader_proc, args=(q,))  
    reader.start()  

    reader.join()  
    writer.join()

```

## 进程池pool 
利用Python并行操作可以节约大量的时间。当被操作对象数目不大时，可以直接利用multiprocessing中的Process动态成生多个进程，10几个还好，但如果是上百个，上千个目标，手动的去限制进程数量却又太过繁琐，这时候我们就可以利用进程池pool来操作了。Pool可以提供指定数量的进程，供用户调用，当有新的请求提交到pool中时，如果池还没有满，那么就会创建一个新的进程用来执行该请求；但如果池中的进程数已经达到规定最大值，那么该请求就会等待，直到池中有进程结束，才会创建新的进程来它。首先来看一个简单的例子

```python

import multiprocessing
import time

def func(ID):
    print("ID: %d", % ID)
    time.sleep(3)
    print("end of process %s" % os.getpid())

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes = 3)
    for i in range(4):
        pool.apply_async(func, (i, ))   #维持执行的进程总数为processes=3，当一个进程执行完毕后会添加新的进程进去

    print "starting the pool !!!"
    pool.close()
    pool.join()   
    #调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束

    print("Sub-process(es) done.")


```

关键函数解释：
* apply_async(func[, args[, kwds[, callback]]]) 它是非阻塞运行与之相对应的是apply(func[, args[, kwds]])是阻塞的，也就是说运行完一个再运行下一个，
* close()    关闭pool，使其不在接受新的任务。
* terminate()    结束工作进程，不在处理未完成的任务。
* join()    主进程阻塞，等待子进程的退出， join方法要在close或terminate之后使用。


创建一个进程池pool，并设定进程的数量为3，xrange(4)会相继产生四个对象[0, 1, 2, 4]，四个对象被提交到pool中，因pool指定进程数为3，所以0、1、2会直接送到进程中执行，当其中一个执行完事后才空出一个进程处理对象3。因为非阻塞，主函数执行独立于进程的执行，所以运行完for循环后直接输出“starting the pool !!!”，主程序在pool.join（）处等待各个进程的结束。若为阻塞的例子：


```python

#coding: utf-8
import multiprocessing
import time

def func(ID):
    print("ID: %d", % ID)
    time.sleep(1)
    print("end of process %s" % os.getpid())

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes = 3)
    for i in range(4):
        pool.apply(func, (i, ))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去

    print "starting the pool !!!"
    pool.close()
    pool.join()   #调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    print "Sub-process(es) done."


```


若想返回各个进程的结果该如何操作呢？可以利用如下的例子，这告诉我们，利用pool我们可以实现并行计算。

```python
import multiprocessing
import time,os

def func(ID):
    print("ID: %d" % ID)
    time.sleep(1)
    print("end of process %s" % os.getpid())
    return "done"+ str(ID)

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=4)
    result = []
    for i in xrange(10):
        result.append(pool.apply_async(func, (i, )))
    pool.close()
    pool.join()
    for res in result:
        print ":::", res.get()
    print("Sub-process(es) done.")

```

使用多个函数来进行计算的例子：

```python
import multiprocessing
import os, time, random

def worker_1(interval):
    print "worker_1"
    time.sleep(interval)
    print "end worker_1"

def worker_2(interval):
    print "worker_2"
    time.sleep(interval)
    print "end worker_2"

def worker_3(interval):
    print "worker_3"
    time.sleep(interval)
    print "end worker_3"

if __name__=='__main__':
    function_list=  [worker_1,worker_2,worker_3] 
    print "parent process %s" %(os.getpid())

    pool=multiprocessing.Pool(4)
    for func in function_list:
        pool.apply_async(func,args=(1,))     #Pool执行函数，apply执行函数,当有一个进程执行完毕后，会添加一个新的进程到pool中

    print 'Waiting for all subprocesses done...'
    pool.close()
    pool.join()    #调用join之前，一定要先调用close() 函数，否则会出错, close()执行后不会有新的进程加入到pool,join函数等待素有子进程结束
    print 'All subprocesses done. exiting ...'
```


## 利用Queue 多进程并发运行处理数据

从前面我们知道，Queue是一个非常方便的进行进程间数据传输的工具，而同时我们也可以利用Queue这个特性来进行数据流的多进程并发设计,这里的关键在于如何设置退出机制，先学习一个例子：

```python

import multiprocessing
import time

class work_process(multiprocessing.Process):
   
   def __init__(self, task_queue, result_queue,flag):
       multiprocessing.Process.__init__(self)
       self.task_queue = task_queue # 任务队列
       self.result_queue = result_queue  # 结果队列
       self.flag=flag # 退出标记

   def run(self):
       proc_name = self.name
       while True:  # 循环进行
           next_task = self.task_queue.get()   # 获取任务队列的数据
           print('flag is %d' %self.flag)
           if next_task is None:               ### 退出机制设计
               # Poison pill means shutdown
               print ('%s: Exiting' % proc_name)
               self.task_queue.task_done()
               break
           print ('%s: %s' % (proc_name, next_task))
           answer = next_task() # __call__()
           self.task_queue.task_done()
           self.result_queue.put(answer)  #存储记录
       print('proces is done')
       return


class Task(object):
   def __init__(self, a, b):
       self.a = a
       self.b = b
   def __call__(self):  ## we can use Task() to excute this method
       return '%s * %s = %s' % (self.a, self.b, self.a * self.b)
   def __str__(self):
       return '%s * %s' % (self.a, self.b)


if __name__ == '__main__':
   # Establish communication queues
   tasks = multiprocessing.JoinableQueue()
   results = multiprocessing.Queue()
   flag=[0]
   # Start process
   num_process = multiprocessing.cpu_count()
   print ('Creating %d consumers' % num_process)
   record = [ work_process(tasks, results,flag[0])
                 for i in range(2) ]
   for w in work_process:
       w.start()
   
   # Enqueue jobs
   num_jobs = 10
   for i in range(num_jobs):
       tasks.put(Task(i, i+1))
   
   # Add a exit mechanism for each thread
   for i in range(4):
       tasks.put(None)

   flag[0]=1
   # Wait for all of the tasks to finish
   tasks.join()


   
   # Start printing results
   while num_jobs:
       result = results.get()
       print ('Result:', result)
       num_jobs -= 1




```

从上面可以看到，程序中添加了两个退出机制的选择，但只有一个有效,就是利用queue在最后设置退出机制。那么我们可以从此知道如何在多进程情况下设置退出机制然后进行queue队列的并行计算。值得注意的是，tasks.join() 必须是JoinableQueue() 这个quene下面才能使用，同时，要避免出错必须加上在工作函数中加上self.task_queue.task_done()这个命令才行。否则就会出bug!

