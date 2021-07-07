# Importações realizadas
import random
import time
import copy

# Função de Criar uma Matriz com valores 0 e 1
def criaMatrizC(linhas, colunas):
    #PREENCHIMENTO ALEATORIO DA MATRIZ
    return [[random.randint(0, 1) for i in range(colunas)] for j in range(linhas)]

# Função para visualizar a matriz Gráfica
def visualiza(matriz, linhas, colunas):
    i = 0
    j = 0

    # SUBISTITUIR OS `0` POR | | E O `1` POR |X|
    while i < linhas:
        while j < colunas:
            if matriz[i][j] == 0:
                print('| |, ', end='')
            else:
                print('|X|, ', end='')
            j += 1
        j = 0
        print('')
        i += 1

#Função First Fit (PRIMEIRA FUNÇÃO)
def firstFit(matriz, colunas, size):
    # Variável que guarda a quantidade de posições vazias em sequência
    contador = 0

    j = 0

    # Variáveis que guardam as coordenadas de um elemento, pra acessar um dado elemento usar: matriz[posX][posY]
    posX = -1
    posY = -1

    for linha in matriz:

        # Atualiza o posX pra cada linha da matriz
        posX += 1

        for elemento in linha:
            # Verifica se o posY é a última posição da lista, caso seja, será zerado pois passaremos para outra linha
            if posY == colunas - 1:
                posY = 0
            # Se ainda não for o último elemento, somamos 1 a coordenada y
            else:
                posY += 1

            # Verifica se o espaço em questão é um espaço vazio
            if elemento == 0:
                contador += 1

                # Verifica se a quantidade de espaços vazios corresponde ao tamanho a ser alocado
                if contador == size:
                    # print(posX, posY)  ---------> para debuggar, não descomentar

                    # Iterar a quantidade de vezes a ser alocada
                    for i in range(size):
                        # Testar se a alocação cabe em somente uma linha
                        if posY >= size - 1:
                            matriz[posX][posY - i] = 1

                        # Caso não seja possível a alocação em uma única linha
                        else:
                            # Verifica se é o primeiro elemento da linha
                            if posY - i >= 0:
                                # print(posY - i)
                                matriz[posX][posY - i] = 1
                            # Caso seja o primeiro elemento, volta uma linha e começa pelo ultimo elemento da nova linha
                            else:
                                # print('mudando matriz[{}][{}]'.format(posX - 1, (colunas - 1) - i)) -----> para debbugar
                                matriz[posX - 1][(colunas - 1) - j] = 1
                                j += 1
                    return matriz

            # Se for espaço ocupado, reinicia o contador
            else:
                contador = 0
    # Retorna False caso não haja expaço suficiente
    return False

#FUNÇÃO PARA BUSCAR ESPAÇOS NA MATRIZ
def buscaEspaçoMenor(matriz, linhas, colunas, size):
    contador = 0

    # Variável pra guardar os tamanhos dos espaços vazios que estão disponíveis
    empty_spaces = []
    empty_spaces_used = []

    # Variáveis pra guardar as coordenadas dos espaços vazios
    posX = -1
    posY = -1

    for linha in matriz:
        posX += 1

        for elemento in linha:
            # Verifica se o posY é a última posição da lista, caso seja, será zerado pois passaremos para outra linha
            if posY == colunas - 1:
                posY = 0
            # Se ainda não for o último elemento, somamos 1 a coordenada y
            else:
                posY += 1

            # print('passando pelo elemento [{}][{}] - {}'.format(posX, posY, matriz[posX][posY]))

            # Verifica se o espaço em questão é um espaço vazio
            if elemento == 0:
                contador += 1

                if posX == linhas - 1 and posY == colunas - 1:
                    if contador not in empty_spaces_used:
                        if contador == size:
                            return [contador, (posX, posY)]
                        elif contador > size:
                            if contador not in empty_spaces_used:
                                empty_spaces.append([contador, (posX, posY)])

            else:
                # Verifica se passamos por um espaço vazio do tamanho exato a ser alocado
                if contador == size:
                    # A posição atual na varredura é a do 1, então devemos voltar uma casa para informar onde termina
                    #  o espaço vazio, para isso devemos testar se estamos na primeira posição da lista
                    if posY > 0:
                        return [contador, (posX, posY - 1)]
                    # Caso estivermos na primeira posição, volta uma linha e retorna as informações
                    else:
                        return [contador, (posX - 1, colunas - 1)]

                # Caso não seja um espaço do tamanho exato a ser alocado, adiciona o tamanho do espaço e as coordenadas
                # de onde esse termina em uma lista e continua a iteração
                elif contador > size and contador not in empty_spaces_used:
                    empty_spaces_used.append(contador)
                    if posY > 0:
                        empty_spaces.append([contador, (posX, posY - 1)])
                    else:
                        empty_spaces.append([contador, (posX - 1, colunas - 1)])
                contador = 0
    # Caso não exista um espaço do tamanho exato a ser alocado, retorna o tamanho do menor espaço disponível e as
    # coordenadas de onde esse termina
    try:
        return sorted(empty_spaces, key=lambda x: x[0])[0]
    except:
        return False

