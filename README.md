# Face detection and recognition with a Telegram bot as a control panel

### Requirements:

- python 3.* and these specific packages
  ```sh
    $ pip3 install python-telegram-bot
    $ pip3 install Pillow OR sudo apt install python3-pil

  ```
- OpenCV 3.*

### How to run:

Create training sample of a person
```sh
$ mkdir db && cd ./db && mkdir <name>

$ mkdir faces
$ python3 data.py <name>
```

To train a chosen recognizer (Eigen, Fisher or LBPH)
```sh
$ python3 train.py recognizer
```

Run a server with a chosen recognizer (Eigen, Fisher or LBPH) and Telegram bot packed in.
Don't forget to insert your bot token first
```sh
$ python3 main.py recognizer port_number
```
Run a client with an ultrasonic sensor connected (Intel Edison is preferred)
```sh
$ python3 ./client/detect.py port_number
```

### Bot commands:

Telegram bot has two commands:
- /stay
- /stop

### /stay
Adds a job which is going to be executed every time detection occurs. If so happened, face_recognition() method is going to try to find any faces and predict who is on a picture, then it will send it to your Telegram chat with a bot.

### /stop
Removes previously added job
