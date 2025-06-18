import curses
import sys
import time

def menu_principal(stdscr):
    # inicia dizendo que o cursor será invisível
    curses.curs_set(1)
    # organizei através de uma variável incrementativa
    linha = 0
    stdscr.addstr(linha, 0, "*--**--Calculadora Binária--**--*")
 
    stdscr.addstr(linha+1, 2, "Escolha a quantidade de bits:")
    quantidade_bits = escolher_bits(stdscr)

    limpar_tela(stdscr)
    stdscr.addstr(linha+1, 2, "Operações disponíveis:")
    stdscr.addstr(linha+2, 3, "+ : Adição")
    stdscr.addstr(linha+3, 3, "- : Subtração")
    stdscr.addstr(linha+4, 3, "* : Multiplicação")
    stdscr.addstr(linha+5, 3, "/ : Divisão")

    stdscr.refresh()

    # obtendo o valor do usuário
    num1, op, num2 = ler_operandos_decimal(quantidade_bits, stdscr)
    # convertendo o valor para binário.
    bin1, bin2 = converter_em_binário(num1, num2, quantidade_bits)

    try:
        if op == "+":
            resultado = somar_subtrair(bin1, bin2)
            mostrar_resultado(bin1, bin2, resultado[-quantidade_bits:], stdscr)
        elif op == "-":
            # ja busco criar o segundo binário negado pra mandar para a função de somar subtrair
            bin2_negado = somar_subtrair(inverter_bits(bin2), '0' * (quantidade_bits - 1) + '1')
            resultado = somar_subtrair(bin1, bin2_negado)
            mostrar_resultado(bin1, bin2, resultado[-quantidade_bits:], stdscr)
        elif op == "*":
            # chama a função de multiplicar e ela retorna o valor e o bool de um caso de overflow
            resultado, overflow = multiplicar(bin1, bin2)
            mostrar_resultado(bin1, bin2, resultado[-quantidade_bits:], stdscr, resto=None, overflow=overflow)
        elif op == "/":
            # passa os valores absolutos para a função dividir, retona o resto e o cociente
            quociente, resto = dividir(
                format(abs(num1), f'0{quantidade_bits}b'),
                format(abs(num2), f'0{quantidade_bits}b')
            )

            # ajusta o sinal do quociente se os sinais forem diferentes
            if (num1 < 0) ^ (num2 < 0):
                quociente = inverter_bits(quociente)
                quociente = somar_subtrair(quociente, '0' * (quantidade_bits - 1) + '1')
            
            mostrar_resultado(bin1, bin2, quociente[-quantidade_bits:], stdscr, resto)
        else:
            raise ValueError
        
    except ValueError:
        erro = 'Entrada inválida'
        mostrar_erro(erro, stdscr)
        
def mostrar_erro(erro, stdscr, linha=0):
    limpar_tela(stdscr)
    # recebe o erro por paramêtro, avisa o usuário, espera 2 seundos e retorna para onde foi chamado
    stdscr.addstr(linha-1, 0, f"Erro: {erro}")
    stdscr.refresh()
    time.sleep(2)
    return

def limpar_tela(stdscr):
    # função simples, pra mater melhor organizado as coisas
    stdscr.clear()
    stdscr.refresh()
    return

def escolher_bits(stdscr):
    #definindo o limite máximo de bits, aqui eu trato o primeiro passo do overflow
    linha = 2
    stdscr.addstr(linha, 3, "8, 16, 32:")
    curses.echo()
    bits = stdscr.getstr(linha, len('8, 16, 32: ')+2, 2).decode("utf-8")

    match bits:
        case '8': quantidade_bits = 8
        case '16': quantidade_bits = 16
        case '32': quantidade_bits = 32
        case _: 
            erro = 'Escolha uma quantidade de bits válida dentre as opções (8, 16 ou 32):'
            mostrar_erro(erro, stdscr, linha)
            return escolher_bits(stdscr)

    return quantidade_bits

def sinal_magnitude_para_complemento2(binario):
    # criando um função separada para controlar o sinal magnitude
    if binario[0] == '0':
        return binario
    invertido = inverter_bits(binario)
    return somar_subtrair(invertido, '0' * (len(binario) - 1) + '1')

def inverter_bits(binario):
    # aqui temos o complemento de um
    return ''.join('1' if b == '0' else '0' for b in binario)

def ler_operandos_decimal(quantidade_bits, stdscr):
    linha = 6
    stdscr.addstr(0, 0, "*--**--Calculadora Binária--**--*")

    # definindo os limites para o numero, não pode exeder o limite de representáveis 2^quantidade de bits
    limite_inferior = -(2 ** (quantidade_bits - 1))
    limite_superior = (2 ** (quantidade_bits - 1)) - 1

    try:
        # vamos receber os valores limitano o numero máximo que e quantidade de bits pode representar
        stdscr.addstr(linha, 2, f"Digite o primeiro número entre {limite_inferior} e {limite_superior}: ")
        curses.echo()
        num1 = int(stdscr.getstr(linha, len(f"Digite o primeiro número entre {limite_inferior} e {limite_superior}: ") + 2, 20).decode("utf-8"))
        if not (limite_inferior <= num1 <= limite_superior): raise ValueError

        stdscr.addstr(linha + 1, 2, "Digite o operador (+, -, *, /): ")
        op = stdscr.getstr(linha + 1, len("Digite o operador (+, -, *, /): ") + 2, 1).decode("utf-8")

        stdscr.addstr(linha + 2, 2, f"Digite o segundo número entre {limite_inferior} e {limite_superior}: ")
        num2 = int(stdscr.getstr(linha + 2, len(f"Digite o segundo número entre {limite_inferior} e {limite_superior}: ") + 2, 20).decode("utf-8"))
        if not (limite_inferior <= num2 <= limite_superior): raise ValueError

    except ValueError:
        # se não estiver no intervalo, então ele chama a tela de erro e recomeça.
        erro = 'Valor fora do intervalo ou inválido, tente novamente:'
        mostrar_erro(erro, stdscr, linha)
        return ler_operandos_decimal(quantidade_bits, stdscr)

    return num1, op, num2

