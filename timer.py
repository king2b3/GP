''' Simple timer data structure
'''
import time
class Timer():
    def __init__(self):
        '''Timer class to track and report time usage to print'''
        self.start_time = 0
        self.end_time = 0

    def start_timer(self) -> None:
        ''' Records the start of a timer and resest both the start / end
        '''
        self.start_time = time.time()

    def end_timer(self) -> None:
        ''' Records the end value of a timer
        '''
        self.end_time = time.time()

    def __str__(self) -> str:
        ''' Returns the End - Start.
        '''
        return f"{self.end_time - self.start_time:.3f}"

    def __repr__(self) -> str:
        ''' Returns the End - Start.
        '''
        return f"{self.end_time - self.start_time:.3f}"