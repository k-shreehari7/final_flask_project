from datetime import datetime
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











@app.route('/',methods=['GET','POST'])
def hello_world():
    image=''
    img=''
    new_img_name=''
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
            print(plain)
            img=os.path.join(app.config['IMAGE_UPLOADS'],image.filename)
            imag=Image.open(img,'r')
            print(imag)
            if(len(plain)==0):
                ans=decode(image.filename)
                print('Decoded data ' + str(ans))
                return redirect(request.url)
                # raise ValueError('Data is Empty')
            newimg=imag.copy()
            encode_enc(newimg,plain)
            new_image_path=os.path.join(app.config['IMAGE_UPLOADS'],)
            new_img_name="stego_img" + image.filename
            new_image_path=os.path.join(app.config['IMAGE_UPLOADS'],new_img_name)
            newimg.save(new_image_path, str(new_img_name.split(".")[1].upper()))




        # img=
    return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True, port=8000)


 


