#!/usr/bin/env python3
"""
Calcula os desvios das curvas em relação à Harman IE 2019, atribui as notas
de Graves, Médios e Agudos e gera desvios.csv, gráficos e avaliações (.md)
em avaliacoes/, com 'X' no que não é calculável.

As assinaturas sonoras são classificadas manualmente e não são calculadas
por este script.

Uso (na raiz do projeto):
python3 scripts/graficos.py
"""
import csv
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
DIR_MEDICOES = RAIZ / "medicoes"
DIR_GRAFICOS = RAIZ / "graficos"
DIR_AVALIACOES = RAIZ / "avaliacoes"
ARQ_ALVO = RAIZ / "target" / "HarmanIE2019.txt"
ARQ_DESVIOS = RAIZ / "desvios.csv"

# chave -> (rótulo, de Hz, até Hz)
BANDAS = {
    "Graves": ("Graves", 20, 250),
    "Medios": ("Médios", 250, 4000),
    "Agudos": ("Agudos", 4000, 10000),
}

F_MIN, F_MAX, N_PONTOS = 20, 20000, 1000
F_NOTA_MAX = 10000
F_ALINHAMENTO = 1000
Y_LIMITE = 30

# Nota da banda: 5 até 0.5 dB de desvio médio e, a partir daí,
# cai 1 ponto por dB (nota = 5.5 - desvio), até o mínimo de 1.
NOTA_MAX, NOTA_MIN = 5.0, 1.0
DESVIO_NOTA_MAX = 0.5

COLUNAS = [
    "IEM", "Graves (dB)", "Medios (dB)", "Agudos (dB)",
    "Vies Graves (dB)", "Vies Medios (dB)", "Vies Agudos (dB)",
    "Desvio total (dB)", "Desvio maximo (dB)",
    "Freq. do desvio maximo (Hz)",
    "Nota Graves", "Nota Medios", "Nota Agudos", "Nota Som",
]

freq = np.logspace(np.log10(F_MIN), np.log10(F_MAX), N_PONTOS)
ref = int(np.argmin(np.abs(freq - F_ALINHAMENTO)))
faixa_nota = freq < F_NOTA_MAX

MODELO = """# {nome}

[← Voltar ao ranking](../README.md)

| Preço | Assinatura | Configuração medida |
| :---: | :---: | :--- |
| USD X | X | X |

## Resposta em frequência

![Gráfico do {nome}](../graficos/{slug}.png)

## Avaliação do som

| Banda | Desvio médio | Nota |
| :--- | :---: | :---: |
{bandas}
| **Média** | | **{som:.2f}** |

| Desvio total (20 Hz–10 kHz) | Desvio máximo | Frequência do desvio máximo |
| :---: | :---: | :---: |
| {total} dB | {maximo} dB | {freq_max} |

*Desvio total, desvio máximo e sua frequência são informativos e não entram nas notas. O desvio total não é utilizado para atribuir as notas de Graves, Médios ou Agudos.*

## Minhas medições

| Item | Medida |
| :--- | :--- |
| Massa por lado | X g |
| Maior diâmetro do bocal | X mm |
| Maior comprimento da carcaça | X mm |

*Medidos com balança e paquímetro digitais.*

## Avaliação do uso

| # | Grupo | Item | Critério atende? | Nota |
| :---: | :--- | :--- | :--- | :---: |
| 1 | Bocal | Bocal compatível (≤ 6.0 mm) | Diâmetro máximo de até 6.0 mm. | X |
| 2 | Conforto | Confortável após 60 minutos | Carcaça sem pressão, dor ou desconforto após 60 min. | X |
| 3 | Cabo | Flexível e sem microfonia | Flexível, desenrola fácil e sem ruídos na roupa. | X |
| 4 | Ponteiras | Silicone macio e flexível | Dobram ao meio facilmente com dois dedos. | X |
| 5 | Reparo | Troca de cabo | Cabo removível e com conexão fácil de encontrar. | X |
| **Soma** | | | | **X** |

**Extras (não entram na nota):** X

## Nota geral

| Graves | Médios | Agudos | Uso | **Geral** |
| :---: | :---: | :---: | :---: | :---: |
| {nota_graves} | {nota_medios} | {nota_agudos} | X | **X** |

*Geral = (Graves + Médios + Agudos + Uso) ÷ 4. As quatro notas pesam o mesmo, 25% cada. Por isso o som (graves, médios e agudos) responde por 75% da nota e o uso por 25%.*

## Resumo

**Prós**

- ✅ X
- ✅ X
- ✅ X

**Contras**

- ❌ X
- ❌ X
- ❌ X

## Especificações

| Item | Informação |
| :--- | :--- |
| Drivers | X |
| Quantidade por lado | X |
| Tecnologia | X |
| Carcaça | X |
| Conexão do cabo | X |
| Plug | X mm |
| Faixa de frequência | X |
| Impedância | X Ω |
| Sensibilidade | X dB |

## Como avalio

Confira [aqui](../README.md#como-avalio).
"""


