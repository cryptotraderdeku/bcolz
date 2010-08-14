# Small benchmark to compare the times for computing expressions by
# using compressed arrays vs plain numpy arrays.  The tables.Expr
# module is used for this.

import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
import numexpr as ne
import tables as tb
import carray as ca
from time import time

N = 1e6   # the number of elements in x
clevel = 3  # the compression level

# Create the numpy array
x = np.arange(N)
# Create a compressed array
cx = ca.carray(x, clevel=clevel)
print "cx-->", repr(cx)
cout = ca.carray(np.empty((0,), dtype='f8'), clevel=clevel)

t0 = time()
out = ne.evaluate("x+1")
print "Time for numexpr--> %.3f" % (time()-t0,) 

t0 = time()
expr = tb.Expr("x+1")
out = expr.eval()
print "Time for numpy array--> %.3f" % (time()-t0,) 

t0 = time()
expr = tb.Expr("cx+1")
expr.setOutput(cout, append_mode=True)
expr.eval()
print "Time for compressed array--> %.3f" % (time()-t0,) 
print "cout-->", repr(cout)

assert_array_equal(out, cout.toarray(), "Arrays are not equal")
