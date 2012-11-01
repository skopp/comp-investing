

'''
Class used to print the percentage of a loop
How to use:
1. Before the loop:
    percentPrinter = PercentPrinter(total_iterations, printPercentValue)
2. Inside de loop:
    percentPrinter.next()
'''
class PercentPrinter():
    def __init__(self, iterations, percent):
        print 'Starting %d iterations' % iterations
        self.iterations = iterations
        self.percent = percent
        self.iteration = 0
        self.next_print = self.iterations * self.percent

    def next(self):
        self.iteration += 1  # First so it prints the 100%

        if self.iteration == self.iterations:
            print '100% complete'
        elif self.iteration > self.next_print:
            print "%.1f%% complete" % (100 * self.next_print / self.iterations)
            self.next_print += (self.iterations * self.percent)
