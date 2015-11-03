from src.main.common import BinomialCoefficientsFunction
from src.main.common import GammaFunction
from src.main.common import VectorManipulation
from scipy.misc import factorial
import numpy as np


class NuclearAttractionIntegral:

    @staticmethod
    def a_function(l, r, i, l_1, l_2, pa, pb, pc, g):
        e = 1 / (4*g)
        f_l = BinomialCoefficientsFunction.calculate_coefficient(l, l_1, l_2, pa, pb)
        num = (-1)**i * factorial(l) * pc**(l - 2*r - 2*i) * e**(r + i)
        dom = factorial(r) * factorial(i) * factorial(l - 2*r - 2*i)
        out = (-1)**l * f_l * (num/dom)
        return out

    @classmethod
    def primitive_nuclear_attraction(cls, gaussian_1, gaussian_2, nuclei):
        a_1 = gaussian_1.exponent
        a_2 = gaussian_2.exponent
        l_1 = gaussian_1.integral_exponents
        l_2 = gaussian_2.integral_exponents

        r_a = gaussian_1.coordinates
        r_b = gaussian_2.coordinates
        r_c = nuclei.coordinates
        r_p = VectorManipulation.vector_gaussian(a_1, r_a, a_2, r_b)

        r_ab = VectorManipulation.squared_distance(r_a, r_b)
        r_pc = VectorManipulation.squared_distance(r_p, r_c)

        r_p_a = VectorManipulation.vector_minus(r_p, r_a)
        r_p_b = VectorManipulation.vector_minus(r_p, r_b)
        r_p_c = VectorManipulation.vector_minus(r_p, r_c)

        g = a_1 + a_2

        out1 = 0
        for l in range(0, l_1[0] + l_2[0] + 1):
            for r in range(0, int(l/2) + 1):
                for i in range(0, int((l - 2*r) / 2) + 1):
                    out2 = cls.a_function(l, r, i, l_1[0], l_2[0], r_p_a[0], r_p_b[0], r_p_c[0], g)
                    for m in range(0, l_1[1] + l_2[1] + 1):
                        for s in range(0, int(m/2) + 1):
                            for j in range(0, int((m - 2*s) / 2) + 1):
                                out3 = cls.a_function(m, s, j, l_1[1], l_2[1], r_p_a[1], r_p_b[1], r_p_c[1], g)
                                for n in range(0, l_1[2] + l_2[2] + 1):
                                    for t in range(0, int(n/2) + 1):
                                        for k in range(0, int((n - 2*t) / 2) + 1):
                                            out4 = cls.a_function(n, t, k, l_1[2], l_2[2], r_p_a[2], r_p_b[2], r_p_c[2], g)
                                            v = (l + m + n) - 2*(r + s + t) - (i + j + k)
                                            out5 = GammaFunction.incomplete_gamma_function(v, g * r_pc**2)
                                            out6 = out2 * out3 * out4 * out5
                                            out1 += out6

        out1 *= ((2 * np.pi) / g) * np.exp(- (a_1 * a_2 * r_ab**2) / g)
        return out1