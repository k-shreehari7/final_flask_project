from datetime import datetime
from pydoc import plainpager
from flask import Flask,render_template, request
from flask import request
from flask import redirect

import os
from PIL import Image 


from sqlalchemy import false
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///crypt.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False



class Crypt():
    def __repr__(self)->str:
        return f"{self.sno}-{self.plain}"


app.config["IMAGE_UPLOADS"]="/home/hari/final_flask_project/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"]=["PNG","GIF"]
def allowed_image(filename):
    if not '.' in filename:
        return false
    ext=filename.rsplit('.',1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def encode_enc(newimg,data):
    print('INSIDE ENCODE ENC')
    w=newimg.size[0]
    print("w=" + str(w))
    (x,y)=(0,0)
    for pixel in modPix(newimg.getdata(),data):
        newimg.putpixel((x,y),pixel)
        if(x==w-1):
            x=0
            y+=1
        else:
            x+=1        

def genData(data):
 
        # list of binary codes
        # of given data
        newd = []
 
        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd

def modPix(pix, data):
 
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
 
    for i in range(lendata):
 
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]
 
        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
 
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1
 
        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
 
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
 
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def decode(filename):



    path='/home/hari/final_flask_project/static/img/uploads'
    image=os.path.join(path,filename)
    imj= Image.open(image, 'r')

 
    data = ''
    imgdata = iter(imj.getdata())
 
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
 
        # string of binary data
        binstr = ''
 
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
 
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

#DES practice
def char2hex(s):
	temp=""
	for c in s:
		temp += hex(ord(c))[2:]
#		print(temp)
	return temp
	
  #return temp
 
def hex2bin(s):
	mp = {'0' : "0000",
		'1' : "0001",
		'2' : "0010",
		'3' : "0011",
		'4' : "0100",
		'5' : "0101",
		'6' : "0110",
		'7' : "0111",
		'8' : "1000",
		'9' : "1001",
		'a' : "1010",
		'b' : "1011",
		'c' : "1100",
		'd' : "1101",
		'e' : "1110",
		'f' : "1111" }
	bin = ""
	for i in range(len(s)):
		bin = bin + mp[s[i]]
	return bin


def bin2hex(s):
    mp = {"0000" : '0',
          "0001" : '1',
          "0010" : '2',
          "0011" : '3',
          "0100" : '4',
          "0101" : '5',
          "0110" : '6',
          "0111" : '7',
          "1000" : '8',
          "1001" : '9',
          "1010" : 'a',
          "1011" : 'b',
          "1100" : 'c',
          "1101" : 'd',
          "1110" : 'e',
          "1111" : 'f' }
    hex = ""
    for i in range(0,len(s),4):
        ch = ""
        ch = ch + s[i]
        ch = ch + s[i + 1]
        ch = ch + s[i + 2]
        ch = ch + s[i + 3]
        hex = hex + mp[ch]
         
    return hex

def xor(a, b):
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans = ans + "0"
        else:
            ans = ans + "1"
    return ans

def permute(key , keyp , len):
	perm = ""
	for i in range(0 , len):
		perm = perm + key[keyp[i]-1]
	return perm

def shift_left(k , nth_shifts):
	s = ""
	for i in range(nth_shifts):
		for j in range(1,len(k)):
			s = s + k[j]
		s = s + k[0]
		k = s
		s = ""
	return k 



def bin2dec(binary):
       
    binary1 = binary
    decimal, i, n = 0, 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal
 
# Decimal to binary conversion
def dec2bin(num):
    res = bin(num).replace("0b", "")
    if(len(res)%4 != 0):
        div = len(res) / 4
        div = int(div)
        counter =(4 * (div + 1)) - len(res)
        for i in range(0, counter):
            res = '0' + res
    return res


keyp = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30,  22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4 ]


shift_table = [1, 1, 2, 2,
                2, 2, 2, 2,
                1, 2, 2, 2,
                2, 2, 2, 1 ]


key_comp = [14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32 ]