def slug(nome):
    return re.sub(r"[^a-z0-9]+", "_", nome.lower()).strip("_")


def carregar(caminho):
    """Lê (frequência, amplitude); ignora cabeçalhos, linhas inválidas e duplicatas."""
    dados = []
    for linha in caminho.read_text(encoding="utf-8-sig").splitlines():
        p = re.split(r"[,\t;\s]+", linha.strip())
        try:
            f, a = float(p[0]), float(p[1])
        except (ValueError, IndexError):
            continue
        if np.isfinite([f, a]).all() and f > 0:
            dados.append((f, a))

    if len(dados) < 2:
        raise ValueError(f"Dados insuficientes em '{caminho}'.")

    f, a = np.array(dados).T
    f, idx = np.unique(f, return_index=True)
    return f, a[idx]


def interp(f, a):
    return np.interp(np.log10(freq), np.log10(f), a)


def nota(desvio):
    """Nota contínua da banda a partir do desvio médio (dB) com 2 casas."""
    return min(
        NOTA_MAX,
        max(NOTA_MIN, NOTA_MAX + DESVIO_NOTA_MAX - desvio)
    )


def descobrir_iems():
    """Agrupa arquivos .txt pelo nome base, sem o sufixo ' [n]'."""
    grupos = {}
    for arq in sorted(DIR_MEDICOES.iterdir()):
        if arq.suffix.lower() == ".txt":
            base = re.sub(r"\s*\[\d+\]$", "", arq.stem).strip()
            grupos.setdefault(base, []).append(arq)
    return grupos


def processar(iem, arquivos, harman):
    curva = np.mean([interp(*carregar(a)) for a in arquivos], axis=0)
    curva += harman[ref] - curva[ref]
    dif = curva - harman
    erro = np.abs(dif)

    linha = {"IEM": iem}

    for chave, (_, lo, hi) in BANDAS.items():
        m = (freq >= lo) & (freq < hi)
        desvio = f"{erro[m].mean():.2f}"
        linha[f"{chave} (dB)"] = desvio
        linha[f"Vies {chave} (dB)"] = f"{dif[m].mean():+.2f}"
        linha[f"Nota {chave}"] = f"{nota(float(desvio)):.2f}"

    # Média das notas de Graves, Médios e Agudos
    linha["Nota Som"] = f"{np.mean([
        float(linha[f'Nota {chave}']) for chave in BANDAS
    ]):.2f}"

    i_max = int(np.argmax(np.where(faixa_nota, erro, -1)))
    linha["Desvio total (dB)"] = f"{erro[faixa_nota].mean():.2f}"
    linha["Desvio maximo (dB)"] = f"{erro[i_max]:.2f}"
    linha["Freq. do desvio maximo (Hz)"] = f"{freq[i_max]:.0f}"

    return {"linha": linha, "curva": curva, "i_max": i_max}


