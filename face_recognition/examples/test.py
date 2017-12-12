from PIL import Image
import face_recognition
from tkinter import Tk, Label, Button, Entry, filedialog

#얼굴부분 크롭
def face_crop() :
    # Load the jpg file into a numpy array
    image = face_recognition.load_image_file(window.filename)

    # Find all the faces in the image using the default HOG-based model.
    # This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
    # See also: find_faces_in_picture_cnn.py
    face_locations = face_recognition.face_locations(image)

    #print("I found {} face(s) in this photograph.".format(len(face_locations)))
    findfacesize = Label(window, text="사진에서 {}개의 얼굴을 찾았습니다.".format(len(face_locations)))
    findfacesize.pack()
    for face_location in face_locations:

        # Print the location of each face in this image
        top, right, bottom, left = face_location
        #print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

        facelocation_xy = Label(window, text="얼굴 위치 Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
        facelocation_xy.pack()
        # You can access the actual face itself like this:
        face_image = image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.show()


def callback2() :
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


def call_file():
    window.filename =  filedialog.askopenfilename(initialdir = "C:\\Users\lenovo\Documents\ face_recognition\examples",title = "choose your file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    call_file_name = Label(window, text=window.filename)
    call_file_name.pack()
    #print (window.filename)

window = Tk()
window.title('얼굴인식프로그램')

b1 = Button(window, text="얼굴크롭",command=face_crop)
b1.pack()
b2 = Button(window, text="얼굴찾기",command=callback2)
b2.pack()
#b1.grid(row=0, column=0)		# 버튼 b1을 윈도우 내에 grid 로 배치. 위치는 (0, 0)
#b2.grid(row=1, column=1)		# 버튼 b2를 윈도우 내에 grid 로 배치. 위치는 (1, 1)

lbl = Label(window, text="이름")
#lbl.pack()


txt = Entry(window)
txt.pack()
call_file = Button(window, text="파일가져오기",command=call_file)
call_file.pack()


btnOK = Button(window, text="확인")
btnOK.pack()
window.mainloop()
