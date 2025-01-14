import warnings
import numpy as np


def calc_basis(t, s, k):
    return (t[s+k+1] - t[s]) / (k + 1)

def M_knots_sequence(k, interior_knots, boundary_knots=(0, 1)):
    """
    Generates knots sequence for basis M spline
    :param k:
    :param interior_knots:
    :param boundary_knots:
    :return:
    """
    t = [min(boundary_knots)] * k + interior_knots + [max(boundary_knots)] * k
    return t

def M_basis (i, x, k, t, verbose=False):

    knot_seq_len = len(t)

    if i + k > knot_seq_len:
        raise ValueError("i + k > |t|.")

    # force np.array on x and t
    x = np.array(x)  # Convert x to a NumPy array if it's not already
    t = np.array(t)  # Convert t to a NumPy array if it's not already

    # if x == 1, reduce by epsilon amount for finding j
    x[x == 1] = 1 - np.finfo(np.float32).eps
    if verbose:
        print('x', x)

    def M_basis_in(i, x, k, t):

        if k == 1:
            if (x >= t[i - 1]) & (x < t[i]):
                return(1 / (t[i] - t[i - 1]))
            else:
                return(0)
        else:
            if t[i - 1 + k] > t[i - 1]:
                return(
                        k * ((x - t[i - 1]) * M_basis_in(i, x, k - 1, t) + (t[i - 1 + k] - x) * M_basis_in(i + 1, x, k - 1, t))  / ((k - 1) * (t[i - 1 + k] - t[i - 1]))
                )
            else:
                return(0)

    if np.ndim(x) == 0:
        return(M_basis_in(i, x, k, t))
    else:
        return(np.array(list(map(lambda xx : M_basis_in(i, xx, k, t), x))))


def M_spline(k, interior_knots, individual=False, boundary_knots = (0,1),  lambdas = None, x=0):
    t = M_knots_sequence(k, interior_knots, boundary_knots)
    m = len(t) - k

    if len(lambdas) != m or len(lambdas) != m:
        raise ValueError("Incorrect number of lambdas. Need ", m, "lambdas.")

    if len(lambdas) and individual:
        warnings.warn("lambdas are compatible with individual output.")

    if not len(lambdas):
        lambdas = [1/m for _ in range(m)]

    if sum(lambdas) != 1:
        warnings.warn("Lambdas do no sum up to 1.")

    if individual:
        out = np.apply_along_axis(lambda i: M_basis(i, x, k, t), axis=0, arr=np.arange(1, m+1))
    else:
        out = np.apply_along_axis(lambda i: M_basis(i, x, k, t), axis=0, arr=np.arange(1, m+1)).dot(lambdas)
    return out

def I_knots_sequence(k, interior_knots, boundary_knots = (0,1)):
    t = [min(boundary_knots)] * (k+1) + interior_knots + [max(boundary_knots)] * (k+1)
    return t

    knot_seq_len = len(t)

    if not (i in range(1, knot_seq_len-k+1)):
        raise ValueError("i > m = length(t) - k.")


    # force np.array on x and t
    x = np.array(x)  # Convert x to a NumPy array if it's not already

def I_basis(i, x, k, t, verbose=False):

    t = np.array(t)  # Convert t to a NumPy array if it's not already
    x = np.array(x) # convert to array
    
    # if x == 1, reduce by epsilon amount for finding j
    x[x == 1] = 1 - np.finfo(np.float32).eps
    if verbose:
        print('x', x)

    # find indicator j such that t_j <= x < t_{j+1}
    if np.ndim(x) == 0:
        j = np.where((x >= t[:-1]) & (x < t[1:]))[0][0] + 1
    else:
        j = np.array(list(map(lambda xx: np.where((xx >= t[:-1]) & (xx < t[1:]))[0][0], x))) + 1
    if verbose:
        print('j', j)

    def I_basis_value(jx):
        j, x = jx

        if i > j:
            out = 0
        elif i < j - k + 1:
            out = 1
        else:
            out = sum(map(
                lambda ii : (t[ii + k] - t[ii - 1]) / (k + 1) * M_basis(ii, x, k + 1, t),
                range(i, j + 1)))
        return out
    
    if np.ndim(x) == 0:
        return np.array(I_basis_value((j,x)))
    else:
        return np.array(list(map(I_basis_value, zip(j, x))))


