def busca_binaria(lista, alvo, inicio, fim):
    if inicio > fim:
        return -1  # Elemento não encontrado
    meio = (inicio + fim) // 2
    if lista[meio] == alvo:
        return meio  # Retorna o índice do elemento
    elif lista[meio] < alvo:
        return busca_binaria(lista, alvo, meio + 1, fim)
    else:
        return busca_binaria(lista, alvo, inicio, meio - 1)
    
lista = [1, 3, 5, 7, 9, 11, 13]
alvo = 13


indice_rec = busca_binaria(lista, alvo, 0, len(lista) - 1)
print(f"Índice do elemento: {indice_rec}")

