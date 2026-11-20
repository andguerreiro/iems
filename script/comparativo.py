#!/usr/bin/env python3
"""Lê avaliacoes/*.md; gera comparativo.csv e atualiza o ranking do README.md."""

import csv
import io
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARQ_README = RAIZ / "README.md"
ARQ_COMPARATIVO = RAIZ / "comparativo.csv"
DIR_AVALIACOES = RAIZ / "avaliacoes"

ROTULOS = {"Graves": "Graves", "Medios": "Médios", "Agudos": "Agudos"}
ROTULO_SOM = "Média"
LIMITE_BOCAL_MM = 6.0
TOL = 0.02 + 1e-9
TOL_FREQ_HZ = 250

NOTA_MAX, NOTA_MIN = 5.0, 1.0
DESVIO_NOTA_MAX = 0.5

ITENS_USO = [
    ("Bocal", "Bocal compatível (≤ 6.0 mm)"),
    ("Conforto", "Confortável após 60 minutos"),
    ("Cabo", "Flexível e sem microfonia"),
    ("Ponteiras", "Silicone macio e flexível"),
    ("Reparo", "Troca de cabo"),
]
ITEM_BOCAL = ITENS_USO[0]

COLUNAS = [
    "Posicao", "IEM", "Assinatura", "Massa (g)", "Bocal (mm)",
    "Carcaca (mm)", "Preco (USD)",
    "Desvio Graves (dB)", "Desvio Medios (dB)", "Desvio Agudos (dB)",
    "Desvio total (dB)", "Desvio maximo (dB)", "Freq. do desvio maximo (Hz)",
    "Nota Graves", "Nota Medios", "Nota Agudos", "Nota Som",
    "Uso Bocal", "Uso Conforto", "Uso Cabo", "Uso Ponteiras", "Uso Reparo",
    "Nota Uso", "Nota geral",
]


class AvaliacaoInvalida(Exception):
    pass


def slug(nome):
    return re.sub(r"[^a-z0-9]+", "_", nome.lower()).strip("_")


def numero(texto):
    limpo = re.sub(r"^[~\s]+", "", str(texto).strip()).replace(",", ".")
    return float(limpo)


def valor_medida(texto):
    """'~9.16 kHz' -> 9160.0; '~7.50 dB' -> 7.5; '~8.00 kHz / ~10.00 kHz' -> 8000.0."""
    primeiro = str(texto).split("/")[0].strip()
    m = re.match(
        r"^[~\s]*(-?\d+(?:[.,]\d+)?)\s*(kHz|Hz|dB)?$",
        primeiro,
        re.IGNORECASE,
    )
    if not m:
        raise ValueError(f"valor não numérico: '{texto}'")
    num = float(m.group(1).replace(",", "."))
    unidade = (m.group(2) or "").lower()
    if unidade == "khz":
        return num * 1000.0
    return num


def formatar_db(x):
    return f"~{x:.2f}"


def formatar_freq_hz(hz):
    if hz >= 1000:
        return f"~{hz / 1000:.2f} kHz"
    return f"~{hz:.0f} Hz"


def arredondar(x):
    return f"{x + 1e-9:.2f}"


def calcular_nota_banda(desvio):
    if desvio <= DESVIO_NOTA_MAX:
        return NOTA_MAX
    return max(NOTA_MIN, NOTA_MAX + DESVIO_NOTA_MAX - desvio)


def gravar_se_mudou(caminho, conteudo, encoding="utf-8"):
    if caminho.is_file() and caminho.read_text(encoding=encoding) == conteudo:
        return False
    caminho.write_text(conteudo, encoding=encoding)
    return True


def linhas(texto):
    saida = []
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha.startswith("|"):
            continue
        celulas = [
            c.strip().replace("**", "").strip()
            for c in linha.strip("|").split("|")
        ]
        if not all(re.fullmatch(r":?-+:?", c) for c in celulas):
            saida.append(celulas)
    return saida


def secao(texto, titulo):
    padrao = (
        rf"^##[ \t]+{re.escape(titulo)}[ \t]*\n"
        r"(.*?)(?=^##[ \t]|\Z)"
    )
    resultado = re.search(padrao, texto, re.MULTILINE | re.DOTALL)
    if not resultado:
        raise AvaliacaoInvalida(f"seção '## {titulo}' não encontrada")
    return resultado.group(1)


