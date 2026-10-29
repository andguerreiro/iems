import os
import numpy as np
import matplotlib.pyplot as plt

def carregar(caminho):
    d = np.loadtxt(caminho)
    return d[:, 0], d[:, 1]

f1, a1 = carregar("IEM [1].txt")
f2, a2 = carregar("IEM [2].txt")
fh, ah = carregar("Harman IE 2019 Target.txt")

freq = np.logspace(np.log10(20), np.log10(20000), 1000)
interp = lambda f, a: np.interp(np.log10(freq), np.log10(f), a)

klean = (interp(f1, a1) + interp(f2, a2)) / 2
harman = interp(fh, ah)

# normaliza em 1 kHz (mesmo valor do alvo nesse ponto)
ref = np.argmin(np.abs(freq - 1000))
klean = klean - klean[ref] + harman[ref]

# desvio médio absoluto por banda (grade log-uniforme)
bandas = {"Graves": (20, 250), "Médios": (250, 4000), "Agudos": (4000, 10000)}
for nome, (lo, hi) in bandas.items():
    m = (freq >= lo) & (freq < hi)
    print(f"{nome}: {np.mean(np.abs(klean - harman)[m]):.2f} dB")

fig, ax = plt.subplots(figsize=(11.7, 6.4), dpi=150)
ax.plot(freq, klean, color="#4A90D9", lw=2.2, label="Kefine Klean")
ax.plot(freq, harman, color="gray", lw=1.8, ls=":", label="Harman IE 2019 (target)")
ax.set_xscale("log")
ax.set_xlim(20, 20000)
ax.set_xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
ax.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"])
ax.set_xlabel("Frequência (Hz)")
ax.set_ylabel("Amplitude relativa (dB) — normalizado em 1 kHz")
ax.set_title("Kefine Klean vs Harman IE 2019")
ax.grid(True, which="both", alpha=0.3)
ax.legend(loc="lower left")
fig.tight_layout()
os.makedirs("graficos", exist_ok=True)
fig.savefig("graficos/kefine_klean.png")
