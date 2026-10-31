# IEMs Avaliados

| Posição | IEM | Nota (1 a 5) | Preço (USD) | Assinatura |
| :---: | :--- | :---: | :---: | :--- |
| **1º** | [Kefine Klean](/avaliacoes/kefine_klean.md) | **4,4** | 49 | Harman-quente |
| **2º** | [Kiwi Ears Cadenza 2](/avaliacoes/kiwi_ears_cadenza_2.md) | **4,2** | 50 | Harman-suave |
| **3º** | [KZ Castor](/avaliacoes/kz_castor.md) | **4,0** | 15 | Harman |
| **4º** | [Sennheiser IE 100 Pro](/avaliacoes/sennheiser_ie_100_pro.md) | **4,0** | 109 | Neutra-leve |
| **5º** | [KZ EDX Pro X](/avaliacoes/kz_edx_pro_x.md) | **3,4** | 10 | Quente-brilhante |
| **6º** | [Truthear Zero Red](/avaliacoes/truthear_zero_red.md) | **3,4** | 55 | Neutra |
| **7º** | [KZ ZS12 Pro X](/avaliacoes/kz_zs12_pro_x.md) | **2,8** | 59 | Neutra-brilhante |
| **8º** | [JBL Tune 110](/avaliacoes/jbl_tune_110.md) | **2,0** | 15 | Em V |

## Como avalio

Cada IEM recebe nota inteira de 1 a 5 em cinco itens: Graves, Médios, Agudos, Físico e Acessórios.

(1) = Péssimo, (2) = Ruim, (3) = OK, (4) = Ótimo e (5) = Excelente

A **nota geral** é a média simples dos cinco itens, mostrada com uma casa decimal. Como cada item tem o mesmo peso, o som (Graves, Médios e Agudos) vale 3/5 da nota, e Físico e Acessórios valem 2/5. Esses dois últimos são avaliações subjetivas, sem medição. Empates na nota geral são desempatados pelo menor preço. O preço não entra na nota. Também não calculo custo-benefício: ao comparar vários produtos da mesma categoria, uma razão entre nota e preço favorece os mais baratos mesmo quando são claramente menos refinados. A nota e o preço estão lado a lado na tabela para quem quiser fazer essa conta.

### Graves, Médios e Agudos

A nota mede o quanto a curva de resposta em frequência do IEM se afasta da [**Harman IE 2019**](/target/HarmanIE2019.txt), a curva-alvo de referência para fones intra-auriculares, construída a partir de pesquisas de preferência de ouvintes. Ela mede proximidade com esse alvo, não qualidade sonora em si, e o gosto de cada pessoa pode ser diferente.

A distância é a média, em dB, dos desvios para cima e para baixo na banda:

- Até 1,5 dB: Excelente (5)
- Acima de 1,5 até 2,5 dB: Ótimo (4)
- Acima de 2,5 até 3,5 dB: OK (3)
- Acima de 3,5 até 5 dB: Ruim (2)
- Acima de 5 dB: Péssimo (1)

Como a nota é dada por faixas, notas vizinhas podem representar diferenças pequenas: um desvio de 2,49 dB recebe nota 4 e um de 2,51 dB recebe nota 3. O desvio em dB é a informação mais precisa.

Nos textos, uma banda é descrita como "irregular" quando a curva fica acima do alvo em parte da faixa e abaixo em outra. A nota trata os dois lados do mesmo jeito.

### Físico e Acessórios

- **Físico:** conforto, ergonomia e construção.
- **Acessórios:** cabo, ponteiras e embalagem.

### De onde vêm os dados

- **Curvas de resposta:** vêm de [medições](/medicoes) publicadas no squig.link, feitas por várias fontes independentes. Elas podem variar um pouco entre fontes, equipamentos e unidades do mesmo modelo, principalmente nos agudos mais altos.
- **Massa e bocal:** a massa de cada lado foi medida com balança digital, e o maior diâmetro do bocal, com paquímetro digital.
- **Impressões de uso:** conforto, cabo, ponteiras e embalagem são avaliados por mim, com as unidades que comprei.
- **Independência:** todas as unidades foram compradas por mim, sem patrocínio ou afiliados.