#FUNÇÃO BEST FIT (SEGUNDA FUNÇÃO)
def bestFit(matriz, colunas, size, espaço):
    try:
        # Variável que guarda o tamanho do menor espaço vazio encontrado pela varredura
        empty_size = espaço[0]
        # Coordenadas de onde termina o espaço vazio
        posX = espaço[1][0]
        posY = espaço[1][1]
    except:
        return False

    j = 0

    # Existem 2 casos possíveis, ou o espaço encontrado é exatamente igual ao tamanho a ser alocado, ou não
    # Testa se é o caso de não serem iguais os tamanhos
    if size != empty_size:
        # Altera a posição de onde devemos iniciar a alocação
        new_posY = posY - (empty_size - size)

        for i in range(size):
            if new_posY - i >= 0:
                matriz[posX][new_posY - i] = 1
            else:
                matriz[posX - 1][(colunas - 1) - j] = 1
                j += 1
    else:
        for i in range(size):
            if posY - i >= 0:
                matriz[posX][posY - i] = 1
            else:
                matriz[posX - 1][(colunas - 1) - j] = 1
                j += 1

    return matriz


def buscaEspaçoMaior(matriz, linhas, colunas, size):
    contador = 0

    # Variável pra guardar os tamanhos dos espaços vazios que estão disponíveis
    empty_spaces = []
    empty_spaces_used = []

    # Variáveis pra guardar as coordenadas dos espaços vazios
    posX = -1
    posY = -1

    for linha in matriz:
        posX += 1

        for elemento in linha:
            # Verifica se o posY é a última posição da lista, caso seja, será zerado pois passaremos para outra linha
            if posY == colunas - 1:
                posY = 0
            # Se ainda não for o último elemento, somamos 1 a coordenada y
            else:
                posY += 1

            # Verifica se o espaço em questão é um espaço vazio
            if elemento == 0:
                contador += 1
                if posX == linhas - 1 and posY == colunas - 1:
                    if contador not in empty_spaces_used and contador >= size:
                        empty_spaces.append([contador, (posX, posY)])

            elif elemento == 1:
                if contador not in empty_spaces_used and contador >= size:
                    empty_spaces_used.append(contador)

                    if posY > 0:
                        empty_spaces.append([contador, (posX, posY - 1)])
                    else:
                        empty_spaces.append([contador, (posX - 1, colunas - 1)])
                contador = 0
    try:
        return sorted(empty_spaces, key=lambda x: x[0], reverse=True)[0]
    except:
        return False

# FUNÇÃO WORS FIT ( TERCEIRA FUNÇÃO )
def worstFit(matriz, colunas, size, espaço):
    try:
        empty_size = espaço[0]
        posX = espaço[1][0]
        posY = espaço[1][1]
    except:
        return False

    j = 0

    new_posY = posY - (empty_size - size)

    for i in range(size):
        if new_posY - i >= 0:
            matriz[posX][new_posY - i] = 1
        else:
            matriz[posX - 1][(colunas - 1) - j] = 1
            j += 1
    return matriz

# FUNÇÃO DE DESALOCAÇÃO ( QUARTA FUNÇÃO )
def desaloca(matriz, colunas, posXI, posYI, posXF, posYF):
    try:
        while posXI != posXF or posYI != posYF:
            matriz[posXI][posYI] = 0

            if posYI + 1 > colunas - 1:
                posYI = 0
                posXI += 1
            else:
                posYI += 1
        matriz[posXF][posYF] = 0
        return matriz
    except IndexError:
        return False

