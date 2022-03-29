import os
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
from dataclasses import dataclass
from uncertainties import ufloat, unumpy, umath


IMG_PATH: str = "img/"  # relative path where the image will be stored.


@dataclass
class PlotResult:
    """ Resulting data that will be returned from the plot function. """
    quadA: ufloat
    quadB: ufloat
    quadC: ufloat


def quadFit(x, a, b, c):
    """ Quadratic fit function. """
    return a*x*x + b*x +c


def Plot(data):
# Settings 
    LINE_WIDTH = 2    # Dicke Graph linie
    NUM_STDDEV_Y = 1  # Anzahl der Standardabweichungen für die Fehlerbalken
    NUM_STDDEV_X = 1

    plt.style.use(['science', 'grid'])
    
    plt.rc('font', size=25)
    plt.figure(figsize=(15, 8))
    plt.subplots_adjust(top=0.96, bottom=0.10, left=0.08, right=0.965, hspace=0.2, wspace=0.2)

    label_x = "Text (Unit)"
    label_y = "Text (Unit)"

# Data
    # NOTE: Use .n to get value from ufloat - Use .s to get error from ufloat
    x    = [val.x.n for val in data]
    xErr = [val.x.s for val in data]
    
    y    = [val.y.n for val in data]
    yErr = [val.y.s for val in data]

# Fit
    opt, covariance = optimize.curve_fit(quadFit, x, y)
    optUncertainty = np.sqrt(np.diag(covariance))  # Get Uncertainty from covariance matrix
    
    xFit = np.linspace(min(x), max(x), 20)         # 20 points from min(x) to max(x)
    yFit = [quadFit(xi, opt[0], opt[1], opt[2]) for xi in xFit]

    a = ufloat(opt[0], optUncertainty[0])
    b = ufloat(opt[1], optUncertainty[1])
    c = ufloat(opt[2], optUncertainty[2])
    
    print(f"a = {a}")
    print(f"b   = {b}")
    print(f"c   = {c}")
    information: str = '\n'.join([
        f"y(x) = $ax^2 + bx + c$",
        f"a = {a} unit",
        f"b = {b} unit",
        f"c = {c} unit"
    ])
 
# Plot
    # NOTE: Use zorder=1,2, 3,... to set lines/points etc into background/foreground. The higher the order, the more in foreground.
    plt.scatter(x, y, lw=LINE_WIDTH, label='Messpunkte')
    plt.errorbar(x, y, xerr=[NUM_STDDEV_X*xe for xe in xErr], yerr=[NUM_STDDEV_Y*ye for ye in yErr], linestyle='none', label=f'{NUM_STDDEV_X}-fache Stddev', capsize = 4, lw=LINE_WIDTH)
    plt.plot(xFit, yFit, lw=LINE_WIDTH, label='Fit Funktion')

# Label and Legend
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.legend(loc = 'lower right')
    plt.figtext(0.30, 0.66, information)

# Save
    if not os.path.exists(IMG_PATH):
        os.makedirs(IMG_PATH)

    plt.savefig(IMG_PATH + "A2.png")

# Return result values
    return PlotResult(a, b, c)




@dataclass
class point:
    """ Measured data that contains an x and y point. """
    x: ufloat
    y: ufloat


if __name__ == "__main__":
# Setup test data
    x = np.linspace(-10, 10, 30)
    y = [xi*xi for xi in x]

    data = []
    for i in range(len(x)):
        data.append(point(ufloat(x[i], 0.2), ufloat(y[i], 2)))

# Run plot
    Plot(data)