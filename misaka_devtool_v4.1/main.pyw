import tkinter as tk
import socketio
import eventlet
import tkinter as tk
import shutil
import os



current = os.path.dirname(os.path.abspath(__file__))
sio = socketio.Server()
command = ""
packagedata = ""

@sio.on('connect')
def connect(sid, environ):
    print('client connected')

@sio.on('disconnect')
def disconnect(sid):
    print('client disconnected')

@sio.on('command_request')
def receive(sid, data):
    global command
    sio.emit('command_response', command, room=sid)
    command = ""

@sio.on('data_request')
def receive(sid, data):
    global packagedata
    sio.emit('data_response', packagedata, room=sid)
    packagedata = ""

@sio.on('data_request_respring')
def receive(sid, data):
    global packagedata
    sio.emit('data_response_respring', packagedata, room=sid)
    packagedata = ""

@sio.on('Log')
def receive(sid, data):
    NewNameInput.insert(tk.END, f"{data}\n")
    NewNameInput.see('end')

def respring():
    global command
    command = "Respring"

def makeinstall():
    shutil.make_archive(current+"/Install", 'zip', root_dir=current+"/package")
    f = open(current+"/Install.zip", 'rb')
    global packagedata
    packagedata = f.read()
    f.close()
    global command
    command = "MakeInstall"

def makeinstallandrespring():
    shutil.make_archive(current+"/Install", 'zip', root_dir=current+"/package")
    f = open(current+"/Install.zip", 'rb')
    global packagedata
    packagedata = f.read()
    f.close()
    global command
    command = "MakeInstall_Respring"

def server_startup_b():
    import threading
    t = threading.Thread(target=server_startup)
    t.start()
    NewNameInput.insert(tk.END, "misaka devtool 4.1\n")
    NewNameInput.insert(tk.END, "Background execution must be enabled in the settings of the misaka app.\n")
    NewNameInput.insert(tk.END, "by しまりん\n")
def server_startup():
    app = socketio.WSGIApp(sio)
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8080)), app)


root = tk.Tk()
root.title(u"misaka devtool")
root.geometry("900x600")

root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

EditFrame = tk.Frame(
    root,
    bg="#161616", 
)
EditFrame.grid(
    column=1,
    row=0,
    sticky="NSEW",
    rowspan=2
)
EditFrame.columnconfigure(0, weight=1)
EditFrame.rowconfigure(1, weight=1)


## AppNameLabel =====================
AppNameLabel = tk.Label(
    EditFrame,
    text="misaka devtool 4.1",
    bg="#eb077f", 
    fg="white"
)
AppNameLabel.grid(
    column=0,
    row=0,
    ipadx=10,
    ipady=10,
    sticky="NEW"
)

## NewNameInput =====================
NewNameInput = tk.Text(
    EditFrame,
    bg="#161616", 
    fg="white",
    highlightthickness=0
)
NewNameInput.grid(
    column=0,
    sticky="NEW",
)
NewNameInput.config(height=root.winfo_height())

## Button Frame =====================
ButtonFrame = tk.Frame(
    EditFrame,
    bg="#161616", 
)
ButtonFrame.grid(
    column=0,
    row=2,
    sticky="NSEW",
)
ButtonFrame.columnconfigure(0, weight=1)
ButtonFrame.columnconfigure(1, weight=1)

## Button ===========================
UnSetButton2 = tk.Button(
    ButtonFrame,
    bg="#eb077f", 
    fg="#eb077f",
    text="Make & Install",
    command=makeinstall
)
UnSetButton2.grid(
    column=1,
    row=0,
    ipadx=10,
    ipady=10,
    sticky="NSEW",
)
SetButton = tk.Button(
    ButtonFrame,
    bg="#eb077f", 
    fg="#eb077f",
    text="Make & Install & Respring",
    command=makeinstallandrespring
)
SetButton.grid(
    column=2,
    row=0,
    ipadx=10,
    ipady=10,
    sticky="NSEW",
)
UnSetButton = tk.Button(
    ButtonFrame,
    bg="#eb077f", 
    fg="#eb077f",
    text="Respring",
    command=respring
)
UnSetButton.grid(
    column=0,
    row=0,
    ipadx=10,
    ipady=10,
    sticky="NSEW",
)

if __name__ == '__main__':
    root.after(1000, server_startup_b)
    root.mainloop()
