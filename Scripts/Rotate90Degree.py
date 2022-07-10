# rotate a square size image 90 degree clockwise

image3x3 = [[1,2,3],
            [4,5,6],
            [7,8,9]]

image4x4 = [[1,2,3,4],
            [5,6,7,8],
            [9,10,11,12],
            [13,14,15,16]]

def solution1(img): ##brute force, need extra space
    length = len(img)
    #Building new empty list with same size list entered
    newimage = []
    for i in range(length):
        row = []
        for j in range(length):
            row.append(int(0))
        newimage.append(row)

    for i in range(length):
        for j in range(length):
            newimage[j][length-i-1] = (img[i][j])
            #print(newimage)
            #newimage.[]  = image[i][j]

    for i in newimage:
        print(i)

#print(solution1(image3x3))
#print(solution1(image4x4))

def solution2step_1(img):
    length = len(img)
    for i in range(length):
        for j in range(i,length):
            temp = img[i][j]
            img[i][j] = img[j][i]
            img[j][i] = temp
    return img



def solution2step_2(img):
    length = len(img)
    for i in range(length):
        for j in range(length//2):

            temp = img[i][j]
            img[i][j] = img[i][length-j-1]
            img[i][length-j-1] = temp
    for i in img:
        print(i)


print(solution2step_2(solution2step_1(image3x3)))
print(solution2step_2(solution2step_1(image4x4)))