def apos(tabela, cabecalho):
    for atual, seguinte in zip(tabela, tabela[1:]):
        if len(atual) >= len(cabecalho) and all(
            a.startswith(b) for a, b in zip(atual, cabecalho)
        ):
            return seguinte
    raise AvaliacaoInvalida(
        f"tabela '{' | '.join(cabecalho)}' não encontrada"
    )


def pendentes(texto):
    celulas = [c for linha in linhas(texto) for c in linha]
    n = sum(
        bool(re.fullmatch(r"(USD )?X( g| mm)?", c))
        for c in celulas
    )
    n += len(re.findall(
        r"(?m)^(?:-[ \t]*[✅❌][ \t]*|\*\*Extras[^\n]*?:\*\*[ \t]*)X[ \t]*$",
        texto,
    ))
    n += len(re.findall(
        r"(?m)^\*Geral = \([^)]*\bX\b[^)]*\)", texto
    ))
    return n


def ler_uso(texto):
    tabela = linhas(secao(texto, "Avaliação do uso"))

    lidos_lista = [
        ((r[1], r[2]), r[4])
        for r in tabela
        if len(r) == 5 and r[0].isdigit()
    ]

    lidos = dict(lidos_lista)

    if len(lidos) != len(lidos_lista):
        raise AvaliacaoInvalida("item duplicado na tabela de uso")

    if set(lidos) != set(ITENS_USO):
        raise AvaliacaoInvalida(
            f"tabela de uso: ausentes "
            f"{set(ITENS_USO) - set(lidos) or '-'}; "
            f"não reconhecidos "
            f"{set(lidos) - set(ITENS_USO) or '-'}"
        )

    invalidos = [chave for chave, v in lidos.items() if v not in ("0", "1")]
    if invalidos:
        raise AvaliacaoInvalida(
            f"itens do uso devem ser 0 ou 1: {invalidos}"
        )

    soma_md = next(
        (numero(r[4]) for r in tabela if r[0] == "Soma"),
        None,
    )

    return {chave: int(v) for chave, v in lidos.items()}, soma_md


def descobrir_avaliacoes():
    if not DIR_AVALIACOES.is_dir():
        sys.exit(f"Pasta não encontrada: '{DIR_AVALIACOES}'.")

    arquivos = sorted(DIR_AVALIACOES.glob("*.md"))
    if not arquivos:
        sys.exit(f"Nenhuma avaliação (.md) encontrada em '{DIR_AVALIACOES}'.")
    return arquivos


