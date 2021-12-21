random = SystemRandom()
        xrange = range


        infile = str("/home/tin/Ton Duc Thang/HK1 nam 3/Bảo Mật Thông Tin/vc-webapp/static/uploads/Screenshot_from_2021-12-19_19-51-55.png")

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