from PIL import Image, ImageDraw
import face_recognition
import faceswap
from tkinter import Tk, Listbox ,Label, Button, Entry, filedialog, Frame

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

        listbox.insert('end', "사진에서 {}개의 얼굴을 찾았습니다.".format(len(face_locations)))

        #findfacesize.pack()
        for face_location in face_locations:

            # Print the location of each face in this image
            top, right, bottom, left = face_location
            #print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

            listbox.insert('end', "얼굴 위치 Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
            #facelocation_xy.pack()
            # You can access the actual face itself like this:
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            pil_image.save("cut_image.jpg")
            listbox.insert('end',  "이미지 파일이 저장 되었습니다. '(Name : cut_image.jpg)' ")
            pil_image.show()

    def callback2(self) :
        # Load the jpg files into numpy arrays
        biden_image = face_recognition.load_image_file("obama.jpg")
        obama_image = face_recognition.load_image_file("haha.jpg")
        unknown_image = face_recognition.load_image_file(self.image1)

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

        # 결과는 알 수없는 얼굴이 known_faces 배열에있는 누군가와 일치 하는지를 나타내는 True / False 배열입니다.
        results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
        '''
        for i in range(len(results)):
            if format(results[i]) ==  'TRUE':
                if i==0:
                    listbox.insert('end', "오바마의 얼굴과 일치합니다.")
                elif i==1:
                    listbox.insert('end', "하하의 얼굴과 일치합니다.")
            else :
                listbox.insert('end', "일치하는 사람이 없습니다.")
        '''
        listbox.insert('end', "오바마의 얼굴과 일치합니다. {}".format(results[0]))
        listbox.insert('end', "하하의 얼굴과 일치합니다. {}".format(results[1]))
        listbox.insert('end', "새로운 얼굴과 일치합니다. {}".format(not True in results))

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

        #listbox.insert('end', "이미지 파일에서 {}개의 얼굴을.".format(len(face_landmarks_list)))

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

            '''
            for facial_feature in facial_features:
                listbox.insert('end',"The {} in this face has the following points: {}".format(facial_feature, face_landmarks[facial_feature]))
            '''

            # Let's trace out each facial feature in the image with a line!
            pil_image = Image.fromarray(image)
            d = ImageDraw.Draw(pil_image)

            for facial_feature in facial_features:
                d.line(face_landmarks[facial_feature], width=5)
            pil_image.save("face_drawline.jpg")
            pil_image.show()
    def call_first_file(self):
        window.filename =  filedialog.askopenfilename(initialdir = "C:\\Users\lenovo\Documents\ face_recognition\examples",title = "choose your file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        #call_file_name = Label(file1, text=window.filename)
        #call_file_name.pack(side = 'left')
        call_file_name1.delete(0, 'end')
        call_file_name1.insert( 0, window.filename )
        self.image1 = window.filename

    def call_second_file(self):
        window.filename =  filedialog.askopenfilename(initialdir = "C:\\Users\lenovo\Documents\ face_recognition\examples",title = "choose your file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        #call_file_name = Label(file2, text=window.filename)
        #call_file_name.pack(side = 'left')
        call_file_name2.delete(0, 'end')
        call_file_name2.insert( 0, window.filename )

        self.image2 = window.filename
    def face_swap(self):
        faceswap.main(self.image1, self.image2)

window = Tk()

#사용자인터페이스 tkinter를 이용한 UI
window.title('얼굴인식프로그램')

main = Frame(window,bd=10)
main.pack()

#오른쪽 도움말 프레임
right = Frame(main)
right.pack(side ='right')

help_label = Label(right,bd=20, justify='left', text="※사용방법\n\n1. 얼굴이 포함된 이미지 파일을 불러온다."+
    "\n(얼굴 합성하기는 합성할 파일 이미지도 선택해야 한다.)"+
    "\n\n2. 하단의 목록중에서 원하는 편집기능을 선택한다."+
	"\n\n3. 가운데에 있는 리스트박스에서 결과가 출력되고 결과이미지파일이 보여진다."+
	"\n\n\n"+
"\n※각 기능별 설명"+
	"\n\n1. 얼굴 크롭"+
	"\n    - 사진에서 얼굴이 있는지 없는지 확인 후 얼굴부분만 크롭에서 출력한다."+
	"\n\n2. 얼굴비교"+
	"\n    - 등록된 얼굴이미지와 비교하여 일치하는지 확인한다."+
    "\n\n3. 메이크업"+
    "\n    - 얼굴의 각 부위(눈,눈썹,턱)를 인식 후 색상을 입힌다."+
    "\n\n4. 얼굴외곽선 그리기"+
	"\n    - 얼굴의 각 부위(눈,눈썹,입,턱)를 인식해서 외곽선을 그린다."+
    "\n\n5. 얼굴 합성하기"+
	"\n    - 두 개의 얼굴이미지를 합성한다."+
    "\n      (성공하면 A의 얼굴에 B의 얼굴이 합성된 'output.jpg'파일이 생성된다.)"
    )
help_label.pack()

#왼쪽프레임
left = Frame(main)
left.pack(side ='left')



file1 = Frame(left)
file1.pack(side= 'top')

file2 = Frame(left)
file2.pack(side= 'top')

middleframe = Frame(left)
middleframe.pack( )

bottomframe = Frame(left)
bottomframe.pack( side = 'bottom' )

a = face_detect()

lb = Label(file1, text="기본 이미지 파일경로 : ")
lb.pack(side = 'left')
call_file_name1 = Entry(file1, width=60)
call_file_name1.pack(side = 'left')
b1 = Button(file1, text="파일가져오기",command=a.call_first_file)
b1.pack(side = 'left')

lb2 = Label(file2, pady=10,text="합성할 이미지 파일경로 : ")
lb2.pack(side = 'left')
call_file_name2 = Entry(file2, width=60)
call_file_name2.pack(side = 'left')
b2 = Button(file2, text="파일가져오기",command=a.call_second_file)
b2.pack(side = 'left')

listbox = Listbox(middleframe, width=80)
listbox.pack()

b3 = Button(bottomframe, pady=15,padx=15, text="얼굴크롭",command=a.face_crop)
b3.pack(side = 'left')
b4 = Button(bottomframe, pady=15,padx=15, text="얼굴비교",command=a.callback2)
b4.pack(side = 'left')
b5 = Button(bottomframe, pady=15,padx=15, text="메이크업", command=a.face_makeup)
b5.pack(side = 'left')
b6 = Button(bottomframe, pady=15,padx=15, text="얼굴외곽선 그리기", command=a.face_drawline)
b6.pack(side = 'left')
b7 = Button(bottomframe, pady=15,padx=15, text="얼굴 합성하기", command=a.face_swap)
b7.pack()

window.mainloop()