initial_perm =[39, 7, 7, 32, 16, 45, 88, 126,
              89, 122, 12, 63, 57, 23, 2, 73, 
							114, 43, 104, 107, 44, 104, 9, 49,
							116, 58, 3, 6, 96, 66, 71, 54, 
							75, 85, 67, 57, 44, 64, 60, 95,
							10, 116, 8, 29, 122, 102, 65, 97,
							61, 16, 31, 106, 14, 125, 76, 84,
							47, 65, 8, 9, 116, 86, 21, 88, 
							50, 73, 119, 15, 75, 87, 37, 47, 
							76, 94, 29, 29, 114, 59, 3, 120, 
							101, 33, 21, 72, 92, 77, 57, 25,
							75, 122, 59, 54, 118, 75, 55, 82, 
							63, 52, 96, 109, 91, 73, 97, 85,
							26, 74, 83, 20, 93, 90, 8, 124,
							109, 92, 53, 23, 66, 12, 109, 6,
              41, 115, 42, 91, 70, 17, 61, 30]


final_perm = [117, 63, 78, 123, 55, 30, 22, 64, 
              97, 6, 113, 75, 47, 23, 79, 113, 
							22, 117, 98, 118, 127, 39, 128, 36, 
							83, 48, 54, 24, 113, 66, 45, 101, 
							14, 17, 85, 9, 44, 97, 117, 54, 
							87, 61, 52, 24, 13, 84, 11, 115, 
							66, 84, 95, 123, 97, 123, 62, 115, 
							79, 13, 43, 99, 14, 31, 37, 95, 
							44, 92, 25, 97, 81, 77, 25, 44, 
							93, 101, 59, 126, 86, 93, 50, 70, 
							121, 33, 91, 37, 94, 83, 85, 61, 
							65, 30, 72, 82, 18, 38, 15, 37, 
							1, 85, 47, 29, 87, 102, 84, 95, 
							28, 97, 122, 102, 63, 52, 106, 89, 
							2, 30, 39, 108, 17, 119, 56, 30, 
							54, 109, 22, 11, 103, 23, 128, 45]

exp_d = [32, 1 , 2 , 3 , 4 , 5 , 4 , 5,
         6 , 7 , 8 , 9 , 8 , 9 , 10, 11,
         12, 13, 12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21, 20, 21,
         22, 23, 24, 25, 24, 25, 26, 27,
         28, 29, 28, 29, 30, 31, 32, 1 ]


per = [ 16,  7, 20, 21,
        29, 12, 28, 17,
         1, 15, 23, 26,
         5, 18, 31, 10,
         2,  8, 24, 14,
        32, 27,  3,  9,
        19, 13, 30,  6,
        22, 11,  4, 25 ]


