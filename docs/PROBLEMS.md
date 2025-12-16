# Problemas Encontrados e Soluções

Este documento descreve os principais desafios encontrados durante a implementação do desafio "Adaptive Lying Oracle" e como foram resolvidos.

## 1. Problema: Impossibilidade de Testar o Oráculo Mentiroso

### Descrição do Problema

O desafio especifica que o oráculo deve começar a mentir após t=200 passos. No entanto, com um intervalo de apenas 1-100 e usando busca binária eficiente, o agente consegue encontrar o número oculto em **aproximadamente 7 passos** (log₂(100) ≈ 6.64).

Isso significa que o episódio termina muito antes de atingir t=200, tornando **impossível testar a funcionalidade de detecção de mentiras** do agente - que é justamente o core do desafio!

### Solução Implementada

Para testar a funcionalidade do oráculo mentiroso, ajustamos temporariamente o `liar_oracle_threshold` para valores menores durante o desenvolvimento, permitindo fazer uma solução mais robusta:

```python
# env.py - Para testes
liar_oracle_threshold = 3  # ou 5, para forçar a mentira cedo
```

Isso permitiu:
- Verificar se o agente detecta contradições corretamente
- Testar a lógica de inversão de crença
- Validar o reset do intervalo de busca
- Debugar o comportamento adaptativo

**Observação**: Para demonstração final ou quando o número oculto é sorteado entre valores maiores que permitam mais iterações, o threshold deve ser restaurado para 200 conforme a especificação original.

## 2. Problema: Lógica de Busca Binária Incorreta

### Descrição do Problema

A primeira implementação tinha um bug crítico na atualização do intervalo de busca:

```python
# ERRADO
if effective_answer:  # hidden > action
    proposed_lower = action + 1
    proposed_upper = self.upper
else:  # hidden <= action
    proposed_lower = self.lower
    proposed_upper = action  # BUG: deveria ser action - 1
```

Quando `hidden <= action`, sabemos que o número **não é** `action` (pois já testamos). Portanto, o novo limite superior deve ser `action - 1`, não `action`.

### Impacto

Este bug causava:
- O agente ficava preso testando o mesmo número repetidamente
- Intervalos impossíveis não eram detectados corretamente
- Loop infinito quando o número oculto era próximo aos limites (especialmente números baixos)

### Exemplo do Bug

```
Hidden: 22
Step 1: action=50, answer=False → [1, 50]  ✓
Step 2: action=25, answer=False → [1, 25]  ✓
Step 3: action=13, answer=True  → [14, 25] ✓
Step 4: action=19, answer=True  → [20, 25] ✓
Step 5: action=22, answer=False → [20, 22] ✗ ERRADO! Deveria ser [20, 21]
Step 6: action=21, answer=True  → [22, 22] ✓
Step 7: action=22, answer=False → [22, 22] ✗ LOOP! Nunca detecta que 22 está fora
```

### Solução

Correção da lógica de busca binária:

```python
# CORRETO
if effective_answer:  # hidden > action
    proposed_lower = action + 1
    proposed_upper = self.upper
else:  # hidden <= action
    proposed_lower = self.lower
    proposed_upper = action - 1  # ✓ Exclui o action já testado
```

Agora o agente:
- Atualiza os intervalos corretamente
- Detecta contradições quando `lower > upper`
- Nunca fica preso em loops infinitos
- Funciona para qualquer posição do número oculto (baixo, alto ou meio)

## 3. Problema: Visualização com Poucos Dados

### Descrição do Problema

Ao calcular a média móvel (rolling mean) com janela de 20 passos, o código falhava quando o episódio terminava antes de 20 steps:

```python
ValueError: x and y must have same first dimension, but have shapes (0,) and (16,)
```

### Solução

Adicionamos verificação antes de calcular a média móvel:

```python
window = 20
if len(rewards) >= window:
    rolling_mean = np.convolve(rewards, np.ones(window)/window, mode='valid')
    ax1.plot(steps_list[window-1:], rolling_mean, linewidth=2, 
             label=f'Rolling mean (window={window})')
else:
    print(f"Not enough data points for rolling mean (need {window}, have {len(rewards)})")
```

Isso permite que o notebook funcione mesmo quando o agente é muito eficiente(ou utiliza o modelo de desafio inicial) e encontra o número rapidamente.

## Resumo das Lições Aprendidas(TLDR)

1. **Testes realistas**: Para testar edge cases (oráculo mentiroso), ajustes temporários nos parâmetros são necessários quando a solução ótima impede o teste do comportamento desejado

2. **Busca binária**: Atenção aos detalhes - excluir valores já testados é fundamental para evitar loops

3. **Simplicidade**: Detecção de contradições baseada em lógica simples (intervalo impossível) é mais robusta que históricos complexos