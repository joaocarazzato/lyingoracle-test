# Oráculo Mentiroso - RL Toy

## Visão Geral

Este repositório implementa um agente que aprende a lidar com um **oráculo mentiroso** em um ambiente de aprendizado por reforço. O desafio foi apresentado por um recrutador em uma entrevista técnica e demonstra como um agente pode detectar e se adaptar a mudanças na dinâmica do ambiente.

## Descrição do Desafio

O agente deve encontrar um número oculto (1-100) perguntando a um oráculo se "o número é maior que k?" O problema: o oráculo diz a verdade nos primeiros 200 passos, depois **começa a mentir** (invertendo suas respostas) nos 300 passos restantes.

### Ambiente (`env.py`)

- **Número oculto**: Inteiro aleatório entre 1-100
- **Ação do agente**: Escolher k (1-100), perguntando "hidden > k?"
- **Comportamento do oráculo**:
  - t < 200: Retorna booleano verdadeiro
  - t ≥ 200: Retorna booleano invertido (mente)
- **Duração do episódio**: 500 passos
- **Recompensas**:
  - `+1.0` se o agente acertar o número (episódio termina)
  - `-0.01` por passo caso contrário

### Agente (`agent.py`)

O agente implementa uma estratégia de busca binária adaptativa:

1. **Suposição inicial**: Oráculo é verdadeiro
2. **Busca binária**: Mantém intervalo de busca `[lower, upper]`
3. **Detecção de contradição**: Quando o intervalo se torna impossível (`lower > upper`), o agente percebe que o oráculo está mentindo
4. **Adaptação**: Muda sua crença e inverte a interpretação das respostas do oráculo
5. **Recuperação**: Reseta o intervalo de busca e continua com a nova crença

### Notebook (`notebook.ipynb`)

O notebook demonstra:
- Simulação completa de 500 passos
- Métricas de desempenho e logs
- Visualização com dois gráficos:
  - **Recompensa ao longo do tempo** com média móvel (janela=20)
  - **Crença do agente** sobre a veracidade do oráculo
- Mostra a queda de desempenho em t=200 quando o oráculo começa a mentir
- Mostra a recuperação quando o agente detecta a contradição e se adapta

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

Execute o notebook Jupyter para ver o agente em ação.

O notebook mostrará como o agente encontra com sucesso o número oculto ao se adaptar ao comportamento mutável do oráculo.

## Problemas

Os problemas encontrados e que precisaram ser contornados a partir das necessidades do desafio original podem ser encontrados em `docs/PROBLEMS.md`.