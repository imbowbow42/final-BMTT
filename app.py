#app.py
from captcha.image import ImageCaptcha
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw
import sys
from random import SystemRandom, random, randint



 
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

        #WRITE PYTHON CODE HERE
        ###############################
        random = SystemRandom()
        xrange = range


        infile = str("./vc-webapp/static/uploads/Screenshot_from_2021-12-19_19-51-55_A.png")

        if not os.path.isfile(infile):
            print("That file does not exist.")
            exit()

        img = Image.open(infile)

        f, e = os.path.splitext(infile)
        out_filename_A = UPLOAD_FOLDER+"_A.png"
        out_filename_B = UPLOAD_FOLDER+"_B.png"

        img = img.convert('1')  # convert image to 1 bit

        print("Image size: {}".format(img.size))
        # Prepare two empty slider images for drawing
        width = img.size[0]*1
        height = img.size[1]*1
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
        

        ###############################
        file.filename = "./vc-webapp/static/uploads/_A.png"
        filename = "./vc-webapp/static/uploads/_A.png"

        # print(type(file.filename))
        # print(type(filename))
        filename = secure_filename(file.filename)
             
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below ')

        
        
        print(file.filename)
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>', methods = ['GET'])
def display_image():
    filename = "_A.png"
    print('display_image filename: ' + filename)
    return redirect(url_for('./static', filename='uploads/' + filename), code=301)
 
@app.route('/register/')
def register():
    return render_template('register.html')

@app.route('/register/', methods = ['POST'])
def generate_captcha():
    image = ImageCaptcha(width = 280, height = 90)
    captcha_text = str(randint(10000, 99999))
    data = image.generate(captcha_text) 
    image.write(captcha_text, './static/uploads/captcha.png')
    return render_template('register_display.html')

if __name__ == "__main__":
    app.run(debug=True)