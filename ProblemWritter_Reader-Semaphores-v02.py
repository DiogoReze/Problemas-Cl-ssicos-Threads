'''
Código retirado e modificado de: https://codereview.stackexchange.com/questions/219766/first-readers-writers-problem-using-a-single-condition?fbclid=IwAR0RCwVMfuGtKAj6ZM5ji4eyhVhnrhWjWFdDlDr83AU56c9VDLNYoLaLLJU

http://cocic.cm.utfpr.edu.br/progconcorrente/doku.php?id=python
'''
import threading
import time

'''
classe criada apenas para o recurso compartilhado
'''
 
class SharedResource:
    def __init__(self):
        self.val = 0
 
'''
classe principal, no qual é realizado os bloqueios e desbloqueios
'''
 
class RWLock:
    #construtor
    def __init__(self):
        self.readers = 0
        self.mutex = threading.Semaphore(1) #Semáforo de leitura
        self.lock = threading.Semaphore(1)  #Semáforo de escrita
 
    def read_acquire(self):
        self.mutex.acquire() #bloqueia para leitura
        self.readers += 1 #soma a quantidade de leitores
        if self.readers == 1:
            self.lock.acquire() #Se você é o primeiro leitor, bloqueie o recurso dos escritores.
                                # Recurso permanece reservado para leitores subseqüentes
        self.mutex.release() # desbloqueia
 
    def read_release(self):
        self.mutex.acquire() #bloqueia para leitura
        self.readers -= 1
        if self.readers == 0:
            self.lock.release() #Se você for o último leitor, poderá desbloquear o recurso. 
                                # Isso torna disponível para escritores.
        self.mutex.release() #desbloqueia
 
    def write_acquire(self):
        self.lock.acquire() #bloqueia o semaforo de escrita
 
    def write_release(self):
        self.lock.release() #desbloqueia
 
 
def read(lock, res):
    lock.read_acquire()
    print(threading.current_thread().ident, "Reading:", res.val)
    time.sleep(0.5)
    lock.read_release()
 
 
def write(lock, res):
    lock.write_acquire()
    print(threading.current_thread().ident, "Writing")
    res.val += 1
    time.sleep(2)
    lock.write_release()
 
if __name__ == '__main__':
 
    lock = RWLock()
    res = SharedResource()
 
    #criação dos escritores
    writer = threading.Thread(target=write, args=(lock, res,))
    writer2 = threading.Thread(target=write, args=(lock, res,))
    writer3 = threading.Thread(target=write, args=(lock, res,))
 
    #criação dos leitores
    reader = threading.Thread(target=read, args=(lock, res,))
    reader2 = threading.Thread(target=read, args=(lock, res,))
    reader3 = threading.Thread(target=read, args=(lock, res,))
    reader4 = threading.Thread(target=read, args=(lock, res,))
 
    writer.start()
    reader.start()
    writer2.start()
    writer3.start()
    reader2.start()
    reader3.start()
    reader4.start()