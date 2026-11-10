# Meus IEMs: avaliações pessoais

Avalio apenas os IEMs que comprei e usei. As notas refletem minha experiência e meus critérios pessoais, não uma classificação definitiva.

## Ranking

<!-- RANKING:INICIO -->
| Posição | IEM | Assinatura | Preço (USD) | Nota geral |
| :---: | :--- | :--- | :---: | :---: |
| 1º | [Kiwi Ears Cadenza 2](avaliacoes/kiwi_ears_cadenza_2.md) | Neutro | 50 | 4.14 |
| 2º | [Kefine Klean](avaliacoes/kefine_klean.md) | Neutro quente | 49 | 4.00 |
| 3º | [KZ Castor Prata](avaliacoes/kz_castor_prata.md) | Neutro | 15 | 3.75 |
| 4º | [Sennheiser IE 100 Pro](avaliacoes/sennheiser_ie_100_pro.md) | Magro | 100 | 3.53 |
| 5º | [Truthear Zero Red](avaliacoes/truthear_zero_red.md) | Neutro | 55 | 3.42 |
| 6º | [KZ EDX Pro X](avaliacoes/kz_edx_pro_x.md) | Em V | 10 | 3.40 |
| 7º | [KZ ZS12 Pro X](avaliacoes/kz_zs12_pro_x.md) | Em U | 50 | 3.31 |
| 8º | [JBL Tune 110](avaliacoes/jbl_tune_110.md) | Baixudo | 15 | 2.09 |
<!-- RANKING:FIM -->

*Em caso de empate, prevalecem o menor preço e, depois, o menor desvio total.*

## Como avalio

A Nota Geral considera quatro componentes:

- Graves
- Médios
- Agudos
- Uso

Graves, médios, agudos e uso têm o mesmo peso na Nota Geral. Assim, o som representa 75% da nota e o uso, 25%.

### Som

Graves, médios e agudos são avaliados com base em medições de resposta em frequência, comparadas à curva [Harman IE 2019](target/HarmanIE2019.txt), adotada como referência de preferência neste projeto.

A nota de cada banda depende do desvio médio em relação ao alvo e cai de forma contínua, sem degraus: cada 1 dB de desvio tira 1 ponto.

| Desvio médio | Nota |
| :--- | :---: |
| Até 0.5 dB | 5 |
| Entre 0.5 e 4.5 dB | 5.5 − desvio |
| A partir de 4.5 dB | 1 |

Por exemplo, um desvio médio de 1.92 dB resulta em nota 3.58. A conta é feita pelos scripts a partir do desvio exibido com duas casas.

As bandas avaliadas são:

- Graves: 20 a 250 Hz.
- Médios: 250 Hz a 4 kHz.
- Agudos: 4 a 10 kHz.

Desvios para cima e para baixo recebem o mesmo peso. Frequências acima de 10 kHz não entram na pontuação devido à menor confiabilidade das medições nessa região.

### Uso

A Nota Uso considera minha experiência com o bocal, a carcaça, o conforto, o cabo e as ponteiras, além da possibilidade de trocar o cabo.

São avaliados 5 itens, cada um valendo 0 ou 1 ponto:

| # | Grupo | Item | Critério para 1 ponto | Critério para 0 ponto |
| :---: | :--- | :--- | :--- | :--- |
| 1 | Bocal | Bocal compatível (≤ 6.0 mm) | Diâmetro máximo de até 6.0 mm. | Diâmetro superior a 6.0 mm. |
| 2 | Conforto | Confortável após 60 minutos | A carcaça não causa pressão, dor ou desconforto após 60 minutos de uso. | Causa pressão, dor ou desconforto após 60 minutos de uso. |
| 3 | Cabo | Flexível e sem microfonia | O cabo é flexível, desenrola facilmente e não produz ruídos claramente audíveis ao entrar em contato com a roupa. | O cabo apresenta rigidez excessiva, dificuldade para desenrolar ou microfonia incômoda. |
| 4 | Ponteiras | Silicone macio e flexível | As ponteiras de silicone dobram ao meio facilmente, utilizando apenas dois dedos, sem esforço. | As ponteiras são rígidas e não dobram facilmente ao meio. |
| 5 | Reparo | Troca de cabo | Cabo removível e com conexão fácil de encontrar. | Cabo fixo ou com conexão proprietária. |

A Nota Uso corresponde à soma dos pontos obtidos, variando de 0 a 5.

