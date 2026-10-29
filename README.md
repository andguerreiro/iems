# IEMs Avaliados

| Posição | IEM | Nota (1 a 5) | Preço (USD) | Assinatura |
| :---: | :--- | :---: | :---: | :--- |
| **1º** | [Kefine Klean](/avaliacoes/kefine_klean.md) | **4,2** | 49 | Harman-Quente |
| **2º** | [Kiwi Ears Cadenza 2](/avaliacoes/kiwi_ears_cadenza_2.md) | **4,2** | 50 | Balanceado-Quente |
| **3º** | [KZ Castor](/avaliacoes/kz_castor.md) | **4,0** | 15 | Harman-leve |
| **4º** | [Sennheiser IE100 Pro](/avaliacoes/sennheiser_ie100_pro.md) | **4,0** | 109 | Quente |
| **5º** | [KZ EDX Pro X](/avaliacoes/kz_edx_pro_x.md) | **3,4** | 10 | Quente-brilhante |
| **6º** | [Truthear Zero Red](/avaliacoes/truthear_zero_red.md) | **2,8** | 55 | Neutra |
| **7º** | [KZ ZS12 Pro X](/avaliacoes/kz_zs12_pro_x.md) | **2,8** | 59 | Neutra-brilhante |
| **8º** | [JBL Tune 110](/avaliacoes/jbl_tune_110.md) | **1,8** | 15 | Em V |

## Como avalio

Cada IEM recebe nota inteira de 1 a 5 em cinco itens: Graves, Médios, Agudos, Físico e Acessórios.

(1) = Péssimo, (2) = Ruim, (3) = OK, (4) = Ótimo e (5) = Excelente

A nota geral é a média simples dos cinco itens. Empates na nota geral são desempatados pelo menor preço.

Em graves, médios e agudos, a nota mede a distância média absoluta entre a curva e a Harman IE 2019 na banda, considerando desvios tanto para cima quanto para baixo:

- Até 1,5 dB: Excelente (5)
- Acima de 1,5 até 2,5 dB: Ótimo (4)
- Acima de 2,5 até 3,5 dB: OK (3)
- Acima de 3,5 até 5 dB: Ruim (2)
- Acima de 5 dB: Péssimo (1)

Se a curva vai pros dois lados na mesma banda, o texto descreve como irregular.

Físico = conforto, ergonomia e construção.

Acessórios = cabo, ponteiras e embalagem.

A massa de cada lado foi medida com uma balança digital, e o maior diâmetro do bocal, com um paquímetro digital.

### Como o desvio médio por banda é calculado

O desvio médio de cada banda é calculado por script, a partir dos dados da medição e da curva-alvo Harman IE 2019, seguindo estes passos:

1. **Média das medições:** quando há mais de uma medição do mesmo IEM, a curva usada é a média ponto a ponto entre elas.
2. **Grade comum:** a curva do IEM e a Harman IE 2019 são reamostradas por interpolação linear numa mesma grade de 1000 pontos, espaçados de forma logarítmica entre 20 Hz e 20 kHz.
3. **Normalização em 1 kHz:** a curva do IEM é deslocada na vertical para ficar com o mesmo nível da Harman em 1 kHz. Só o nível geral muda, o formato da curva não.
4. **Distância ponto a ponto:** em cada ponto da grade, calcula-se o valor absoluto da diferença, em dB, entre a curva do IEM e a Harman. Desvios para cima e para baixo contam igual e não se cancelam.
5. **Média por banda:** o desvio médio da banda é a média simples dessas distâncias nos pontos que caem dentro dela:
   - Graves: 20 Hz até 250 Hz
   - Médios: 250 Hz até 4 kHz
   - Agudos: 4 kHz até 10 kHz

   O limite inferior de cada banda entra e o superior não. A região do Ar (10–20 kHz) fica fora do cálculo.
6. **Nota:** o valor bruto da média é comparado com a régua acima, sem arredondar, e cada limite de faixa vale "até" (inclusive). Nos textos, o desvio aparece com duas casas decimais.

Como a grade é logarítmica, cada oitava pesa igual no cálculo, e não cada Hz. Isso acompanha a forma como o gráfico é lido e como se ouve a diferença entre frequências.

### Bandas e regiões

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

A região do Ar (10–20 kHz) não entra na nota, porque as medições variam muito entre sistemas nessa faixa. Se houver algo relevante ali, aparece só no texto da avaliação.
