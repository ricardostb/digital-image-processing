#===============================================================================
# Blur com algoritmos: ingênuo, separável e com imagem integral.
#-------------------------------------------------------------------------------
# Universidade Tecnológica Federal do Paraná
#-------------------------------------------------------------------------------
# Aluno: Ricardo S. Borges
#===============================================================================

import sys
import timeit
import numpy as np
import cv2

#===============================================================================

INPUT_IMAGE =  'imagem.bmp'
WINDOW_SIZE = 9

#===============================================================================

# para cada pixel, soma todos os pixels do kernel e faz a média
def ingenuo (img, w):
    out = np.copy(img)

    for linha in range(w // 2, img.shape[0] - (w // 2)):
        for coluna in range(w // 2, img.shape[1] - (w // 2)):
            for canal in range(img.shape[2]):
                soma = 0

                for linha_w in range(linha - (w // 2), linha + (w // 2) + 1):
                    for coluna_w in range(coluna - (w // 2), coluna + (w // 2) + 1):
                        soma += img[linha_w, coluna_w, canal]

                out[linha, coluna, canal] = soma / (w * w)

    return out

#-------------------------------------------------------------------------------

# borra a imagem em um sentido depois em outro
def separavel(img, w):
    out = np.copy(img)

    for linha in range(w // 2, img.shape[0] - (w // 2)):
        for coluna in range(w // 2, img.shape[1] - (w // 2)):
            for canal in range(img.shape[2]):
                soma = 0
                for coluna_w in range(coluna - (w // 2), coluna + (w // 2) + 1):
                    soma += out[linha, coluna_w, canal]
                out[linha, coluna, canal] = soma / w

    for coluna in range(w // 2, img.shape[1] - (w // 2)):
        for linha in range(w // 2, img.shape[0] - (w // 2)):
            for canal in range(img.shape[2]):
                soma = 0
                for linha_w in range(linha - (w // 2), linha + (w // 2) + 1):
                    soma += out[linha_w, coluna, canal]
                out[linha, coluna, canal] = soma / w

    return out

#-------------------------------------------------------------------------------

# cria uma imagem integral e borra a imagem utilizando-a
def integral(img, w):
    integral = np.copy(img)
    out = np.copy(img)

    # cria imagem integral
    for canal in range(img.shape[2]):
        for coluna in range(1, img.shape[1]):
            integral[0, coluna, canal] = integral[0, coluna-1, canal] + img[0, coluna, canal]

        for linha in range(1, img.shape[0]):
            integral[linha, 0, canal] = integral[linha-1, 0, canal] + img[linha, 0, canal]

        for linha in range(1, img.shape[0]):
            for coluna in range(1, img.shape[1]):
                integral[linha, coluna, canal] = (img[linha, coluna, canal] + integral[linha-1, coluna, canal] + 
                                             integral[linha, coluna-1, canal] - integral[linha-1, coluna-1, canal])

    # borra a imagem
    for linha in range(img.shape[0]):
        cima = max(linha - (w // 2), 0)
        baixo = min(linha + (w // 2), img.shape[0] - 1)
        for coluna in range(img.shape[1]):
            esquerda = max(coluna - (w // 2), 0)
            direita = min(coluna + (w // 2), img.shape[1] - 1)
            area = (baixo - cima + 1) * (direita - esquerda + 1)
            for canal in range(img.shape[2]):
                db = integral[baixo, direita, canal]
                eb = integral[baixo, esquerda - 1, canal] if esquerda > 0 else 0
                dc = integral[cima - 1, direita, canal] if cima > 0 else 0
                ec = integral[cima - 1, esquerda - 1, canal] if cima > 0 and esquerda > 0 else 0
                
                soma = db - eb - dc + ec
                out[linha, coluna, canal] = soma / area

    return out

#===============================================================================

# le a imagem, chama as funcoes de blur e calcula seus tempos de execucao
def main():
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()
    img = img.astype(np.float32) / 255

    start = timeit.default_timer()
    img_ing = ingenuo(img, WINDOW_SIZE)
    ingenuo_time = timeit.default_timer() - start

    start = timeit.default_timer()
    img_sep = separavel(img, WINDOW_SIZE)
    separavel_time = timeit.default_timer() - start

    start = timeit.default_timer()
    img_int = integral(img, WINDOW_SIZE)
    integral_time = timeit.default_timer() - start

    print(f"Tempos: Ingênuo - {ingenuo_time}, Separável - {separavel_time}, Integral - {integral_time}")

    cv2.imshow('Ingenuo', img_ing)
    cv2.imshow('Separavel', img_sep)
    cv2.imshow('Integral', img_int)

    cv2.waitKey()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()

#===============================================================================