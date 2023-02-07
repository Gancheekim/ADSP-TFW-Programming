import time
import numpy as np
import matplotlib.pyplot as plt


def GW(x, t, f, B, sgm, a, b):
    start_time = time.time()
    dt = t[1] - t[0]
    df = f[1] - f[0]
    n0 = int(t[0] / dt)
    n1 = int(t[-1] / dt)
    m0 = int(f[0] / df)
    m1 = int(f[-1] / df)
    T = t.size
    F = f.size
    N1 = int(1 / (dt * df))
    N2 = int(1 / (dt * df * 2))
    Q1 = int(B / dt)
    k = np.arange(-Q1, Q1 + 1)
    ans = []

    for n in range(n0, n1 + 1):
        # x_1(q)
        x1 = np.zeros(N1)
        for q in range(2 * Q1 + 1):
            idx = n + k[q]
            if idx < 0 or idx >= T:
                x1[q] = 0
            else:
                x1[q] = x[idx] * np.power(sgm, 0.25) * np.exp(-sgm * np.pi * (k[q] * dt)**2.0) * dt

        # Q2
        Q2 = min(n1 - n, n - n0)

        # c_1(q)
        c1 = np.zeros(N2)
        for q in range(2 * Q2 + 1):
            idx1 = n + q - Q2
            idx2 = n - q + Q2
            if (idx1 < n0) or (idx1 > n1) or (idx2 < n0) or (idx2 > n1):
                c1[q] = 0
            else:
                c1[q] = x[idx1] * np.conjugate(x[idx2]) * 2 * dt

        # X_1(m) = FFT[x_1(q)]
        X_1 = np.fft.fft(x1)
        X1 = np.zeros(F, dtype = 'complex_')
        for m in range(m0, m0 + F):
            X1[m - m0] = X_1[(m + N1) % N1]
        X1 = np.power(X1, a, dtype=complex)

        # C_1(m) = FFT[c_1(q)]
        C1 = np.fft.fft(c1)
        C = np.zeros(m1 - m0 + 1, dtype = 'complex_')
        for m in range(m0, m1 + 1):
            C[m - m0] = C1[(m + N2) % N2]
        C = np.power(C, b, dtype=complex)

        ans.append(X1 * C)
    
    end_time = time.time()
    total_time = end_time - start_time
    print(total_time)
    ans = np.asarray(ans)
    ans = ans.T
    ans = np.abs(ans)

    fig, axs = plt.subplots(2, 1, constrained_layout=True)
    axs[0].plot(t, x)
    axs[0].set_ylabel('x')

    X, Y = np.meshgrid(t, f)
    im = axs[1].pcolormesh(X, Y, ans, cmap = "gray")
    plt.colorbar(im, ax = axs[1], orientation = "horizontal")
    axs[1].set_ylabel('Gabor-Wigner transform')

    plt.show()
    