def I_spline(k, interior_knots, x=0, lambdas=None, individual=False, boundary_knots = (0,1), exclude_constant_splines = True):
    
    t = I_knots_sequence(k, interior_knots, boundary_knots)
    if exclude_constant_splines:
        m = len(t) - k - 2
    else:
        m = len(t) - k
    
    if lambdas not in (None, m):
        raise ValueError("Incorrect number of lambdas. Need ", m, " lambdas.")
    if lambdas and individual:
        warnings.warn("lambdas are compatible with individual output.")
    if not lambdas:
        lambdas = [1/m for _ in range(m)]
    if sum(lambdas) < .9999 or sum(lambdas) > 1.0001:
        warnings.warn("Lambdas do not sum up to 1.")
    
    i_sequence = 2 if exclude_constant_splines else 1, m + 2 if exclude_constant_splines else m + 1
    i_sequence = [i for i in range(i_sequence[0], i_sequence[1])]

    if individual:
        out = np.array([I_basis(i, x, k, t) for i in i_sequence])
    else:
        out = np.dot(np.array([I_basis(i, x, k, t) for i in i_sequence]), lambdas)

    return out


# I_spline and M_spline and depedencies

# test
import numpy as np
# Generate sorted random values
x = np.sort(np.random.rand(100))
# Generate a sequence from 0 to 1 with a step of 0.01
x = np.arange(0, 1.01, 0.01)
#print("x", x)
# Calculate y values using a lambda function
y = np.array([min(max(1.2 * xi + np.random.normal(0, 0.2), 0), 1) for xi in x])
# Set the value of e
e = 1e-12


# print("output M_basis test 1", M_basis(2, x, 3, (0, 0, 0, .1, .5, .9, 1, 1, 1)))
# print("output M_basis test 1", M_basis(3, x, 3, (0, 0, 0, .1, .5, .9, 1, 1, 1)))
# print("output M_basis", [M_basis(i, x, 3, (0, 0, 0, .1, .5, .9, 1, 1, 1)) for i in range(1, 7)]),
#print("output", I_basis(3, x, 3, (0,0,0,0,.1,.5,.9,1,1,1,1), verbose=False))
# print("output", [I_basis(i, x, 3, [0, 0, 0, 0, 0.1, 0.5, 0.9, 1, 1, 1, 1]) for i in range(1, 9)])
# print("output",I_spline(x=x, k=3, interior_knots=[.1, .5, .9], individual = True))


## check M_basis
#print("output M_basis test 1", M_basis(6, x, 3, (0, 0, 0, .1, .5, .9, 1, 1, 1))) # confirmed

## check M spline
#print("ouput M_spline test 1", M_spline(3, [.1, .5, .9], individual=True, x=x)) # not confirmed # @TODO confirm

## check I_basis
#print("output I_basis test 1", I_basis(2, x, 3, (0,0,0,0,.1,.5,.9,1,1,1,1), verbose=False))  # confirmed
#print("output I basis test 2", [I_basis(i, x, 3, [0, 0, 0, 0, 0.1, 0.5, 0.9, 1, 1, 1, 1]) for i in range(1, 9)]) # confirmed

# print("output I spline test 1", 
#       I_spline(x = .12, k = 3, interior_knots = [.1, .9], individual = True)) ## confirmed

# print("output I spline test 1", 
#       I_spline(x = x, k = 3, interior_knots = [.1, .9], individual = True)[:, 12])