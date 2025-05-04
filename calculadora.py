import curses
import sys

def menu_principal(stdscr):
    curses.curs_set(1)

    # Exibe o menu principal usando curses e lê a escolha do usuário

    linha = 0
    stdscr.addstr(linha, 0, "*--**--Calculadora Binária--**--*")
 
    stdscr.addstr(linha+1, 2, "Escolha a quantidade de bits:")
    quantidade_bits, limite = escolher_bits(stdscr)

    limpar_tela(stdscr)
    stdscr.addstr(linha+1, 2, "Operações disponíveis:")
    stdscr.addstr(linha+2, 3, "+ : Adição")
    stdscr.addstr(linha+3, 3, "- : Subtração")
    stdscr.addstr(linha+4, 3, "* : Multiplicação")
    stdscr.addstr(linha+5, 3, "/ : Divisão")

    # Ecreve o menu na tela
    stdscr.refresh()

    # Lê quais serão os operandos e qual será o operador
    num1, op, num2 = ler_operandos_decimal(limite, stdscr)

    bin1, bin2 = converter_em_binário(num1, num2, quantidade_bits)
    # Converte os números decimais para binários

    try:
        if op == "+":
            somar(bin1, bin2, quantidade_bits, stdscr)
        elif op == "-":
            subtrair(bin1, bin2, quantidade_bits, stdscr)
        elif op == "*":
            multiplicar(bin1, bin2, quantidade_bits, stdscr)
        elif op == "/":
            dividir(bin1, bin2, quantidade_bits, stdscr)
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
    
    match bits:
        case '8':
            quantidade_bits = 8
            limite = 255
        case '16':
            quantidade_bits = 16
            limite = 65535
        case '32':
            quantidade_bits = 32
            limite = 4294967295
        case _:
            erro = 'Escolha uma quantidade de bits válida (8, 16 ou 32):'
            mostrar_erro(erro, linha, stdscr)
            return escolher_bits(stdscr)

    return quantidade_bits, limite

def ler_operandos_decimal(limite, stdscr):

    linha = 6
    stdscr.addstr(0, 0, "*--**--Calculadora Binária--**--*")

    # Pede dois números decimais e o operador para o usuário e retorna
    stdscr.addstr(linha, 2, f"Digite o primeiro número até {limite}: ")
    curses.echo()
    num1 = stdscr.getstr(linha, len(f"Digite o primeiro número até {limite}: ")+2, 20).decode("utf-8")

    stdscr.addstr(linha+1, 2, "Digite o operador (+, -, *, /): ")
    op = stdscr.getstr(linha+1, len("Digite o operador (+, -, *, /): ")+2, 1).decode("utf-8")

    stdscr.addstr(linha+2, 2, f"Digite o segundo número até {limite}: ")
    num2 = stdscr.getstr(linha+2, len(f"Digite o segundo número até {limite}: ")+2, 20).decode("utf-8")

    return num1, op, num2

def converter_em_binário (num1, num2, quantidade_bits, stdscr):
    if quantidade_bits == 8:
        bin1 = format(int(num1), '08b')     # Converte para binário com 8 bits colocando 0 suficiente à esquerda
        bin2 = format(int(num2), '08b')
    elif quantidade_bits == 16:
        bin1 = format(int(num1), '016b')    # Converte para binário com 16 bits colocando 0 suficiente à esquerda
        bin2 = format(int(num2), '016b')
    elif quantidade_bits == 32:
        bin1 = format(int(num1), '032b')    # Converte para binário com 32 bits colocando 0 suficiente à esquerda
        bin2 = format(int(num2), '032b')
    else:
        erro = 'Escolha uma quantidade de bits válida (8, 16 ou 32):'
        converter_em_binário (num1, num2, quantidade_bits)
        return escolher_bits(stdscr)
    return bin1, bin2

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

def somar(bin1, bin2, quantidade_bits, stdscr):
    pass

def subtrair(bin1, bin2, quantidade_bits, stdscr):
    pass

def multiplicar(bin1, bin2, quantidade_bits, stdscr):
    pass

def dividir(bin1, bin2, quantidade_bits, stdscr):
    pass

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
