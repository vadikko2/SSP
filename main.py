from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job
from datetime import datetime
import subprocess
import socket
import cv2
import sys
import os

global is_listening
is_listening = True
TOKEN = 'INSERT YOUR BOT TOKEN HERE'
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')

# Connection
subprocess.call('fuser -n tcp ' + sys.argv[2] + '-k' , shell = True)
sock = socket.socket()
print('Trying to connect')
sock.bind(('', int(sys.argv[2])))
print("Opened!")
sock.listen(100)
conn, addr = sock.accept()
print('Connected!', addr)


if sys.argv[1] == 'Eigen':
    recognizer = cv2.face.createEigenFaceRecognizer()
elif sys.argv[1] == 'Fisher':
     recognizer = cv2.face.createFisherFaceRecognizer()
elif sys.argv[1] == 'LBPH':
     recognizer = cv2.face.createLBPHFaceRecognizer()

def face_recognition():

    cap = cv2.VideoCapture(0)

    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    detected_faces = face_cascade.detectMultiScale(gray)

    if len(detected_faces) == 0:
        return 'NO FACES FOUND'
    else:
        for (x, y, w, h) in detected_faces:
            face = img[y:y + h, x: x + w]
            f_gray = cv2.resize(cv2.cvtColor(face, cv2.COLOR_BGR2GRAY),(150,150))
            nbr_predicted = recognizer.predict(f_gray)
            print(nbr_predicted[0])
            cv2.imwrite('./faces/' + str(datetime.now()) + '.png', face)

    cap.release()
    return names[int(nbr_predicted[0])]


def stay_socket(bot, job):
    global is_listening
    while is_listening:
        conn.send(b'1')
        data = conn.recv(1)

        if data == b'1':
            name = face_recognition()

            for picture in os.listdir('./faces/'):
                bot.sendMessage(job.context, text=name)
                bot.sendPhoto(chat_id=job.context,
                              photo=open('./faces/' + picture, 'rb'))
                os.remove('./faces/' + picture)


def stay(bot, update, job_queue, chat_data):
    global is_listening
    is_listening = True
    update.message.reply_text('Listening is on now')
    job = Job(stay_socket, 0, context=update.message.chat_id)
    chat_data['job'] = job
    job_queue.put(job, next_t=0.0)
    update.message.reply_text('OK')


def stop(bot, update, chat_data):
    update.message.reply_text('Camera has been shut down')
    global is_listening
    is_listening = False
    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']


# We don't want to accept anything but /stay and /stop commands
def trash(bot, update):
    update.message.reply_text("I don't understand you.")
    update.message.reply_text('Available commands:\n'           + \
                              '/stay - turn VideoCapture on;\n ' + \
                              '/stop - turn VideoCapture off;'


if __name__ == '__main__':

    try:
        names = []
        names.append('NoName')
        directory_list = os.listdir('./db/')

        for directory in directory_list:
            if directory != '.directory':
                names.append(directory)

        print(names)

        recognizer.load('model_' + sys.argv[1])

        up = Updater(TOKEN)
        up.dispatcher.add_handler(CommandHandler('stay', stay,
                                                        pass_job_queue=True,
                                                        pass_chat_data=True))
        up.dispatcher.add_handler(CommandHandler('stop', stop,
                                                        pass_chat_data=True))
        up.dispatcher.add_handler(MessageHandler(Filters.all, trash))

        up.start_polling()
        up.idle()

    except Exception as error:
        print(error)

    finally:
        sock.close()