def montar_linha(caminho):
    nome_md = caminho.name
    texto = caminho.read_text(encoding="utf-8")

    titulo_match = re.search(r"^#[ \t]+(.+)$", texto, re.MULTILINE)
    iem = titulo_match.group(1).strip() if titulo_match else caminho.stem

    n = pendentes(texto)
    if n:
        raise AvaliacaoInvalida(
            f"{n} campo(s) ainda com 'X' em {nome_md}"
        )

    preco_txt, assinatura = apos(
        linhas(texto), ["Preço", "Assinatura"]
    )[:2]

    assinatura = assinatura.strip()
    if not assinatura or assinatura == "X":
        raise AvaliacaoInvalida(f"assinatura não preenchida em {nome_md}")

    preco = numero(preco_txt.removeprefix("USD"))

    secao_geral = secao(texto, "Nota geral")
    graves_md, medios_md, agudos_md, uso_md, geral_md = map(
        numero,
        apos(
            linhas(secao_geral),
            ["Graves", "Médios", "Agudos", "Uso", "Geral"],
        )[:5],
    )

    notas_resumo = {
        "Graves": graves_md,
        "Medios": medios_md,
        "Agudos": agudos_md,
    }

    formula = re.search(
        r"^\*Geral = \(([^)]*)\) ÷ 4",
        secao_geral,
        re.MULTILINE,
    )

    sec_bandas = linhas(secao(texto, "Avaliação do som"))
    bandas_md = {r[0]: r[1:] for r in sec_bandas}

    som_linha = bandas_md.get(ROTULO_SOM, [])
    som_md = (
        numero(som_linha[1])
        if len(som_linha) > 1 and som_linha[1]
        else None
    )

    total_md, max_md, freq_md = map(
        valor_medida,
        apos(
            sec_bandas,
            ["Desvio total", "Desvio máximo", "Frequência"],
        )[:3],
    )

    medidas = {
        r[0]: r[1]
        for r in linhas(secao(texto, "Minhas medições"))
        if len(r) >= 2
    }

    massa = (
        medidas.get("Massa por lado", "")
        .partition(" ")[0].replace(",", ".")
    )
    bocal = (
        medidas.get("Maior diâmetro do bocal", "")
        .partition(" ")[0].replace(",", ".")
    )
    comprimento = (
        medidas.get("Maior comprimento da carcaça", "")
        .partition(" ")[0].replace(",", ".")
    )

    valores, soma_md = ler_uso(texto)
    soma_uso = sum(valores.values())
    uso = float(soma_uso)

    avisos = []

    def comparar(nome, lido, calculado, tol=TOL):
        if abs(lido - calculado) > tol:
            avisos.append(
                f"{nome} no .md ({lido:g}) "
                f"difere do calculado ({calculado:g})."
            )

    if not massa:
        avisos.append("massa não encontrada.")
    if not comprimento:
        avisos.append("comprimento da carcaça não encontrado.")
    if not bocal:
        avisos.append("bocal não encontrado.")
    else:
        esperado = int(numero(bocal) <= LIMITE_BOCAL_MM)
        if valores[ITEM_BOCAL] != esperado:
            avisos.append(
                f"'{ITEM_BOCAL[1]}' está {valores[ITEM_BOCAL]}, "
                f"mas o bocal mede {bocal} mm "
                f"(esperado {esperado})."
            )

    if soma_md is None:
        avisos.append("linha Soma ausente na tabela de uso.")
    else:
        comparar("soma do uso", soma_md, soma_uso, 0)

    desvios_bandas = {}
    notas = {}

    for banda, rotulo in ROTULOS.items():
        if rotulo not in bandas_md or len(bandas_md[rotulo]) < 2:
            raise AvaliacaoInvalida(
                f"banda '{rotulo}' ausente ou incompleta em {nome_md}"
            )
        desvio_txt, nota_txt = bandas_md[rotulo][:2]
        desvio_val = valor_medida(desvio_txt)
        desvios_bandas[banda] = desvio_val

        nota_calc = calcular_nota_banda(desvio_val)
        notas[banda] = nota_calc

        comparar(f"nota de {banda}", numero(nota_txt), nota_calc)
        comparar(
            f"nota de {banda} em Nota geral",
            notas_resumo[banda],
            nota_calc,
        )

    som = sum(notas.values()) / 3
    pontos = sum(notas.values()) + uso
    geral = pontos / 4

    if som_md is None:
        avisos.append(f"linha '{ROTULO_SOM}' ausente na tabela de bandas.")
    else:
        comparar("Nota Som", som_md, som)

    comparar("Nota Uso", uso_md, uso)
    comparar("Nota Geral", geral_md, geral)

    if not formula:
        avisos.append(
            "fórmula '*Geral = (...) ÷ 4' ausente na seção Nota geral."
        )
    else:
        valores_esperados = {
            "Graves": notas["Graves"],
            "Médios": notas["Medios"],
            "Agudos": notas["Agudos"],
            "Uso": uso,
        }
        termos = [t.strip() for t in formula.group(1).split("+")]
        if len(termos) != 4:
            avisos.append(
                f"fórmula da Nota geral no .md "
                f"({formula.group(1)}) deve ter 4 termos."
            )
        else:
            for termo in termos:
                if termo in valores_esperados:
                    continue
                try:
                    valor_termo = numero(termo)
                except ValueError:
                    avisos.append(
                        f"fórmula da Nota geral no .md "
                        f"({formula.group(1)}) contém termo inválido: '{termo}'."
                    )
                    break
                if valor_termo not in valores_esperados.values():
                    avisos.append(
                        f"fórmula da Nota geral no .md "
                        f"({formula.group(1)}) contém o número "
                        f"{valor_termo:g}, que não corresponde "
                        "a Graves, Médios, Agudos ou Uso."
                    )
                    break

    for aviso in avisos:
        print(f"[AVISO] {iem}: {aviso}")

    linha = {
        "IEM": iem,
        "Assinatura": assinatura,
        "Massa (g)": massa,
        "Bocal (mm)": bocal,
        "Carcaca (mm)": comprimento,
        "Preco (USD)": f"{preco:g}",
        "Desvio Graves (dB)": formatar_db(desvios_bandas["Graves"]),
        "Desvio Medios (dB)": formatar_db(desvios_bandas["Medios"]),
        "Desvio Agudos (dB)": formatar_db(desvios_bandas["Agudos"]),
        "Desvio total (dB)": formatar_db(total_md),
        "Desvio maximo (dB)": formatar_db(max_md),
        "Freq. do desvio maximo (Hz)": formatar_freq_hz(freq_md),
        **{f"Nota {b}": f"{n:.2f}" for b, n in notas.items()},
        "Nota Som": arredondar(som),
        "Uso Bocal": valores[ITENS_USO[0]],
        "Uso Conforto": valores[ITENS_USO[1]],
        "Uso Cabo": valores[ITENS_USO[2]],
        "Uso Ponteiras": valores[ITENS_USO[3]],
        "Uso Reparo": valores[ITENS_USO[4]],
        "Nota Uso": arredondar(uso),
        "Nota geral": arredondar(geral),
    }

    return (
        -float(linha["Nota geral"]),
        preco,
        total_md,
        iem.lower(),
    ), linha


