import os
import re
import sys
import numpy as np

# raiz do projeto = pasta acima de "script/" (funciona de qualquer diretório)
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_MEDICOES = os.path.join(RAIZ, "medicoes")
DIR_GRAFICOS = os.path.join(RAIZ, "graficos")
ARQ_ALVO = os.path.join(RAIZ, "target", "HarmanIE2019.txt")
ARQ_CSV = os.path.join(RAIZ, "desvios.csv")

# uso: python3 script/gerar_grafico.py [--sem-graficos]
GERAR_GRAFICOS = "--sem-graficos" not in sys.argv

bandas = {
    "Graves": (20, 250),
    "Médios": (250, 4000),
    "Agudos": (4000, 10000),
}

# 1000 pontos em escala logarítmica: cada oitava tem o mesmo número de pontos,
# então a média sobre a curva já pondera cada região pela sua largura em oitavas
freq = np.logspace(np.log10(20), np.log10(20000), 1000)
ref = np.argmin(np.abs(freq - 1000))

# faixa avaliada no desvio total e no desvio máximo (20 Hz a 10 kHz)
faixa_total = (freq >= 20) & (freq < 10000)


def carregar(caminho):
    """Lê frequência/amplitude com separador vírgula, tab, espaço ou ponto e vírgula.
    Ignora cabeçalhos, linhas inválidas e pontos com amplitude exatamente 0."""
    dados = []
    with open(caminho, encoding="utf-8-sig") as fh:
        for linha in fh:
            linha = linha.strip()
            if not linha:
                continue
            partes = [p for p in re.split(r"[,\t;\s]+", linha) if p]
            try:
                dados.append((float(partes[0]), float(partes[1])))
            except (ValueError, IndexError):
                continue  # cabeçalho ou linha inválida
    if not dados:
        raise ValueError(f"Não consegui ler nenhum dado numérico em '{caminho}'.")
    d = np.array(dados)
    d = d[d[:, 1] != 0]          # descarta o ponto final com amplitude 0
    d = d[np.argsort(d[:, 0])]   # garante frequência crescente (exigido pelo np.interp)
    return d[:, 0], d[:, 1]


def interp(f, a):
    return np.interp(np.log10(freq), np.log10(f), a)


def nota(desvio):
    """Nota de 1 a 5 pela régua do README."""
    if desvio <= 1.0:
        return 5
    if desvio <= 2.0:
        return 4
    if desvio <= 3.0:
        return 3
    if desvio <= 4.5:
        return 2
    return 1


def fmt(x):
    return f"{x:.2f}".replace(".", ",")


def descobrir_iems():
    """Agrupa os .txt de medicoes/ pelo nome base (sem o sufixo ' [n]')."""
    grupos = {}
    for f in sorted(os.listdir(DIR_MEDICOES)):
        if not f.lower().endswith(".txt"):
            continue
        base = re.sub(r"\s*\[\d+\]$", "", f[:-4]).strip()
        grupos.setdefault(base, []).append(f)
    return grupos


def salvar_grafico(iem, curva, harman, desvio_total):
    import matplotlib
    matplotlib.use("Agg")  # só salva os PNGs, não abre janelas
    import matplotlib.pyplot as plt

    slug = re.sub(r"[^a-z0-9]+", "_", iem.lower()).strip("_")
    fig, ax = plt.subplots(figsize=(11.7, 6.4), dpi=150)
    ax.plot(freq, curva, color="#4A90D9", lw=2.2, label=iem)
    ax.plot(freq, harman, color="gray", lw=1.8, ls=":", label="Harman IE 2019 (target)")
    ax.set_xscale("log")
    ax.set_xlim(20, 20000)
    ax.set_xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
    ax.set_xticklabels(["20", "50", "100", "200", "500", "1k", "2k", "5k", "10k", "20k"])
    ax.set_xlabel("Frequência (Hz)")
    ax.set_ylabel("Amplitude relativa (dB) — normalizado em 1 kHz")
    ax.set_title(f"{iem} vs Harman IE 2019 — desvio total: {fmt(desvio_total)} dB")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="lower left")
    fig.tight_layout()
    saida = os.path.join(DIR_GRAFICOS, f"{slug}.png")
    fig.savefig(saida)
    plt.close(fig)
    print(f"  Gráfico salvo em {saida}")


