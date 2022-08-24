import threading
import random
import time

# Dining philosophers, 5 Phillies with 5 forks. Must have two forks to eat.
# inheriting threading class in Thread module

class Philosopher(threading.Thread):
    running = True  #used to check if everyone is finished eating

 #Since the subclass overrides the constructor, it must make sure to invoke the base class constructor (Thread.__init__()) before doing anything else to the thread.
    def __init__(self, index, forkOnLeft, forkOnRight):
        threading.Thread.__init__(self)
        self.index = index
        self.forkOnLeft = forkOnLeft
        self.forkOnRight = forkOnRight

    def run(self):
        while(self.running):
            # Philosopher is thinking (but really is sleeping).
            time.sleep(1)
            print ('Filosofo {} está faminto.'.format(self.index))
            self.dine()

    def dine(self):
        # if both the semaphores(forks) are free, then philosopher will eat
        fork1, fork2 = self.forkOnLeft, self.forkOnRight
        while self.running:
            fork1.acquire() # wait operation on left fork
            locked = fork2.acquire(False) 
            if locked: break #if right fork is not available leave left fork
            fork1.release()
            print ('Filosofo {} passou os talheres.'.format(self.index))
            fork1, fork2 = fork2, fork1
        else:
            return
        self.dining()
        #release both the fork after dining
        fork2.release()
        fork1.release()
 
    def dining(self):			
        print ('Flosofo {} comecou a comer. '.format(self.index))
        time.sleep(1)
        print ('Filosofo {} acabou de comer e foi filosofar.'.format(self.index))

def main():
    forks = [threading.Semaphore() for n in range(5)] #initialising array of semaphore i.e forks

    #here (i+1)%5 is used to get right and left forks circularly between 1-5
    philosophers= [Philosopher(i, forks[i%5], forks[(i+1)%5])
            for i in range(5)]

    Philosopher.running = True
    for p in philosophers: p.start()
    time.sleep(20)
    Philosopher.running = False
    print ("Acabou a refeição.")
 

if __name__ == "__main__":
    main()