## Bandas e regiões

| Banda | Região | Faixa | Excesso | Falta | Avaliada |
| :--- | :--- | :--- | :--- | :--- | :---: |
| Graves | Sub-graves | 20–60 Hz | Ressonante | Anêmico | Sim |
| Graves | Graves | 60–250 Hz | Inchado | Magro | Sim |
| Médios | Médios-graves | 250–500 Hz | Turvo | Oco | Sim |
| Médios | Médios | 500 Hz–2 kHz | Anasalado | Afastado | Sim |
| Médios | Médios-altos | 2–4 kHz | Áspero | Apagado | Sim |
| Agudos | Presença | 4–6 kHz | Estridente | Distante | Sim |
| Agudos | Brilho | 6–8 kHz | Sibilante | Escuro | Sim |
| Agudos | Agudos | 8–10 kHz | Farpado | Abafado | Sim |
| Agudos | Ar | 10–20 kHz | Estrondoso | Fechado | Não |

A região do Ar (10–20 kHz) não entra na nota, porque as medições variam muito entre sistemas nessa faixa.

## Como o desvio médio é calculado

Os desvios são calculados por [script](/script/gerar_grafico.py). Ele lê as medições de `medicoes/` e o alvo de `target/`, agrupa os arquivos do mesmo modelo (ex.: `Nome [1].txt` e `Nome [2].txt`), processa cada IEM, salva um gráfico por modelo em `graficos/` e gera o `desvios.csv` na raiz do projeto. Pode ser executado de qualquer diretório (`python3 script/gerar_grafico.py`). Para cada IEM, os passos são:

1. **Curva do IEM:** se há mais de uma medição do mesmo modelo, usa-se a média entre elas.
2. **Mesma base de comparação:** a curva do IEM e a Harman IE 2019 são colocadas na mesma grade de frequências, em escala logarítmica, de 20 Hz a 20 kHz.
3. **Alinhamento em 1 kHz:** a curva do IEM é deslocada para ter o mesmo nível da Harman em 1 kHz. Só o nível muda, o formato da curva não.
4. **Distância em cada ponto:** calcula-se a diferença absoluta, em dB, entre o IEM e a Harman. Desvios para cima e para baixo contam igual e não se cancelam.
5. **Média por banda:** é a média dessas distâncias dentro de cada banda (Graves: 20–250 Hz, Médios: 250 Hz–4 kHz, Agudos: 4–10 kHz). O limite inferior entra e o superior não.
6. **Desvio total:** é a média das distâncias em todos os pontos de 20 Hz a 10 kHz, e não a média das três bandas. A região do Ar (10–20 kHz) fica de fora, como na nota.
7. **Desvio máximo:** é a maior distância em um único ponto entre 20 Hz e 10 kHz, junto com a frequência em que ocorre. É só informativo e não entra na nota: serve para mostrar picos e vales estreitos que a média suaviza.
8. **Nota:** o desvio de cada banda é comparado com a escala acima sem arredondar. Nos textos, ele aparece com duas casas decimais. Nem o desvio total nem o desvio máximo entram na nota geral.

Como a grade é logarítmica, cada oitava pesa igual, e não cada Hz. Por isso Graves (cerca de 3,6 oitavas) e Agudos (cerca de 1,3 oitava) são médias sobre faixas de larguras bem diferentes. Pelo mesmo motivo, o desvio total pesa cada banda pela sua largura em oitavas, e os Agudos influenciam menos do que influenciariam numa média simples das três bandas.

## Comparativo e desvios

O [comparativo.csv](comparativo.csv) reúne os dados de todos os IEMs. Nele, "Nota Som" é a média simples das notas de graves, médios e agudos.

O [desvios.csv](desvios.csv) mostra, para cada IEM, o desvio médio por banda (graves, médios e agudos), o desvio total, ou seja, a média da distância ao alvo Harman IE 2019 em toda a curva de 20 Hz a 10 kHz, e o desvio máximo com a frequência em que ocorre. As linhas são ordenadas pelo desvio total, do mais ao menos próximo do alvo. Esse ranking mede só a fidelidade da curva e pode diferir do ranking por nota geral, que também considera Físico e Acessórios.
