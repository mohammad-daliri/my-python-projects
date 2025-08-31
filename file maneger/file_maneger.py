from tkinter import filedialog, messagebox, Button, Tk, Label
import shutil
import os
import easygui


def file_open_box():
    path = easygui.fileopenbox()
    return path


def directory_open_box():
    path = filedialog.askdirectory()
    return path


def open_file():
    path = file_open_box()
    try:
        os.startfile(path)
    except TypeError:
        messagebox.showinfo("EROR", "file has not found")
        


def copy_file():
    source = file_open_box()
    destination = directory_open_box()
    try:
        shutil.copy(source, destination)
        messagebox.showinfo("Done", "The reuested file was successfully copied.")
        
    except:
        messagebox.showinfo("Error", "The reuested file was not found.")
        
        
def delet_file():
    path = file_open_box()
    try:
        os.remove(path)
        messagebox.showinfo("Done", "File has been deleted")
    except:
        messagebox.showinfo("Error", "File did not delet")



def rename_file():
    try:
        file = file_open_box()
        path1 = os.path.dirname(file)
        extention = os.path.splitext(file)
        new_name = input("new name: ")
        path2 = os.path.join(path1, new_name + extention)
        os.rename(file, path2)
        messagebox.showinfo("done", "the name hass been changed")
    except:
        messagebox.showinfo("erroe", "was not suscsseful")
        
        
def move_file():
    source = file_open_box()
    destination = directory_open_box()
    if source == destination:
        messagebox.showinfo("Error", "same path")
    else:
        try:
            shutil.move(source, destination)
            messagebox.showinfo("done", "file has been imported")
        except:
            messagebox.showinfo("error")
            
            
def make_directory():
    path = directory_open_box()
    name = input("name: ")
    path = os.path.join(path, name)
    try:
        os.mkdir(path)
        messagebox.showinfo("done")
    except:
        messagebox.showinfo("error")
        

def remove_directory():
    path = directory_open_box()
    try:
        os.rmdir(path)
    except:
        messagebox.showinfo("error")
        
        
def list_files():
    path = directory_open_box()
    file_list = sorted(os.listdir(path))
    for i in file_list:
        print(i)
        
        
window = Tk()
window.title("File maneger")
window.configure(bg="black")
window.geometry("300x400")
Label(window, text="what can i do").pack()
Button(window, command=open_file, text="Open the file", fg="blue", activebackground="red", bg="white").pack()
Button(window, command=copy_file, text="Copy the file", fg="blue", activebackground="red", bg="white").pack()
Button(window, command=delet_file, text="Delet the file", fg="blue", activebackground="red", bg="white").pack()
Button(window, command=rename_file, text="Rename the file", fg="blue", activebackground="red", bg="white").pack()
Button(window, command=move_file, text="Move the file", fg="blue", activebackground="red", bg="white").pack()
Button(window, command=make_directory, text="create folder", fg="blue", activebackground="red", bg="white").pack()
Button(window, command=remove_directory, text="Remove the folder", fg="blue", activebackground="red", bg="white").pack()
Button(window, command=list_files, text="List of all files", fg="blue", activebackground="red", bg="white").pack()
window.mainloop()