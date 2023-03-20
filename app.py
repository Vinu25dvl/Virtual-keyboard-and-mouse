from flask import Flask,render_template,Response
from main import vm,vm2
from keyboard_new import key

detect=vm()
detect2=vm2()
detect3=key()

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("webpage.html")
@app.route("/vm")
def vmm():
    return render_template("left2.html")
@app.route("/vk1")
def vk1():
    return render_template("left.html")
def gen(detect):
    while True:
        frame=detect.virtual_mouse()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def gen2(detect2):
    while True:
        frame=detect2.virtual_mouse2()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
def gen3(detect3):
    while True:
        frame=detect3.virtual_keyboard()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
         
@app.route("/home")
def start():
    return Response(gen(detect),mimetype='multipart/x-mixed-replace;boundary=frame')
@app.route("/home2")
def start2():
    return Response(gen2(detect2),mimetype='multipart/x-mixed-replace;boundary=frame')
@app.route("/home3")
def start3():
    return Response(gen3(detect3),mimetype='multipart/x-mixed-replace;boundary=frame')
app.run(debug=True)

