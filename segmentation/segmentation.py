#===============================================================================
# Exemplo: segmentação de uma imagem em escala de cinza.
#-------------------------------------------------------------------------------
# Autor: Bogdan T. Nassu
# Universidade Tecnológica Federal do Paraná
#-------------------------------------------------------------------------------
# Aluno: Ricardo S. Borges
#===============================================================================

import sys
import timeit
import numpy as np
import cv2

#===============================================================================

INPUT_IMAGE =  'arroz.bmp'

# TODO: ajuste estes parâmetros!
NEGATIVO = False
THRESHOLD = 0.80
ALTURA_MIN = 1
LARGURA_MIN = 1
N_PIXELS_MIN = 1

### variaveis globais para identificacao de componentes
t, l, b, r = 0, 0, 0, 0
n_pixels = 0

#===============================================================================

### 0.0 para background e 1.0 para foreground
def binariza (img, threshold):
    return np.where(img < threshold, 0.0, 1.0)

    ''' Binarização simples por limiarização.

Parâmetros: img: imagem de entrada. Se tiver mais que 1 canal, binariza cada
              canal independentemente.
            threshold: limiar.
            
Valor de retorno: versão binarizada da img_in.'''

    # TODO: escreva o código desta função.
    # Dica/desafio: usando a função np.where, dá para fazer a binarização muito
    # rapidamente, e com apenas uma linha de código!

#-------------------------------------------------------------------------------

### preenche um componente a partir de um pixel nao visitado, vizinhanca-4
def flood_fill(img, x0, y0, label):
    global t, l, b, r
    global n_pixels

    n_pixels += 1
    t = min(t, x0)
    l = min(l, y0)
    b = max(b, x0)
    r = max(r, y0)

    img[x0, y0] = label

    if img[x0+1, y0] == -1.0:
        flood_fill(img, x0+1, y0, label)
    if img[x0-1, y0] == -1.0:
        flood_fill(img, x0-1, y0, label)
    if img[x0, y0+1] == -1.0:
        flood_fill(img, x0, y0+1, label)
    if img[x0, y0-1] == -1.0:
        flood_fill(img, x0, y0-1, label)

### rotulagem de componentes
def rotula (img, largura_min, altura_min, n_pixels_min):
    global t, l, b, r
    global n_pixels

    ### seta os pixels de foreground nao visitados como -1.0
    img = np.where(img == 1.0, -1.0, 0.0)
    componentes = []
    label = 0

    ### percorre a imagem procurando por pixels de foreground nao visitados
    for linha in range(img.shape[0]):
        for coluna in range(img.shape[1]):
            t, l = linha, coluna
            b, r = 0, 0
            n_pixels = 0

            if img[linha, coluna] == -1.0:
                label += 1
                flood_fill(img, linha, coluna, label)
                if n_pixels >= n_pixels_min and (r - l) > largura_min and (b - t) > altura_min:
                    componentes.append({"label": label, "n_pixels": n_pixels, "T": t, "L": l, "B": b, "R": r})

    return componentes
    
    '''Rotulagem usando flood fill. Marca os objetos da imagem com os valores
[0.1,0.2,etc].

Parâmetros: img: imagem de entrada E saída.
            largura_min: descarta componentes com largura menor que esta.
            altura_min: descarta componentes com altura menor que esta.
            n_pixels_min: descarta componentes com menos pixels que isso.

Valor de retorno: uma lista, onde cada item é um vetor associativo (dictionary)
com os seguintes campos:

'label': rótulo do componente.
'n_pixels': número de pixels do componente.
'T', 'L', 'B', 'R': coordenadas do retângulo envolvente de um componente conexo,
respectivamente: topo, esquerda, baixo e direita.'''

    # TODO: escreva esta função.
    # Use a abordagem com flood fill recursivo.

#===============================================================================

def main ():
    # Abre a imagem em escala de cinza.
    img = cv2.imread (INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print ('Erro abrindo a imagem.\n')
        sys.exit ()

    # É uma boa prática manter o shape com 3 valores, independente da imagem ser
    # colorida ou não. Também já convertemos para float32.
    img = img.reshape ((img.shape [0], img.shape [1], 1))
    img = img.astype (np.float32) / 255

    # Mantém uma cópia colorida para desenhar a saída.
    img_out = cv2.cvtColor (img, cv2.COLOR_GRAY2BGR)

    # Segmenta a imagem.
    if NEGATIVO:
        img = 1 - img
    img = binariza (img, THRESHOLD)
    cv2.imshow ('01 - binarizada', img)
    cv2.imwrite ('01 - binarizada.png', img*255)

    start_time = timeit.default_timer ()
    componentes = rotula (img, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN)
    n_componentes = len (componentes)
    print ('Tempo: %f' % (timeit.default_timer () - start_time))
    print ('%d componentes detectados.' % n_componentes)

    # Mostra os objetos encontrados.
    for c in componentes:
        cv2.rectangle (img_out, (c ['L'], c ['T']), (c ['R'], c ['B']), (0,0,1))

    cv2.imshow ('02 - out', img_out)
    cv2.imwrite ('02 - out.png', img_out*255)
    cv2.waitKey ()
    cv2.destroyAllWindows ()

if __name__ == '__main__':
    main ()

#===============================================================================