def processar(iem, arquivos, harman):
    curva = np.mean(
        [interp(*carregar(os.path.join(DIR_MEDICOES, f))) for f in arquivos], axis=0
    )

    # normaliza em 1 kHz (mesmo valor do alvo nesse ponto)
    curva = curva - curva[ref] + harman[ref]
    erro = np.abs(curva - harman)

    print(f"\n=== {iem} ({len(arquivos)} arquivo(s): {', '.join(arquivos)}) ===")
    desvios, notas = {}, {}
    for nome, (lo, hi) in bandas.items():
        m = (freq >= lo) & (freq < hi)
        d = np.mean(erro[m])
        desvios[nome] = d
        notas[nome] = nota(d)
        print(f"  {nome} ({lo}–{hi} Hz): {fmt(d)} dB de distância da Harman IE 2019 -> nota {notas[nome]}")

    # desvio total = média direta sobre toda a curva (20 Hz a 10 kHz)
    erro_faixa = erro[faixa_total]
    desvio_total = np.mean(erro_faixa)
    print(f"  Desvio total (20–10000 Hz, média sobre a curva): {fmt(desvio_total)} dB")

    # desvio máximo = maior distância em um único ponto (20 Hz a 10 kHz)
    i_max = np.argmax(erro_faixa)
    desvio_max = erro_faixa[i_max]
    freq_max = freq[faixa_total][i_max]
    print(f"  Desvio máximo: {fmt(desvio_max)} dB em {freq_max:.0f} Hz")

    if GERAR_GRAFICOS:
        salvar_grafico(iem, curva, harman, desvio_total)

    return {
        "iem": iem,
        **desvios,
        "notas": notas,
        "total": desvio_total,
        "max": desvio_max,
        "freq_max": freq_max,
    }


def main():
    print("Raiz do projeto:", RAIZ)

    if not os.path.isdir(DIR_MEDICOES):
        sys.exit(f"Pasta de medições não encontrada: '{DIR_MEDICOES}'.")
    if not os.path.isfile(ARQ_ALVO):
        sys.exit(f"Arquivo do alvo não encontrado: '{ARQ_ALVO}'.")
    if GERAR_GRAFICOS:
        os.makedirs(DIR_GRAFICOS, exist_ok=True)

    harman = interp(*carregar(ARQ_ALVO))

    grupos = descobrir_iems()
    if not grupos:
        sys.exit(f"Nenhum arquivo .txt de IEM encontrado em '{DIR_MEDICOES}'.")
    print(f"{len(grupos)} IEM(s) encontrado(s): {', '.join(grupos)}")

    resultados = []
    for iem, arquivos in grupos.items():
        try:
            resultados.append(processar(iem, arquivos, harman))
        except ValueError as e:
            print(f"\n[ERRO] {iem}: {e}")

    if not resultados:
        sys.exit("Nenhum IEM processado.")

    # ranking: menor desvio total primeiro
    resultados.sort(key=lambda r: r["total"])

    print("\n" + "=" * 92)
    print("RANKING (menor desvio total = mais próximo da Harman IE 2019)")
    print("=" * 92)
    print(f"{'#':<3} {'IEM':<26} {'Graves':>8} {'Médios':>8} {'Agudos':>8} "
          f"{'Total':>8} {'Máximo':>8} {'Em (Hz)':>8}")
    for i, r in enumerate(resultados, 1):
        print(f"{i:<3} {r['iem']:<26} {fmt(r['Graves']):>8} {fmt(r['Médios']):>8} "
              f"{fmt(r['Agudos']):>8} {fmt(r['total']):>8} {fmt(r['max']):>8} "
              f"{r['freq_max']:>8.0f}")

    print("\n" + "=" * 92)
    print("NOTAS POR BANDA")
    print("=" * 92)
    print(f"{'IEM':<26} {'Graves':>8} {'Médios':>8} {'Agudos':>8}")
    for r in resultados:
        n = r["notas"]
        print(f"{r['iem']:<26} {n['Graves']:>8} {n['Médios']:>8} {n['Agudos']:>8}")

    # CSV (vírgula como separador, ponto como decimal)
    with open(ARQ_CSV, "w", encoding="utf-8-sig") as fh:
        fh.write("Posição,IEM,Graves (dB),Médios (dB),Agudos (dB),Desvio total (dB),"
                 "Desvio máximo (dB),Freq. do desvio máximo (Hz)\n")
        for i, r in enumerate(resultados, 1):
            fh.write(f"{i},{r['iem']},{r['Graves']:.2f},{r['Médios']:.2f},"
                     f"{r['Agudos']:.2f},{r['total']:.2f},{r['max']:.2f},"
                     f"{r['freq_max']:.0f}\n")
    print(f"\nCSV salvo em {ARQ_CSV}")


if __name__ == "__main__":
    main()
