from PIL import Image
import numpy as np
from sympy import primerange


# create list of binary ASCII values which we want to hide

# method to create list of letters of message
def dataList(message):
    newDataList = []

    for i in message:
        newDataList.append(format(ord(i), '08b'))
    return newDataList


# method to create list of pixels of the picture
def pixelArray(image):
    imageData = image.getdata()
    return np.array(list(imageData))


# method to hide message into picture
def encode(src, fileName, dest):
    img = Image.open(src, 'r')
    width, height = img.size
    totalPixels = len(pixelArray(img))

    # append end string to know, where the message ends when decoding
    file1 = open(fileName, "a")
    file1.write("#$$#")
    file1.close()

    # convert message from type string to type char
    with open(fileName) as f:
        message = []
        for line in f.readlines():
            for char in line:
                message.append(char)


    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    messLength = len(dataList(message))
    print('velkost skryvanej spravy: ' + str(messLength) + ' znakov')
    print('celkovo pixelov ' + str(totalPixels))
    bMessageList = ''.join(dataList(message))
    reqComponents = len(bMessageList)
    pixArray = pixelArray(img)
    primeList = list(primerange(0, totalPixels))
    print('maximum characters we can encode is ' + str(len(primeList) * 3 // 8))

    '''if reqComponents > len(primeList) * 3 // 8:
        raise Exception('Message is larger than image ')'''

    if reqComponents > len(primeList) * 3 // 8:
        print('You made an invalid move')
        exit()

    else:
        index = 0
        for pixel in primeList:
            for component in range(0, 3):
                if index < reqComponents:
                    if bMessageList[index] == '0' and pixArray[pixel][component] % 2 != 0:
                        pixArray[pixel][component] -= 1

                    elif bMessageList[index] == '1' and pixArray[pixel][component] % 2 == 0:
                        # if pixel[component] != 0:
                        pixArray[pixel][component] += 1

                index += 1

    pixList = pixArray.reshape(height, width, n)

    # print(pixList, n)

    img = Image.fromarray(pixList.astype('uint8'), img.mode)

    img.save(dest)
    print("Image Encoded Successfully")
    # print(pixArray[0][0])
    return


def decode(src):
    img = Image.open(src, 'r')
    encPixArray = pixelArray(img)
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    # print(encPixArray)
    encTotalPixels = len(pixelArray(img))
    primeList = list(primerange(0, encTotalPixels))
    # print(primeList)

    letters = ''
    array = []
    index = 0
    for pixel in primeList:
        for component in range(0, 3):
            if encPixArray[pixel][component] % 2 != 0:
                letters += '1'
            else:
                letters += '0'
            index += 1
            if index == 8:
                index = 0
                array.append(chr(int(letters, 2)))
                letters = ''

    message = ""
    for i in range(len(array)):
        if message[-4:] == "#$$#":
            break
        else:
            message += array[i]
            # print(message)
    if "#$$#" in message:
        print("Hidden Message:", message[:-4])
    else:
        print("No Hidden Message Found")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run = True
    while run:
        print('\nWelcome to image Steganography !')
        print()
        print('To Encode message type: encode\n'
              'To Decode message type: encode\n' 
              'To Exit process type: exit')
        print('Enter operation name [encode/decode/exit]:')
        x = input()
        if x == 'encode':
            f = open("message.txt", "w")
            print('Write a message to hide')

            f.write(input())
            f.close()
            encode('original.png', 'message.txt', 'encoded.png')

        elif x == 'decode':
            decode('encoded.png')

        elif x == 'exit':
            run = False

        elif x:
            print('Please try again')