# FUNÇÃO DE TESTE ( QUINTA FUNÇÃO )
def modoTeste(matriz, linhas, colunas, numeroSimulaçoes):
    matrizOFC = matriz
    m1 = copy.deepcopy(matrizOFC)
    m2 = copy.deepcopy(matrizOFC)
    m3 = copy.deepcopy(matrizOFC)

    # CARACTERISTICAS A SEREM MOSTRADAS AO USUÁRIO!
    falhas = 0
    sucessos = 0
    desalocou = 0
    tempo_inicial = time.time()

    i = 0

    while i < numeroSimulaçoes:
        tamanho = random.randint(1, 20)
        decide_desaloca = random.randint(1, 10)

        # PRIMEIRA FUNÇÃO FIRST FIT
        f1 = firstFit(m1, linhas, tamanho)
        # SEGUNDA FUNÇÃO BESTFIT
        f2 = bestFit(m2, colunas, tamanho, buscaEspaçoMenor(m2, linhas, colunas, tamanho))
        # TERÇA FUNÇÃO  WORS FIT
        f3 = worstFit(m3, colunas, tamanho, buscaEspaçoMaior(m3, linhas, colunas, tamanho))


        if decide_desaloca == 1:
            desalocou += 1
            posXI = random.randint(0, linhas - 1)
            posYI = random.randint(0, colunas - 1)
            posXF = random.randint(posXI, linhas - 1)
            posYF = random.randint(posYI, colunas - 1)

            desaloca(m1, colunas, posXI, posYI, posXF, posYF)
            desaloca(m2, colunas, posXI, posYI, posXF, posYF)
            desaloca(m3, colunas, posXI, posYI, posXF, posYF)

        if not f1 or not f2 or not f3:
            falhas += 1
        else:
            sucessos += 1

        i += 1

    print('Alocações bem-sucedidas: ' + str(sucessos))
    print('Alocações mal-sucedidas: ' + str(falhas))
    print('Tempo decorrido: ' + str(time.time() - tempo_inicial))
    print('Número de desalocações pseudo-randomicas durante a simulação: ' + str(desalocou))

# DICIONÁRIO ( OPÇÕES )
options = {1: visualiza,
           2: firstFit,
           3: bestFit,
           4: worstFit,
           5: desaloca,
           6: modoTeste}

# LINHAS E COLUNAS PARA CRIAR A MATRIZ INICIAL!

# NÚMERO DE LINHAS DA MATRIZ
linhas = int(input('\n'
                   'BEM VINDO AO SIMULADOR DE ALOCAÇÕES!\n'
                   '\n'
                   'Vamos alocar uma matriz para começar as operações!\n'
                   '\n'
                   'Quantas linhas terá sua matriz?\n'))

print('')
# NÚMEROS DE COLUNAS DA MATRIZ
colunas = int(input('Quantas colunas terá sua matriz?\n'))

matriz = criaMatrizC(linhas, colunas)

