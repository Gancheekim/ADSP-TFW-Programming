import time
import numpy as np
import matplotlib.pyplot as plt


def GS(x, t, f, B, sgm1, sgm2, a, b):
    start_time = time.time()
    dt = t[1] - t[0]
    df = f[1] - f[0]
    n0 = int(t[0] / dt)
    m0 = int(f[0] / df)
    T = t.size
    F = f.size
    N = int(1 / (dt * df))
    Q = int(B / dt)
    k = np.arange(-Q, Q + 1)
    ans = []
    
    for n in range(n0, n0 + T):
        # x_1(q)
        x1 = np.zeros(N)
        x2 = np.zeros(N)
        for q in range(2 * Q + 1):
            idx = n + k[q]
            if idx < 0 or idx >= T:
                x1[q] = x2[q] = 0
            else:
                x1[q] = x[idx] * np.power(sgm1, 0.25) * np.exp(-sgm1 * np.pi * (k[q] * dt)**2.0) * dt
                x2[q] = x[idx] * np.power(sgm2, 0.25) * np.exp(-sgm2 * np.pi * (k[q] * dt)**2.0) * dt

        # X_1(m) = FFT[x_1(q)]
        X_1 = np.fft.fft(x1)
        X_2 = np.fft.fft(x2)
        X1 = np.zeros(F, dtype = 'complex_')
        X2 = np.zeros(F, dtype = 'complex_')
        for m in range(m0, m0 + F):
            X1[m - m0] = X_1[(m + N) % N]
            X2[m - m0] = X_2[(m + N) % N]
        X1 = np.power(X1, a, dtype=complex)
        X2 = np.power(X2, b, dtype=complex)
        X2 = np.conjugate(X2)
        ans.append(X1 * X2)
    
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
    axs[1].set_ylabel('Generalized Spectrogram')

    plt.show()

