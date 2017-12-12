from PIL import Image, ImageDraw
import face_recognition
import faceswap
from tkinter import Tk, Listbox ,Label, Button, Entry, filedialog

#얼굴부분 크롭
class face_detect:
    def __init__(self):
        self.image1 = ""
        self.image2 = ""
    def face_crop(self) :
        # Load the jpg file into a numpy array
        image = face_recognition.load_image_file(self.image1)

        # Find all the faces in the image using the default HOG-based model.
        # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
        # See also: find_faces_in_picture_cnn.py
        face_locations = face_recognition.face_locations(image)

        listbox.insert(0, "사진에서 {}개의 얼굴을 찾았습니다.".format(len(face_locations)))

        #findfacesize.pack()
        for face_location in face_locations:

            # Print the location of each face in this image
            top, right, bottom, left = face_location
            #print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

            listbox.insert(0, "얼굴 위치 Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
            #facelocation_xy.pack()
            # You can access the actual face itself like this:
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            pil_image.save("cut_image.jpg")
            listbox.insert(2, "Image file save '(Name : cut_image.jpg)' ")
            pil_image.show()

    def callback2(self) :
        # Load the jpg files into numpy arrays
        biden_image = face_recognition.load_image_file("유재석.png")
        obama_image = face_recognition.load_image_file("하하.jpg")
        unknown_image = face_recognition.load_image_file("하하2.jpg")

        # Get the face encodings for each face in each image file
        # Since there could be more than one face in each image, it returns a list of encodings.
        # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

        known_faces = [
            biden_face_encoding,
            obama_face_encoding
        ]

        # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
        results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
            
        print("Is the unknown face a picture of 유재석? {}".format(results[0]))
        print("Is the unknown face a picture of 하하? {}".format(results[1]))
        print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))

    def face_makeup(self):
        image = face_recognition.load_image_file(self.image1)

        # Find all facial features in all the faces in the image
        face_landmarks_list = face_recognition.face_landmarks(image)

        for face_landmarks in face_landmarks_list:
            pil_image = Image.fromarray(image)
        d = ImageDraw.Draw(pil_image, 'RGBA')

        # Make the eyebrows into a nightmare
        d.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
        d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
        d.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)
        d.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)

        # Gloss the lips
        d.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
        d.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
        d.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=8)
        d.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=8)

        # Sparkle the eyes
        d.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
        d.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

        # Apply some eyeliner
        d.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=6)
        d.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=6)

        pil_image.save('face_makeup.jpg')
        pil_image.show()

    def face_drawline(self):
        image = face_recognition.load_image_file(self.image1)

        # Find all facial features in all the faces in the image
        face_landmarks_list = face_recognition.face_landmarks(image)

        print("I found {} face(s) in this photograph.".format(len(face_landmarks_list)))

        for face_landmarks in face_landmarks_list:

            # Print the location of each facial feature in this image
            facial_features = [
                'chin',
                'left_eyebrow',
                'right_eyebrow',
                'nose_bridge',
                'nose_tip',
                'left_eye',
                'right_eye',
                'top_lip',
                'bottom_lip'
            ]

            for facial_feature in facial_features:
                print("The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))

            # Let's trace out each facial feature in the image with a line!
            pil_image = Image.fromarray(image)
            d = ImageDraw.Draw(pil_image)

            for facial_feature in facial_features:
                d.line(face_landmarks[facial_feature], width=5)
            pil_image.save("face_drawline.jpg")
            pil_image.show()
    def call_first_file(self):
        window.filename =  filedialog.askopenfilename(initialdir = "C:\\Users\lenovo\Documents\ face_recognition\examples",title = "choose your file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        call_file_name = Label(window, text=window.filename)
        call_file_name.grid(row = 3, column=3)

        self.image1 = window.filename

    def call_second_file(self):
        window.filename =  filedialog.askopenfilename(initialdir = "C:\\Users\lenovo\Documents\ face_recognition\examples",title = "choose your file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        call_file_name = Label(window, text=window.filename)
        call_file_name.grid(row = 3, column=3)

        self.image2 = window.filename
    def face_swap(self):
        faceswap.main(self.image1, self.image2)

window = Tk()
window.title('얼굴인식프로그램')

a = face_detect()
b1 = Button(window, text="파일가져오기",command=a.call_first_file)
b2 = Button(window, text="secondfile",command=a.call_second_file)
b3 = Button(window, text="얼굴크롭",command=a.face_crop)
b4 = Button(window, text="얼굴찾기",command=a.callback2)
b5 = Button(window, text="Make Up", command=a.face_makeup)
b6 = Button(window, text="Draw Line", command=a.face_drawline)
b7 = Button(window, text="Face Swap", command=a.face_swap)
listbox = Listbox(window, width=40, height=10)
b1.grid(row=0, column=0)		# 버튼 b1을 윈도우 내에 grid 로 배치. 위치는 (0, 0)
b2.grid(row=0, column=1)		# 버튼 b2를 윈도우 내에 grid 로 배치. 위치는 (1, 1)
b3.grid(row=0, column=2)
b4.grid(row=1, column=0)
b5.grid(row=1, column=1)
b6.grid(row=1, column=2)
b7.grid(row=1, column=3)
listbox.place(x=0, y=100)
# listbox.grid(row=2, column=0 + 1 + 2)

window.mainloop()