def converter_em_binário(num1, num2, quantidade_bits):
    # vamos fazer uma chamada recursiva para obter o complemento de dois se for maior ou igual a zero
    def para_binario_complemento_dois(n, bits):
        if n >= 0:
            return format(n, f'0{bits}b')
        else:
            return format((1 << bits) + n, f'0{bits}b')

    bin1 = para_binario_complemento_dois(num1, quantidade_bits)
    bin2 = para_binario_complemento_dois(num2, quantidade_bits)

    return bin1, bin2

def finalizar(stdscr):
    # finalizar interamente todos os recursos que foram iniciados
    stdscr.clear()
    stdscr.addstr(0, 0, "Encerrando o programa... ")
    stdscr.refresh()
    curses.endwin()
    sys.exit(0)

def pressione_tecla(stdscr):
    # auxiliar de menu, serve para quando no final do calculo vc poder escolher se quer fazer outro calculo ou não
    stdscr.addstr(5, 0, "Pressione a tecla Enter para calcular ou ESC para sair.")
    stdscr.refresh()

    tecla = stdscr.getch()

    try:
        if tecla in (10, 13):     #10 e o 13 é o enter (que Deus tenha piedade)
            limpar_tela(stdscr)
            return menu_principal(stdscr)
        elif tecla == 27:   #27 é o esc
            finalizar(stdscr)
        else:
            raise ValueError
    except ValueError:
        #se for digitada uma tecla não esperada, ele mostra o erro
        erro = 'Tecla inválida'
        mostrar_erro(erro, stdscr)
        return pressione_tecla(stdscr)

def somar_subtrair(bin1, bin2):
    # o resultado é incrementativo, começa vazio e vai sendo adicionado o valor do laço bit-a-bit
    resultado = ''
    carry = 0
    for i in range(len(bin1) - 1, -1, -1):
        total = carry
        total += bin1[i] == '1'
        total += bin2[i] == '1'
        resultado = ('1' if total % 2 else '0') + resultado
        carry = 1 if total > 1 else 0
    return resultado[-len(bin1):]

def multiplicar(bin1, bin2):
    # será usado o algoritmo de multiplicação de booth, o que foi ensinado na aula 
    n = len(bin1)
    A = '0' * n
    Q = bin2
    M = bin1
    Q_1 = '0'

    for _ in range(n):
        if Q[-1] == '1' and Q_1 == '0':
            A = somar_subtrair(A, inverter_bits(M))
            A = somar_subtrair(A, '0' * (n - 1) + '1')
        elif Q[-1] == '0' and Q_1 == '1':
            A = somar_subtrair(A, M)

        combinado = A + Q + Q_1
        combinado = combinado[0] + combinado[:-1]

        A = combinado[:n]
        Q = combinado[n:2*n]
        Q_1 = combinado[-1]

    resultado_completo = A + Q  # 2n bits, concatenação 
    resultado_final = resultado_completo[-n:]  # n bits (para exibir)

    # verificação de overflow correta
    valor_inteiro = int(resultado_completo, 2)
    if resultado_completo[0] == '1':
        valor_inteiro -= (1 << (2 * n))

    minimo = -(1 << (n - 1))
    maximo = (1 << (n - 1)) - 1

    overflow_detectado = not (minimo <= valor_inteiro <= maximo)

    return resultado_final, overflow_detectado

def dividir(smag1, smag2):
    n = len(smag1)

    # converter binários em inteiros
    dividend = int(smag1, 2)
    divisor = int(smag2, 2)

    if divisor == 0:
        raise ValueError("Divisão por zero não é permitida.")

    quotient = dividend // divisor
    remainder = dividend % divisor

    # converter de volta para binário com n bits
    quociente_bin = format(quotient, f'0{n}b')
    resto_bin = format(remainder, f'0{n}b')

    return quociente_bin, resto_bin

def shift_esquerda(A, Q):
    combinado = A + Q
    combinado = combinado[1:] + '0'  # desloca tudo à esquerda
    novo_A = combinado[:len(A)]
    novo_Q = combinado[len(A):]
    return novo_A, novo_Q

def mostrar_resultado(bin1, bin2, resultado, stdscr, resto=None, overflow=False):
    limpar_tela(stdscr)
    stdscr.addstr(8, 0, f"Primeiro número em binário: {bin1}") #debuger para somar manualmente se necessário
    stdscr.addstr(9, 0, f"Segundo número em binário:  {bin2}")
    stdscr.addstr(10, 0, f"Resultado em binário:      {resultado}") #resultado esperado
    if resto is not None:
        stdscr.addstr(11, 0, f"O resto é:                {resto}") # em caso de resto
    if overflow:
        stdscr.addstr(12, 0, "!!! OVERFLOW DETECTADO !!!") # em caso de overfloiw
    stdscr.refresh()
    pressione_tecla(stdscr)

if __name__ == "__main__":
    try:
        curses.wrapper(menu_principal)
    except Exception as e:
        print("Erro ao iniciar a interface curses:", e)
        sys.exit(1)
