#===============================================================================
# Contagem de arroz
#-------------------------------------------------------------------------------
# Universidade Tecnológica Federal do Paraná
#-------------------------------------------------------------------------------
# Aluno: Ricardo S. Borges
#===============================================================================

import sys
import numpy as np
import cv2

#===============================================================================

INPUT_IMAGE =  '60.bmp'

#===============================================================================

# implementação de rotulagem do trabalho 1
def flood_fill(img, x0, y0, label):
    global t, l, b, r
    global n_pixels

    if x0 < 0 or x0 >= img.shape[0] or y0 < 0 or y0 >= img.shape[1]:
        return
    
    if img[x0, y0] != -1.0:
        return

    stack = [(x0, y0)]
    
    while stack:
        x, y = stack.pop()
        
        if x < 0 or x >= img.shape[0] or y < 0 or y >= img.shape[1]:
            continue
            
        if img[x, y] != -1.0:
            continue
            
        n_pixels += 1
        t = min(t, x)
        l = min(l, y)
        b = max(b, x)
        r = max(r, y)
        
        img[x, y] = label
        
        stack.append((x+1, y))
        stack.append((x-1, y))
        stack.append((x, y+1))
        stack.append((x, y-1))

def rotula (img, largura_min, altura_min, n_pixels_min):
    global t, l, b, r
    global n_pixels

    img = np.where(img == 1.0, -1.0, 0.0)
    componentes = []
    label = 0

    for linha in range(img.shape[0]):
        for coluna in range(img.shape[1]):
            t, l = linha, coluna
            b, r = 0, 0
            n_pixels = 0

            if img[linha, coluna] == -1.0:
                label += 1
                flood_fill(img, linha, coluna, label)
                if n_pixels >= n_pixels_min and (r - l) > largura_min and (b - t) > altura_min:
                    componentes.append(n_pixels)

    return componentes

#-------------------------------------------------------------------------------

# procura a moda das categorias de tamanho de arroz,
# verifica se há múltiplos e calcula tamanho médio
def calcula_tamanho_arroz(componentes, intervalo=25):
    categorias = {}
    
    for valor in componentes:
        categoria = (valor // intervalo) * intervalo
        if categoria not in categorias:
            categorias[categoria] = 0
        categorias[categoria] += 1

    categoria_max = max(categorias, key=categorias.get)
    
    print('\nDistribuição por categorias:')
    print(categorias, '\n')

    threshold = categorias[categoria_max] * 0.3

    for cat in categorias.keys():
        if cat < categoria_max and categorias[cat] >= threshold:
            ratio = categoria_max / cat if cat > 0 else 0
            if 1.5 <= ratio <= 3.5:
                print(f'Categoria {categoria_max} pode ser múltiplo de {cat}\n')
                categoria_max = cat
                break

    componentes_categoria = [c for c in componentes if categoria_max - intervalo < c < categoria_max + (2 * intervalo)]
    tamanho_medio = sum(componentes_categoria) / len(componentes_categoria)
    
    return tamanho_medio

# caso seja consideravelmente maior que tamanho médio, divide
def calcula_numero_arroz(componentes, tamanho_medio):
    n_arroz = 0
    for c in componentes:
        if c > tamanho_medio * 1.3:
            n_arroz += round(c / tamanho_medio)
        else:
            n_arroz += 1
    return n_arroz

#===============================================================================

def main():
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()

    # processamento para separar background e foreground
    norm = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    blur = cv2.GaussianBlur(norm, (49, 49), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 19, 0)
    erode = cv2.erode(thresh, None, iterations=3)
    dilate = cv2.dilate(erode, None, iterations=2)

    # rotulagem e ordenação dos componentes
    img_float = dilate.astype(np.float32) / 255.0
    componentes = rotula(img_float, 3, 3, 9)
    componentes.sort()

    # cálculo do tamanho médio e estimativa de quantidade de arroz
    tamanho_medio = int(calcula_tamanho_arroz(componentes))
    n_arroz = calcula_numero_arroz(componentes, tamanho_medio)

    print(f'Tamanho médio estimado: {tamanho_medio}\n')
    print(f'Número estimado de arroz: {n_arroz}\n')

    cv2.imshow('Original', img)
    cv2.imshow('Blur', blur)
    cv2.imshow('Thresh', thresh)
    cv2.imshow('Erode', erode)
    cv2.imshow('Dilate', dilate)

    cv2.waitKey()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()

#===============================================================================