def atualizar_readme(linhas_csv):
    tabela = [
        "| Posição | IEM | Assinatura | Preço (USD) | Nota geral |",
        "| :---: | :--- | :--- | :---: | :---: |",
    ]

    for l in linhas_csv:
        tabela.append(
            f"| {l['Posicao']}º | "
            f"[{l['IEM']}](avaliacoes/{slug(l['IEM'])}.md) "
            f"| {l['Assinatura']} "
            f"| {l['Preco (USD)']} "
            f"| {l['Nota geral']} |"
        )

    novo, n = re.subn(
        r"(<!-- RANKING:INICIO -->\n).*?(<!-- RANKING:FIM -->)",
        lambda m: (
            m.group(1)
            + "\n".join(tabela)
            + "\n"
            + m.group(2)
        ),
        ARQ_README.read_text(encoding="utf-8"),
        flags=re.DOTALL,
    )

    if not n:
        sys.exit("Marcas RANKING não encontradas no README.")

    if gravar_se_mudou(ARQ_README, novo):
        print(f"Ranking atualizado em {ARQ_README}.")
    else:
        print("Ranking do README já estava atualizado.")


def main():
    print("Raiz do projeto:", RAIZ)

    resultados, erros = [], []

    for caminho in descobrir_avaliacoes():
        iem = caminho.stem
        try:
            resultados.append(montar_linha(caminho))
        except (AvaliacaoInvalida, KeyError, ValueError) as erro:
            motivo = (
                erro
                if isinstance(erro, AvaliacaoInvalida)
                else f"dado ausente ou inválido ({erro!r})"
            )
            erros.append(iem)
            print(f"[ERRO] {iem}: {motivo}. Fora do ranking.")

    if not resultados:
        sys.exit("Nenhuma avaliação válida; nada foi gerado.")

    linhas_csv = []
    for posicao, (_, linha) in enumerate(
        sorted(resultados, key=lambda r: r[0]), 1
    ):
        linha["Posicao"] = posicao
        linhas_csv.append(linha)

    buffer = io.StringIO()
    escritor = csv.DictWriter(
        buffer,
        fieldnames=COLUNAS,
        lineterminator="\n",
    )
    escritor.writeheader()
    escritor.writerows(linhas_csv)

    if gravar_se_mudou(
        ARQ_COMPARATIVO,
        buffer.getvalue(),
        "utf-8-sig",
    ):
        print(f"Comparativo salvo ({len(linhas_csv)} IEMs).")
    else:
        print("comparativo.csv já estava atualizado.")

    atualizar_readme(linhas_csv)

    if erros:
        print(
            f"\n{len(erros)} avaliação(ões) com erro: "
            f"{', '.join(erros)}."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