def salvar_grafico(r, harman):
    l, i = r["linha"], r["i_max"]
    fig, ax = plt.subplots(figsize=(11.7, 6.4), dpi=150)

    ax.axvspan(F_NOTA_MAX, F_MAX, color="gray", alpha=0.10, lw=0)

    for x in (250, 4000, F_NOTA_MAX):
        ax.axvline(x, color="gray", lw=0.8, ls="--", alpha=0.6)

    regioes = list(BANDAS.values()) + [
        ("fora da nota", F_NOTA_MAX, F_MAX)
    ]

    for rotulo, lo, hi in regioes:
        ax.text(
            np.sqrt(lo * hi), 0.97, rotulo,
            transform=ax.get_xaxis_transform(),
            ha="center", va="top", fontsize=9, color="gray",
        )

    ax.plot(
        freq, r["curva"], color="#4A90D9",
        lw=2.2, label=l["IEM"]
    )
    ax.plot(
        freq, harman, color="gray",
        lw=1.8, ls=":", label="Harman IE 2019 (alvo)"
    )
    ax.plot(
        freq[i], r["curva"][i], "o",
        color="#D9534F", ms=7, clip_on=False, zorder=5,
        label=f"Desvio máximo: {l['Desvio maximo (dB)']} dB em "
              f"{l['Freq. do desvio maximo (Hz)']} Hz",
    )

    ax.set_xscale("log")
    ax.set_xlim(F_MIN, F_MAX)
    ax.set_ylim(-Y_LIMITE, Y_LIMITE)
    ax.set_xticks([
        20, 50, 100, 200, 500, 1000,
        2000, 5000, 10000, 20000
    ])
    ax.set_xticklabels([
        "20", "50", "100", "200", "500",
        "1k", "2k", "5k", "10k", "20k"
    ])
    ax.set_xlabel("Frequência (Hz)")
    ax.set_ylabel("Amplitude relativa (dB), normalizada em 1 kHz")
    ax.set_title(
        f"{l['IEM']} vs Harman IE 2019 — "
        f"Desvio total: {l['Desvio total (dB)']} dB"
    )
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="lower left")

    fig.tight_layout()
    fig.savefig(DIR_GRAFICOS / f"{slug(l['IEM'])}.png")
    plt.close(fig)


def criar_avaliacao(l):
    """Cria o .md do IEM (campos pendentes = 'X') se ainda não existir."""
    caminho = DIR_AVALIACOES / f"{slug(l['IEM'])}.md"

    if caminho.exists():
        print(f"  [IGNORADO] Avaliação já existe: {caminho.name}")
        return

    hz = int(l["Freq. do desvio maximo (Hz)"])

    caminho.write_text(
        MODELO.format(
            nome=l["IEM"],
            slug=slug(l["IEM"]),
            bandas="\n".join(
                f"| {rotulo} | {l[f'{c} (dB)']} dB | {l[f'Nota {c}']} |"
                for c, (rotulo, _, _) in BANDAS.items()
            ),
            total=l["Desvio total (dB)"],
            maximo=l["Desvio maximo (dB)"],
            freq_max=f"{hz / 1000:.2f} kHz" if hz >= 1000 else f"{hz} Hz",
            som=sum(
                float(l[f"Nota {c}"]) for c in BANDAS
            ) / 3,
            nota_graves=l["Nota Graves"],
            nota_medios=l["Nota Medios"],
            nota_agudos=l["Nota Agudos"],
        ),
        encoding="utf-8",
    )

    print(f"  [CRIADO] Avaliação gerada: {caminho.name}")


def main():
    print("Raiz do projeto:", RAIZ)

    if not DIR_MEDICOES.is_dir():
        sys.exit(f"Pasta não encontrada: '{DIR_MEDICOES}'.")
    if not ARQ_ALVO.is_file():
        sys.exit(f"Arquivo do alvo não encontrado: '{ARQ_ALVO}'.")

    grupos = descobrir_iems()
    if not grupos:
        sys.exit(f"Nenhum arquivo .txt de IEM em '{DIR_MEDICOES}'.")

    harman = interp(*carregar(ARQ_ALVO))
    resultados = []

    for iem, arquivos in grupos.items():
        try:
            resultados.append(processar(iem, arquivos, harman))
        except (ValueError, OSError) as erro:
            print(f"[ERRO] {iem}: {erro}")

    if not resultados:
        sys.exit("Nenhum IEM processado.")

    with open(ARQ_DESVIOS, "w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=COLUNAS,
            lineterminator="\n"
        )
        escritor.writeheader()
        escritor.writerows(sorted(
            (r["linha"] for r in resultados),
            key=lambda l: l["IEM"].lower()
        ))

    print(f"[ATUALIZADO] Desvios e notas salvos em {ARQ_DESVIOS}.")

    DIR_GRAFICOS.mkdir(exist_ok=True)
    DIR_AVALIACOES.mkdir(exist_ok=True)

    for r in resultados:
        iem = r["linha"]["IEM"]

        try:
            salvar_grafico(r, harman)
            print(f"{iem}: gráfico gerado.")
        except Exception as erro:
            print(f"[ERRO] Gráfico de {iem}: {erro}")

        criar_avaliacao(r["linha"])


if __name__ == "__main__":
    main()
