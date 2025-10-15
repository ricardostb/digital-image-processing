#===============================================================================
# Bloom: Gaussiano e Box
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

INPUT_IMAGE =  'GT2.BMP'

#===============================================================================

def get_color_threshold(img, threshold):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, img_gray_thresh = cv2.threshold(gray_img, threshold, 1.0, cv2.THRESH_BINARY)
    img_color_thresh = np.copy(img)
    
    img_color_thresh[img_gray_thresh < 1.0] = 0.0

    return img_color_thresh

def bloom_gaussiano(img, img_thresh):
    step1 = cv2.GaussianBlur(img_thresh, (45,45), 0)
    step2 = cv2.GaussianBlur(img_thresh, (105,105), 0)
    step3 = cv2.GaussianBlur(img_thresh, (155,155), 0)
    step4 = cv2.GaussianBlur(img_thresh, (235,235), 0)

    blur = np.multiply(step1 + step2 + step3 + step4, 0.1)

    return img + blur

def bloom_box(img, img_thresh):
    w1 = 15
    step1 = cv2.blur(cv2.blur(cv2.blur(img_thresh, (w1,w1)), (w1,w1)), (w1,w1))
    w2 = 35
    step2 = cv2.blur(cv2.blur(cv2.blur(img_thresh, (w2,w2)), (w2,w2)), (w2,w2))
    w3 = 49
    step3 = cv2.blur(cv2.blur(cv2.blur(img_thresh, (w3,w3)), (w3,w3)), (w3,w3))
    w4 = 65
    step4 = cv2.blur(cv2.blur(cv2.blur(img_thresh, (w4,w4)), (w4,w4)), (w4,w4))

    blur = np.multiply(step1 + step2 + step3 + step4, 0.1)

    return img + blur

#===============================================================================

def main():
    img = cv2.imread(INPUT_IMAGE, cv2.IMREAD_COLOR)
    if img is None:
        print('Erro abrindo a imagem.\n')
        sys.exit()
    img = img.astype (np.float32) / 255

    threshold = 0.57
    if (INPUT_IMAGE == 'Wind Waker GC.bmp'):
        threshold = 0.48
    img_color_thresh = get_color_threshold(img, threshold)

    start = timeit.default_timer()
    img_bloom_gaussiano = bloom_gaussiano(img, img_color_thresh)
    gaussiano_time = timeit.default_timer() - start
    print(f'Gaussiano: {gaussiano_time:.5f}s')

    start = timeit.default_timer()
    img_bloom_box = bloom_box(img, img_color_thresh)
    box_time = timeit.default_timer() - start
    print(f'Box: {box_time:.5f}s')

    cv2.imshow('Original', img)
    cv2.imshow('Gaussiano', img_bloom_gaussiano)
    cv2.imshow('Box', img_bloom_box)
    cv2.waitKey()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()

#===============================================================================