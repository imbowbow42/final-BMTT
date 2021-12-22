#app.py
from captcha.image import ImageCaptcha
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw
import sys
from random import SystemRandom, random, randint
import zipfile
import io
import pandas as pd


 
app = Flask(__name__)
 
UPLOAD_FOLDER = './static/uploads'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route('/register/display')
def registerDisplayPage():
    return render_template('register_display.html')

@app.route('/vclogin/')
def vclogin():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
             
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        decrypt(UPLOAD_FOLDER+ '/' +filename) # goi hàm decrypt 2 tấm ảnh
        return render_template('index.html', filename= UPLOAD_FOLDER+ '/' +filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
    
def decrypt(file_path):
    infile1 = Image.open(file_path)
    infile2 = Image.open('static/uploads/_B.png')

    outfile = Image.new('1', infile1.size)

    for x in range(infile1.size[0]):
        for y in range(infile1.size[1]):
            outfile.putpixel((x, y), max(infile1.getpixel((x, y)), infile2.getpixel((x, y))))
    outfile.save('static/uploads/decrypted.png','PNG')

 
@app.route('/register/')
def register():
    return render_template('register.html')

@app.route('/register/', methods = ['POST'])
def generate_captcha():
    
    image = ImageCaptcha(width = 280, height = 90)
    captcha_text = str(randint(10000, 99999))
    data = image.generate(captcha_text) 
    image.write(captcha_text, './static/uploads/captcha.png')
    random = SystemRandom()
    xrange = range


    infile = str("./static/uploads/captcha.png")

    if not os.path.isfile(infile):
        print("That file does not exist.")
        exit()

    img = Image.open(infile)

    f, e = os.path.splitext(infile)
    out_filename_A = UPLOAD_FOLDER+"/_A.png"
    out_filename_B = UPLOAD_FOLDER+"/_B.png"

    img = img.convert('1')  # convert image to 1 bit

    print("Image size: {}".format(img.size))
    # Prepare two empty slider images for drawing
    width = img.size[0]*2
    height = img.size[1]*2
    print("{} x {}".format(width, height))
    out_image_A = Image.new('1', (width, height))
    out_image_B = Image.new('1', (width, height))
    draw_A = ImageDraw.Draw(out_image_A)
    draw_B = ImageDraw.Draw(out_image_B)

    # There are 6(4 choose 2) possible patterns and it is too late for me to think in binary and do these efficiently
    patterns = ((1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1),
                (0, 1, 1, 0), (0, 1, 0, 1), (0, 0, 1, 1))
    # Cycle through pixels
    for x in xrange(0, int(width/2)):
        for y in xrange(0, int(height/2)):
            pixel = img.getpixel((x, y))
            pat = random.choice(patterns)
            # A will always get the pattern
            draw_A.point((x*2, y*2), pat[0])
            draw_A.point((x*2+1, y*2), pat[1])
            draw_A.point((x*2, y*2+1), pat[2])
            draw_A.point((x*2+1, y*2+1), pat[3])
            if pixel == 0:  # Dark pixel so B gets the anti pattern
                draw_B.point((x*2, y*2), 1-pat[0])
                draw_B.point((x*2+1, y*2), 1-pat[1])
                draw_B.point((x*2, y*2+1), 1-pat[2])
                draw_B.point((x*2+1, y*2+1), 1-pat[3])
            else:
                draw_B.point((x*2, y*2), pat[0])
                draw_B.point((x*2+1, y*2), pat[1])
                draw_B.point((x*2, y*2+1), pat[2])
                draw_B.point((x*2+1, y*2+1), pat[3])

    out_image_A.save(out_filename_A, 'PNG')
    out_image_B.save(out_filename_B, 'PNG')

    compressFile()

    return render_template('register_display.html')


def compressFile():
    file_name1 = "static/uploads/_A.png"
    file_name2 = "static/uploads/captcha.png"
    file_name_list = [file_name1, file_name2]
    zip_file_name = "static/zipfile/shares.zip"


    file_compress(file_name_list, zip_file_name)


def file_compress(inp_file_names, out_zip_file):

    compression = zipfile.ZIP_DEFLATED
    print(f" *** Input File name passed for zipping - {inp_file_names}")

    # create the zip file first parameter path/name, second mode
    print(f' *** out_zip_file is - {out_zip_file}')
    zf = zipfile.ZipFile(out_zip_file, mode="w")

    try:
        for file_to_write in inp_file_names:
        # Add file to the zip file
        # first parameter file to zip, second filename in zip
            print(f' *** Processing file {file_to_write}')
            zf.write(file_to_write, file_to_write, compress_type=compression)

    except FileNotFoundError as e:
        print(f' *** Exception occurred during zip process - {e}')
    finally:
    # Don't forget to close the file!
        zf.close()
if __name__ == "__main__":
    app.run(debug=True)