# MENU PARA ESCOLHER UMA DAS OPÇÕES
while True:
    print('=========================================')
    # OPÇÕES
    escolhaMain = int(input('Escolha uma opção:\n'
                            '\n'
                            '1 - Visualização de memória\n'
                            '2 - Alocação first fit\n'
                            '3 - Alocação best fit\n'
                            '4 - Alocação worst fit\n'
                            '5 - Desalocação\n'
                            '6 - Modo Teste\n'
                            '7 - Sair\n'
                            'Digite a opção desejada: '))

    # ESCOLHA PARA SAIR
    if escolhaMain == 7:
        break

    # func armazena o nome da função, declarada no dicionário 'options'
    func = options.get(escolhaMain, lambda: 'Opção Inválida!\n')

    # ESCOLHA NÚMERO 1 (VISUALIZAR A MEMÓRIA)
    if escolhaMain == 1:
        while True:
            func(matriz, linhas, colunas)

            print('')
            # sair da função
            try:
                decider = int(input('Digite 1 para voltar.\n'))
            except:
                print("Você digitou alguma coisa inválida!")
                break
            if decider == 1:
                break
            else:
                print("Você digitou alguma coisa inválida!")
                break

    # ESCOLHA NÚMERO 2 ( FIRST FIT )
    if escolhaMain == 2:
        while True:
            # TAMANHO DO ESPAÇO QUE DESEJA-SE SER ALOCADO
            size = int(input('Qual o tamanho do espaço que deseja alocar na modalidade best fit?\n'))
            # VISUALIZAÇÃO DA MATRIZ ANTES
            print('A matriz antes da alocação era assim: ')
            visualiza(matriz, linhas, colunas)
            # VISUALIZAÇÃO DA FINAL DEPOIS DA DESALOCAÇÃO
            print('A matriz depois da alocação ficou assim: ')
            result = func(matriz, colunas, size)

            if not result:
                print('A alocação fahou!')
            else:
                visualiza(matriz, linhas, colunas)

                # SAIR DA FUNÇÃO
            try:
                decider = int(input('Digite 1 para voltar.\n'))
            except:
                print("Você digitou alguma coisa inválida!")
                break

            if decider == 1:
                break
            else:
                print("Você digitou alguma coisa inválida!")
                break

    # ESCOLHA NÚMERO 3 (BEST FIT)
    if escolhaMain == 3:
        while True:
            # TAMANHO DO ESPAÇO QUE DESEJA-SE SER ALOCADO
            size = int(input('Qual o tamanho do espaço que deseja alocar na modalidade best fit?\n'))
            # VISUALIZAÇÃO DA MATRIZ ANTES
            print('A matriz antes da alocação era assim: ')
            visualiza(matriz, linhas, colunas)
            # VISUALIZAÇÃO DA FINAL DEPOIS DA DESALOCAÇÃO
            print('A matriz depois da alocação ficou assim: ')
            result = bestFit(matriz, colunas, size, buscaEspaçoMenor(matriz, linhas, colunas, size))

            if not result:
                print('Alocação falhou!')
            else:
                visualiza(matriz, linhas, colunas)

            # SAIR DA FUNÇÃO
            try:
                decider = int(input('Digite 1 para voltar.\n'))
            except:
                print("Você digitou alguma coisa inválida!")
                break

            if decider == 1:
                break
            else:
                print("Você digitou alguma coisa inválida!")
                break

    # ESCOLHA NÚMERO 4 ( WORS FIT )
    if escolhaMain == 4:
        while True:
            # TAMANHO DO ESPAÇO QUE DESEJA-SE SER ALOCADO
            size = int(input('Qual o tamanho do espaço que deseja alocar na modalidade best fit?\n'))
            # VISUALIZAÇÃO DA MATRIZ ANTES
            print('A matriz antes da alocação era assim: ')
            visualiza(matriz, linhas, colunas)
            # VISUALIZAÇÃO DA FINAL DEPOIS DA DESALOCAÇÃO
            print('A matriz deppis da alocação ficou assim: ')
            result = worstFit(matriz, colunas, size, buscaEspaçoMaior(matriz, linhas, colunas, size))

            if not result:
                print('Alocação falhou!')
            else:
                visualiza(matriz, linhas, colunas)

            # SAIR DA FUNÇÃO
            try:
                decider = int(input('Digite 1 para voltar.\n'))
            except:
                print("Você digitou alguma coisa inválida!")
                break
            if decider == 1:
                break
            else:
                print("Você digitou alguma coisa inválida!")
                break

    # ESCOLHA NÚMERO 5 ( DESALOCAÇÃO )
    if escolhaMain == 5:
        while True:

            try:
            # POSIÇÃO INICIAL DA DESALOCAÇÃO!
                parInicial = input('Insira o par inicial no formato: x, y\n').split(', ')
                posXI, posYI = parInicial
            # POSIÇÃO FINAL DA DESALOCAÇÃO!
                parFinal = input('Insira o par final no formato: x, y\n').split(', ')
                posXF, posYF = parFinal
            except:
                print("Você digitou alguma coisa errada! tente novamente! Não esqueça de dar espaço depois da virgula!")
                break

            # VISUALIZAÇÃO DA MATRIZ ANTES
            print('A matriz antes da desalocação era assim: ')
            visualiza(matriz, linhas, colunas)

            # VISUALIZAÇÃO DA FINAL DEPOIS DA DESALOCAÇÃO
            print('A matriz depois da desalocação ficou assim: ')
            result = desaloca(matriz, colunas, int(posXI), int(posYI), int(posXF), int(posYF))

            if not result:
                print('Posição inválida!')
            else:
                visualiza(matriz, linhas, colunas)


            # SAIR DA FUNÇÃO
            try:
                decider = int(input('Digite 1 para voltar.\n'))
            except:
                print("Você digitou alguma coisa inválida!")
                break
            if decider == 1:
                break
            else:
                print("Você digitou alguma coisa inválida!")
                break

    # ESCOLHA NÚMERO 6 ( MODO DE TESTE )
    if escolhaMain == 6:
        while True:
            print('ENTRANDO NO MODO SIMULAÇÃO')
            print('')
            print('A MATRIZ DESSE MODO É DE TAMANHO 5000x5000.')
            print('')

            # DIGITAR O NÚMERO DE SIMULAÇÕES
            try:
                numeroSimulaçoes = int(input('Quantas vezes deseja rodar a simulação?\n'))
            except:
                print("Você digitou alguma coisa inválida, tente novamente!")
                break
            print("O sistema irá demorar alguns minutos, espere por favor!")
            func(criaMatrizC(5000, 5000), 5000, 5000, numeroSimulaçoes)
            # SAIR DA FUNÇÃO
            try:
                decider = int(input('Digite 1 para voltar.\n'))
            except:
                print("Você digitou alguma coisa inválida!")
                break
            if decider == 1:
                break
            else:
                print("Você digitou alguma coisa inválida!")
                break

