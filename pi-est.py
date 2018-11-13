import math
import numpy as np
from numpy import matlib

from prompt_toolkit import prompt, HTML
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.shortcuts import confirm


class MonteCarloPi:
    def __init__(self, dimensions):
        # dimensions is the numbers of dimensions we're working with
        self.dimensions = dimensions

        # points keeps track of all the point we visited during the last
        # estimate, in order to be able to plot it
        self.points_visited = []

        # result keeps the result of last estimate
        self.result = 0

    def _mask(self, p):
        """The mask is for determining if a given point is inside the
        'n-dimension quadrant' we're working with.
        """
        # n-dimensional pythagorean theorem
        sum = np.sum([x ** 2 for x in np.nditer(p)])
        return math.sqrt(sum) <= 1

    def _solve_for_pi(self, ratio):
        """Solve for Pi using the given ratio of numbers inside the quadrant
        vs outside and the dimension we're working with.
        """
        # Only works for 2 and 3 dimensions and is really hacky.
        # Use volume for n-ball / 2**dimension?
        return ratio * 2 * self.dimensions

    def _generate_points(self, num_points):
        """Generate num_points number of uniformly distributed numbers using
        numpy.random
        """
        s = np.random.RandomState()
        for _ in range(num_points):
            yield s.random_sample(self.dimensions)

    def deviation(self, ref):
        """Return the deviation between the current result and the given
        reference value, in percentage
        """
        return abs(ref - self.result) / ref

    def estimate_points(self, num_points):
        # generate points
        inside, outside = 0, 0
        for p in self._generate_points(num_points):
            self.points_visited.append(p)
            if self._mask(p):
                inside += 1
            else:
                outside += 1

        # quadrant area = inside/total, since square area is 1
        # pi = quadrant area * 4
        self.result = self._solve_for_pi(inside / num_points)

    def estimate_deviation(self, deviation, step, ref):
        inside, outside, total = 0, 0, 0
        while self.deviation(ref) > deviation:
            for p in self._generate_points(step):
                self.points_visited.append(p)
                total += 1
                if self._mask(p):
                    inside += 1
                else:
                    outside += 1

            self.result = self._solve_for_pi(inside / total)

        print('[ ] Reached desired deviation after %d points' % total)

    def plot(self):
        # TODO
        if self.points_visited:
            pass


if __name__ == '__main__':
    dim = int(prompt('[?] Solve in how many dimensions: ', default='2'))
    pi = MonteCarloPi(dim)

    print('[ ] Pi can be estimated from a defined number of points or for a '
          'given deviation value.')
    if confirm('[?] Estimate from deviation value?', suffix=' (y/N) '):
        dev = float(prompt('[?] Desired deviation: ', default='0.001'))
        step = int(prompt('[?] Step for each iteration: ', default='1000'))
        pi.estimate_deviation(dev, step, math.pi)
    else:
        num = int(prompt('[?] How many points to use: ', default='30000'))
        pi.estimate_points(num)

    pi.plot()
    print(HTML('[*] Pi were estimated to <b>{}</b> ({}, ~{:.5f}%)'
               .format(pi.result, math.pi, pi.deviation(math.pi))))
