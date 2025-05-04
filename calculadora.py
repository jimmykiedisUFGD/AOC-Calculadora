import curses
import sys

def menu_principal(stdscr):
    curses.curs_set(1)

    # Exibe o menu principal usando curses e lê a escolha do usuário

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

    # Ecreve o menu na tela
    stdscr.refresh()

    # Lê quais serão os operandos e qual será o operador
    num1, op, num2 = ler_operandos_decimal(stdscr)

    try:
        if op == "+":
            adicionar(num1, num2, quantidade_bits, stdscr)
        elif op == "-":
            subtrair(num1, num2, quantidade_bits, stdscr)
        elif op == "*":
            multiplicar(num1, num2, quantidade_bits, stdscr)
        elif op == "/":
            dividir(num1, num2, quantidade_bits, stdscr)
        else:
            raise ValueError  # Se for qualquer tecla inválida, levanta um erro manualmente

    except ValueError:
        erro = 'Entrada inválida'
        mostrar_erro(erro, stdscr)

def mostrar_erro(erro, linha, stdscr):
    limpar_tela(stdscr)
    stdscr.addstr(linha-1, 0, f"Erro: {erro}")
    stdscr.refresh()
    
    return

def limpar_tela(stdscr):

    # Limpa a tela e exibe o menu principal novamente
    stdscr.clear()
    stdscr.refresh()
    
    return
    
def escolher_bits(stdscr):

    linha = 2
    # Definindo se serão 8, 16, 32 bits
    stdscr.addstr(linha, 3, "8, 16, 32:")
    curses.echo()
    bits = stdscr.getstr(linha, len('8, 16, 32: ')+2, 2).decode("utf-8")
    
    try:
        bits = int(bits)
        if bits not in [8, 16, 32]:
            raise ValueError
    except ValueError:
        erro = 'Número de bits inválido. Escolha entre 8, 16 ou 32:'
        mostrar_erro(erro, linha, stdscr)
        return escolher_bits(stdscr)
    return bits
    # Lê a quantidade de bits do usuário

def ler_operandos_decimal(stdscr):

    linha = 6
    stdscr.addstr(0, 0, "*--**--Calculadora Binária--**--*")

    # Pede dois números decimais e o operador para o usuário e retorna
    stdscr.addstr(linha, 2, "Digite o primeiro número: ")
    curses.echo()
    num1 = stdscr.getstr(linha, len("Digite o primeiro número: ")+2, 20).decode("utf-8")
    #tenho que tratar se o numero cabe na quantidade de bits que foi informado

    stdscr.addstr(linha+1, 2, "Digite o operador (+, -, *, /): ")
    op = stdscr.getstr(linha+1, len("Digite o operador (+, -, *, /): ")+2, 1).decode("utf-8")
    #aqui eu tenho que limitar ao total de 1 operador

    stdscr.addstr(linha+2, 2, "Digite o segundo número: ")
    num2 = stdscr.getstr(linha+2, len("Digite o segundo número: ")+2, 20).decode("utf-8")
    #tenho que tratar se o numero cabe na quantidade de bits que foi informado

    return num1, op, num2

def decimal_para_binario(binario):
    # Converte binário (em lista/vetor) de volta para decimal
    pass

def finalizar(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Encerrando o programa... ")
    stdscr.refresh()

    curses.endwin()  # Encerra o modo curses (importante!)
    sys.exit(0)

def pressione_tecla(stdscr):
    stdscr.addstr(5, 0, "Pressione a tecla Enter para calcular ou ESC para sair.")
    stdscr.refresh()

    tecla = stdscr.getch()

    try:
        if tecla == 13:  # Enter
            menu_principal(stdscr)
        elif tecla == 27:  # ESC
            finalizar(stdscr)
        else:
            raise ValueError  # Se for qualquer tecla inválida, levanta um erro manualmente
    except ValueError:
        erro = 'Tecla inválida'
        mostrar_erro(erro, stdscr)

def adicionar(num1, num2, quantidade_bits, stdscr):

    # converter os números decimais para binários
    bin1, bin2 = decimal_para_binario(num1, num2, quantidade_bits)

    try:
        # decimal:
        ad = float(num1)
        bd = float(num2)
        
        # binário:
        resultado_dec = ad + bd
        resultado_bin = bin1 + bin2 

        # chama a função para imprimir na tela o resultado
        mostrar_resultado(resultado_bin, resultado_dec, stdscr)

    except ValueError:
        erro = 'Entrada inválida'
        mostrar_erro(erro, stdscr)

def subtrair(num1, num2, quantidade_bits, stdscr):
    try:
        a = float(num1)
        b = float(num2)
        result = a - b
        stdscr.addstr(11, 0, f"Resultado: {result}")
    except ValueError:
        erro = 'Entrada inválida'
        mostrar_erro(erro, stdscr)

def multiplicar(num1, num2, quantidade_bits, stdscr):
    # Realiza a multiplicação binária
    try:
        a = float(num1)
        b = float(num2)
        result = a * b
        stdscr.addstr(11, 0, f"Resultado: {result}")
    except ValueError:
        erro = 'Entrada inválida'
        mostrar_erro(erro, stdscr)

def dividir(num1, num2, quantidade_bits, stdscr):
    # Realiza a divisão binária
    try:
        a = float(num1)
        b = float(num2)
        if b != 0:
            result = a / b
            stdscr.addstr(11, 0, f"Resultado: {result}")
        else:
            erro = 'Não pode dividir por zero'
            mostrar_erro(erro, stdscr)
    except ValueError:
        erro = 'Entrada inválida'
        mostrar_erro(erro, stdscr)

def mostrar_resultado(resultado_bin, resultado_dec, stdscr):
    # Exibe o resultado na tela (binário + decimal)

    limpar_tela(stdscr)

    #aqui começamos a exibir a tela de resultador
    stdscr.addstr(0, 0, "Resultados")
    stdscr.addstr(1, 0, "Resultados operação decimal:")
    stdscr.addstr(2, 0, f"{resultado_dec}")

    stdscr.addstr(1, 32, "|Resultados operação binária:")    
    stdscr.addstr(2, 32, f"|{resultado_bin}")

    pressione_tecla(stdscr)

if __name__ == "__main__":
    curses.wrapper(menu_principal)
