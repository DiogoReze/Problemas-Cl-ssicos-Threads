import threading
import time
 
 #Write-Reader Problem in Python - using semaphores

class ReaderWriterProblem():
    def __init__(self):
        self.mutex = threading.Semaphore()  
        self.wrt = threading.Semaphore()  
        self.r_c = 0  
                 
    def reader(self):
        while True:
            
            self.mutex.acquire() # Beginning of security region.(Security region needed so that multiple processes are not allowed to update r_c at the same time).
            self.r_c+=1    # A new reader has entered, hence r_c is incremented by 1. 
            if self.r_c == 1: # If the current reader is the first one, we wait on wrt. Not allowing any writer threads. If r_c is not equal to 1, it means that the reader thread which arrived earlier did the job of blocking writers from the critical section. 
                self.wrt.acquire() 
            self.mutex.release() # End of security region.    
            
            print(f"Leitor {self.r_c} está lendo") 
            
            self.mutex.acquire() # Beginning of security region.(Security region needed so that multiple processes are not allowed to update r_c at the same time).   
            self.r_c-=1  # A reader is leaving the critical section hence, decrementing the r_c by 1.
            if self.r_c == 0: # If the reader exiting is the last remaining reader, we signal wrt thus allowing writer threads to enter. 
                self.wrt.release()  
            self.mutex.release() # End of security region.    
            
            time.sleep(3)          
 
    def writer(self):
        while True:
            self.wrt.acquire()     # At a given point of time there must be only one writer in the critical section. Hence, we wait on wrt, blocking other writers from entering.
            print("Escrevendo dados.....")  
            print("-"*20)
            self.wrt.release()      # Since the write operation is performed, the writer thread is exiting the critical section, hence, we signal wrt making it available for some other writer to enter.
            time.sleep(3)    
 
    def main(self):
        t1 = threading.Thread(target = self.reader) 
        t1.start()
        t2 = threading.Thread(target = self.writer) 
        t2.start()
        t3 = threading.Thread(target = self.reader) 
        t3.start()
        t4 = threading.Thread(target = self.reader) 
        t4.start()
        t6 = threading.Thread(target = self.writer) 
        t6.start()
        t5 = threading.Thread(target = self.reader) 
        t5.start()
        
 
if __name__=="__main__":
    c = ReaderWriterProblem()
    c.main()