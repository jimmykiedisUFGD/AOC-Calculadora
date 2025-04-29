import curses

def menu_principal(stdscr):

    # Exibe o menu principal usando curses e lê a escolha do usuário
    curses.curs_set(1)
    stdscr.clear()
    stdscr.refresh()

    stdscr.addstr(0, 0, "Calculadora Binária")
    stdscr.addstr(1, 0, "Operações disponíveis:")
    stdscr.addstr(2, 2, "Escolha a quantidade de bits:")
    stdscr.addstr(3, 2, "+ : Adição")
    stdscr.addstr(4, 2, "- : Subtração")
    stdscr.addstr(5, 2, "* : Multiplicação")
    stdscr.addstr(6, 2, "/ : Divisão")

    quantidade_bits = escolher_bits(stdscr)

    num1, op, num2 = ler_operandos_decimal(stdscr)

    try:
        result = ""

        if op == "+":
            adicionar(num1, num2, quantidade_bits, stdscr)
        elif op == "-":
            subtrair(num1, num2, quantidade_bits, stdscr)
        elif op == "*":
            multiplicar(num1, num2, quantidade_bits, stdscr)
        elif op == "/":
            dividir(num1, num2, quantidade_bits, stdscr)
        else:
            result = "Operador inválido"

        stdscr.addstr(11, 0, f"Resultado: {result}")
    except ValueError:
        stdscr.addstr(11, 0, "Erro: Entrada inválida.")

    stdscr.addstr(13, 0, "Pressione qualquer tecla para sair.")
    stdscr.getch()

def limpar_tela(stdscr):

    # Limpa a tela e exibe o menu principal novamente
    stdscr.clear()
    stdscr.refresh()
    menu_principal(stdscr)
    
def escolher_bits(stdscr):

    # Definindo se serão 8, 16, 32 bits
    stdscr.addstr(7, 2, "8, 16, 32:")
    curses.echo()
    bits = stdscr.getstr(7, 27, 20).decode("utf-8")
    
    return bits
    # Lê a quantidade de bits do usuário

def ler_operandos_decimal(stdscr):

    # Pede dois números decimais para o usuário e retorna
    stdscr.addstr(7, 0, "Digite o primeiro número: ")
    curses.echo()
    num1 = stdscr.getstr(7, 27, 20).decode("utf-8")
    #tenho que tratar se o numero cabe na quantidade de bits que foi informado

    stdscr.addstr(8, 0, "Digite o operador (+, -, *, /): ")
    op = stdscr.getstr(8, 35, 1).decode("utf-8")
    #aqui eu tenho que limitar ao total de 1 operador

    stdscr.addstr(9, 0, "Digite o segundo número: ")
    num2 = stdscr.getstr(9, 27, 20).decode("utf-8")
    #tenho que tratar se o numero cabe na quantidade de bits que foi informado

    return num1, op, num2

def decimal_para_binario(num1, num2, quantidade_bits):
    # Converte número decimal para binário em complemento de 2
    pass

def binario_para_decimal(binario):
    # Converte binário (em lista/vetor) de volta para decimal
    pass

def mostrar_erro(erro, stdscr):
    stdscr.addstr(11, 0, f"Erro: {erro}")
    stdscr.addstr(10, 0, "Pressione qualquer tecla para calcular.")

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
        mostrar_erro("Entrada inválida.", stdscr)

def subtrair(num1, num2, quantidade_bits, stdscr):
    try:
        a = float(num1)
        b = float(num2)
        result = a - b
        stdscr.addstr(11, 0, f"Resultado: {result}")
    except ValueError:
        stdscr.addstr(11, 0, "Erro: Entrada inválida.")
    stdscr.addstr(10, 0, "Pressione qualquer tecla para calcular.")

def multiplicar(num1, num2, quantidade_bits, stdscr):
    # Realiza a multiplicação binária
    try:
        a = float(num1)
        b = float(num2)
        result = a * b
        stdscr.addstr(11, 0, f"Resultado: {result}")
    except ValueError:
        stdscr.addstr(11, 0, "Erro: Entrada inválida.")
    stdscr.addstr(10, 0, "Pressione qualquer tecla para calcular.")

def dividir(num1, num2, quantidade_bits, stdscr):
    # Realiza a divisão binária
    try:
        a = float(num1)
        b = float(num2)
        if b != 0:
            result = a / b
            stdscr.addstr(11, 0, f"Resultado: {result}")
        else:
            stdscr.addstr(11, 0, "Erro: divisão por zero")
    except ValueError:
        stdscr.addstr(11, 0, "Erro: Entrada inválida.")
    stdscr.addstr(10, 0, "Pressione qualquer tecla para calcular.")

def mostrar_resultado(resultado_bin, resultado_dec, stdscr):
    # Exibe o resultado na tela (binário + decimal)
    stdscr.addstr(11, 0, f"Resultado em binário: {resultado_bin}")
    stdscr.addstr(12, 0, f"Resultado em decimal: {resultado_dec}")
    stdscr.addstr(10, 0, "Pressione qualquer tecla para calcular.")

if __name__ == "__main__":
    curses.wrapper(menu_principal)
