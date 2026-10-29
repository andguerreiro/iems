import os
import re
import sys
import numpy as np
import matplotlib.pyplot as plt

# ====== ALTERE SÓ AQUI ======
IEM = "KZ Castor"
# ============================

# nome do PNG: minúsculo, sem espaços (ex.: "KZ Castor" -> kz_castor.png)
slug = re.sub(r"[^a-z0-9]+", "_", IEM.lower()).strip("_")

# acha os arquivos do IEM na pasta atual (ignora o alvo Harman)
arquivos = sorted(
    f for f in os.listdir(".")
    if f.lower().endswith(".txt")
    and f.lower().startswith(IEM.lower())
    and not f.lower().startswith("harman")
)

if not arquivos:
    sys.exit(f"Nenhum arquivo encontrado começando com '{IEM}'.")

# se acharem arquivos de variações diferentes (ex.: Black e Silver), pede para ser mais específico
bases = {re.sub(r"\s*\[\d+\]$", "", f[:-4]) for f in arquivos}
if len(bases) > 1:
    sys.exit(
        f"'{IEM}' bate com mais de um conjunto de arquivos: {sorted(bases)}.\n"
        "Escreva o nome completo no IEM (ex.: 'Kefine Klean Silver')."
    )

print("Arquivos usados:", ", ".join(arquivos))


def carregar(caminho):
    d = np.loadtxt(caminho)
    return d[:, 0], d[:, 1]


freq = np.logspace(np.log10(20), np.log10(20000), 1000)


def interp(f, a):
    return np.interp(np.log10(freq), np.log10(f), a)


curva = np.mean([interp(*carregar(f)) for f in arquivos], axis=0)
harman = interp(*carregar("Harman IE 2019 Target.txt"))

# normaliza em 1 kHz (mesmo valor do alvo nesse ponto)
ref = np.argmin(np.abs(freq - 1000))
curva = curva - curva[ref] + harman[ref]

# desvio médio absoluto por banda (grade log-uniforme)
bandas = {"Graves": (20, 250), "Médios": (250, 4000), "Agudos": (4000, 10000)}
for nome, (lo, hi) in bandas.items():
    m = (freq >= lo) & (freq < hi)
    print(f"{nome}: {np.mean(np.abs(curva - harman)[m]):.2f} dB")

fig, ax = plt.subplots(figsize=(11.7, 6.4), dpi=150)
ax.plot(freq, curva, color="#4A90D9", lw=2.2, label=IEM)
ax.plot(freq, harman, color="gray", lw=1.8, ls=":", label="Harman IE 2019 (target)")
ax.set_xscale("log")
ax.set_xlim(20, 20000)
ax.set_xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
ax.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"])
ax.set_xlabel("Frequência (Hz)")
ax.set_ylabel("Amplitude relativa (dB) — normalizado em 1 kHz")
ax.set_title(f"{IEM} vs Harman IE 2019")
ax.grid(True, which="both", alpha=0.3)
ax.legend(loc="lower left")
fig.tight_layout()
fig.savefig(f"{slug}.png")
print(f"Gráfico salvo em {slug}.png")