sbox =  [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
          [ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
          [ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
          [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ]],
            
         [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
           [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ]],
   
         [ [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
           [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
           [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]],
       
          [ [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
           [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
           [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14] ],
        
          [ [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
           [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
           [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]],
       
         [ [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
           [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13] ],
         
          [ [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
           [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12] ],
        
         [ [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11] ] ]

def encryption(pt , rk1 , rkb1 , rk2 , rkb2):
	pt = hex2bin(pt)
	print(pt)
 
	pt = permute(pt , initial_perm , 128)
	A = pt[0:32]
	B = pt[32:64]
	C = pt[64:96]
	D = pt[96:128]

	# print(f"A : {A}")
	# print("B : {}".format(B))
	# print("C : {}".format(C))
	# print("D : {}".format(D))

	for i in range(0 , 16):
		B_exp = permute(B , exp_d , 48)
		D_exp = permute(D , exp_d , 48)
	
		xor_x1 = xor(B_exp , rkb1[i])
		xor_x2 = xor(D_exp , rkb2[i])
	
		sbox_str1 = ""
		for j in range(0, 8):
			row = bin2dec(int(xor_x1[j * 6] + xor_x1[j * 6 + 5]))
			col = bin2dec(int(xor_x1[j * 6 + 1] + xor_x1[j * 6 + 2] + xor_x1[j * 6 + 3] + xor_x1[j * 6 + 4]))
			val = sbox[j][row][col]
			sbox_str1 = sbox_str1 + dec2bin(val)

		sbox_str2 = ""
		for j in range(0, 8):
			row = bin2dec(int(xor_x2[j * 6] + xor_x2[j * 6 + 5]))
			col = bin2dec(int(xor_x2[j * 6 + 1] + xor_x2[j * 6 + 2] + xor_x2[j * 6 + 3] + xor_x2[j * 6 + 4]))
			val = sbox[j][row][col]
			sbox_str2 = sbox_str2 + dec2bin(val)
	 
		sbox_str1 = permute(sbox_str1, per, 32)
		sbox_str2 = permute(sbox_str2, per, 32)
	
		result1 = xor(A, sbox_str1)
		A = result1
		result2 = xor(C, sbox_str2)
		B = result2
	
		if i != 15:
			A,B,C,D = B,C,D,A

	combine = A+B+C+D
	c_text = permute(combine  , final_perm , 128)
	return c_text;

def sdes(plain):
    while(len(plain) < 16):
        plain=plain + 'X'
    plain=char2hex(plain)
    key = "aabb09182736ccddccdd09182736aabb"
    key = hex2bin(key)
    k1 = key[0:64]
    k2 = key[64:128]
    key1 = permute(k1, keyp, 56)
    key2 = permute(k2, keyp, 56)
    U = key1[0:28]
    V = key1[28:56]
    Z = key2[0:28]
    W = key2[28:56]
    key1_r = []
    key1_rb = []
    key2_r = []
    key2_rb = []
    for i in range(0 , 16):
        U = shift_left(U , shift_table[i])
        V = shift_left(V , shift_table[i])
        Z = shift_left(Z , shift_table[i])
        W = shift_left(W , shift_table[i])
        combine_str1 = U+V
        combine_str2 = Z+W
        round_key1 = permute(combine_str1 , key_comp , 48)
        round_key2 = permute(combine_str2 , key_comp , 48)
        key1_rb.append(round_key1)
        key2_rb.append(round_key2)
        key1_r.append(bin2hex(round_key1))
        key2_r.append(bin2hex(round_key2))
    
    return bin2hex(encryption(plain, key1_r , key1_rb , key1_r ,key2_rb ))
	

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/algo1',methods=['GET','POST'])
def hello_world():
    image=''
    img=''
    new_img_name=''
    ans=''
    if request.method=='POST':
        if request.files:
            print('Filess are present')
            image=request.files['ciph']
            if image.filename=="":
                print("Image must have the filename")
                return redirect(request.url)
            if not allowed_image(image.filename):
                print("IMAGE EXTENSIONS ARE NOT VALID")
                return redirect(request.url)
            image.save(os.path.join(app.config["IMAGE_UPLOADS"],image.filename))
            print("IMAGE SAVED")
            plain=request.form['plain']
            print("PLAIN TEXT BEFORE ENCRYTPION " + plain)

            if(len(plain) !=0 ):
                plain=sdes(plain)
            print("PLAIN TEXT AFTER ENCRYPTION " + plain)

            

            




            img=os.path.join(app.config['IMAGE_UPLOADS'],image.filename)
            imag=Image.open(img,'r')
            print(imag)
            if(len(plain)==0):
                ans=decode(image.filename)
                print('Decoded data ' + str(ans))
                return render_template('index.html',output=ans)
                
                # raise ValueError('Data is Empty')
            newimg=imag.copy()
            encode_enc(newimg,plain)
            new_image_path=os.path.join(app.config['IMAGE_UPLOADS'],)
            new_img_name="stego_img" + image.filename
            new_image_path=os.path.join(app.config['IMAGE_UPLOADS'],new_img_name)
            newimg.save(new_image_path, str(new_img_name.split(".")[1].upper()))




        # img=
    return render_template('index.html',output=ans)

if __name__=="__main__":
    app.run(debug=True, port=8000)


 