Cada critério representa 20% da Nota Uso e, consequentemente, 5% da Nota Geral.

Os critérios foram escolhidos para avaliar aspectos que influenciam diretamente minha experiência de uso, evitando excesso de itens e sobreposição entre avaliações.

Utilizo sempre o cabo original, as ponteiras inclusas e os mesmos critérios de teste.

O limite de 6.0 mm do bocal é específico do meu canal auditivo. O critério de conforto reflete minha experiência pessoal. O critério de troca de cabo é objetivo e segue a especificação do fabricante.

Construção, embalagem, estojo e acessórios extras são comentados nas avaliações individuais em `Extras`, mas não influenciam a nota.

## Assinatura sonora

A assinatura descreve o perfil tonal de cada IEM, classificado visualmente pelos gráficos gerados pelo script `graficos.py`.

Cada IEM recebe uma única classificação, escolhida entre:

| Assinatura | Característica |
|---|---|
| Neutro | Equilíbrio tonal geral. |
| Neutro quente | Equilíbrio tonal com leve ênfase nos graves e médios-baixos. |
| Neutro brilhante | Equilíbrio tonal com leve ênfase nos agudos. |
| Quente | Graves e médios-baixos em evidência, com maior corpo sonoro. |
| Baixudo | Forte predominância dos graves. |
| Em U | Graves e agudos destacados, com médios relativamente preservados. |
| Em V | Graves e agudos destacados, com médios recuados. |
| Brilhante | Agudos claramente em evidência. |
| Escuro | Agudos atenuados, com apresentação mais sombreada. |
| Suave | Apresentação sem picos ou excessos agressivos nos agudos. |
| Magro | Pouco peso nos graves e menor corpo sonoro. |
| Focado nos médios | Médios e vocais em evidência. |

A classificação é subjetiva e considera o formato geral da curva.

## Medições e limitações

As curvas de resposta em frequência vêm de medições publicadas no [squig.link](https://squig.link/). Os arquivos utilizados estão na pasta [medicoes/](medicoes/).

As medições físicas, como peso, maior diâmetro do bocal e maior comprimento da carcaça, são feitas por mim com balança e paquímetro digitais.

As especificações técnicas são obtidas dos fabricantes.

**Limitações:**

- As medições podem variar conforme o equipamento, a unidade e as condições de teste.
- Os resultados são especialmente sensíveis ao posicionamento do IEM nos graves profundos e nos agudos. Os agudos (4 a 10 kHz) são a região menos confiável, então as notas de Agudos merecem mais cautela que as de Graves e Médios.
- A proximidade da curva Harman não representa, por si só, qualidade sonora absoluta.
- A assinatura sonora é uma classificação visual e subjetiva, não uma medida universal ou uma avaliação de qualidade.
- A Nota Uso é pessoal e pode não corresponder à experiência de outras pessoas.
- O ranking mede o quanto cada IEM me agrada em som e uso, não o custo-benefício. O preço aparece na tabela, mas não entra na nota: prefiro não privilegiar IEMs apenas razoáveis por serem baratos.

## Arquivos do projeto

| Caminho | Conteúdo |
| :--- | :--- |
| [avaliacoes/](avaliacoes/) | Avaliações individuais |
| [medicoes/](medicoes/) | Curvas de resposta em frequência |
| [graficos/](graficos/) | Resposta em frequência de cada IEM contra o alvo |
| [target/](target/) | Curva Harman IE 2019 |
| [comparativo.csv](comparativo.csv) | Ranking e notas consolidadas |
| [desvios.csv](desvios.csv) | Resultados das medições |
| [scripts/](scripts/) | Scripts de cálculo e geração de gráficos |

## Dependências

Os scripts usam Python 3 com as bibliotecas `matplotlib` e `numpy`. Para instalar:

```bash
pip install matplotlib numpy
```

## Atualização do projeto

Execute os comandos na raiz do projeto.

**Atualizar medições e gráficos:**

```bash
python3 scripts/graficos.py
```

**Atualizar o ranking e o comparativo:**

```bash
python3 scripts/comparativo.py
```

## Adicionar um IEM

1. Coloque a medição na pasta `medicoes/`.
2. Execute `python3 scripts/graficos.py` para gerar os gráficos e a avaliação inicial, já com os desvios calculados.
3. Preencha os campos restantes (marcados com `X`) e os 5 critérios de uso no arquivo gerado em `avaliacoes/`.
4. Execute `python3 scripts/comparativo.py` para conferir os dados e atualizar o ranking.
