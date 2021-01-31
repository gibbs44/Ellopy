# Import lib
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from PIL import ImageTk, Image

import re
import time
import csv
import os

# Global variable
global open_status_name
open_status_name = False

def open_file():
    #Text and path zone
    global open_status_name
    global open_file_path

    # Hide home page
    label_main.grid_forget()
    my_label_img.grid_forget()

    # Display the areas to interact with the file
    show_text.grid(row=0, columnspan=10, pady=30, padx=15, sticky=NSEW)
    labelframe_table_field.grid(row=1, column=0, sticky=NSEW, padx=15)
    label_table_field.grid()
    radiobutton_IP.grid(sticky=NW, padx=10)
    radiobutton_Date.grid(sticky=NW, padx=10)
    radiobutton_Methode.grid(sticky=NW, padx=10)
    radiobutton_RC.grid(sticky=NW, padx=10)
    radiobutton_UA.grid(sticky=NW, padx=10)
    labelframe_operator.grid(row=1, column=1, sticky=NSEW, padx=15)
    label_operator.grid()
    radiobutton_egale.grid(sticky=NW, padx=10)
    labelframe_free_field.grid(row=1, column=2, sticky=NSEW, padx=15)
    label_regex_field.grid(sticky=NW)
    entry_regex_field.grid(padx=10, sticky=EW)
    button_regex.grid(pady=10, padx=10, sticky=NW)
    button_open_text_regex.place(x=140, y=85)
    button_delete_regex.place(x=270, y=84)
    label_information_field.grid(sticky=NW)
    entry_information_field.grid(padx=10, sticky=EW)
    button_rb_ip.grid(pady=10, padx=10, sticky=NW)
    button_open_text_search.place(x=141, y=212)
    button_delete_search.place(x=270, y=212)


    label_backgroung_dowload = Label(conteneur_main_window, bg='black', height=15, width=80)
    label_backgroung_dowload.place(x=250, y=150)
    my_progress = ttk.Progressbar(conteneur_main_window, orient=HORIZONTAL, length=500, mode='determinate')
    my_progress.place(x=280, y=190)
    label_wait = Label(conteneur_main_window, text='The content of your file is being checked. Please wait.', font=("Arial", 12), justify='center', fg='white', bg='black')
    label_wait.place(x=335, y=155)
    lunch_wait_image = Image.open("image/wait.png")
    resized_wait_image = lunch_wait_image.resize((150, 150), Image.ANTIALIAS)
    new_lunch_wait_img = ImageTk.PhotoImage(resized_wait_image)
    my_label_wait_img = Label(conteneur_main_window, image=new_lunch_wait_img, bg='black')
    my_label_wait_img.place(x=430, y=220)

    open_file_path = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Log File", "*.log"), ("Text File", "*.txt")))
    open_status_name = open_file_path

    if not open_status_name:
        my_progress.place_forget()
        label_wait.place_forget()
        my_label_wait_img.place_forget()
        label_backgroung_dowload.place_forget()
        messagebox.showinfo(title="File not open", message="No file opened. \n \nIf you need help, click on help menu at the top \nof the application.", icon='error')
        label_file_explorer.configure(text="File not open")
        show_text.delete("1.0", END)
    else:
        # Read and show open file
        show_text.delete("1.0", END)
        open_file_name = open_file_path
        open_file = open(open_file_name, 'r')
        file_content = open(open_file_name, 'r')

        for i in range(5):
            line = open_file.readline()

            regex = '(?P<ip>[(\d\.)]+) - - \[(?P<date>.*?) (?P<time_zone>[-+](.*?))\] "(?P<method>\w+) (?P<request_path>.*?) HTTP/(?P<http_version>.*?)" (?P<return_code>\d+) (?P<response_size>\d+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'

            answer = re.findall(regex, line)
            count_answer = len(answer)
            my_progress['value'] += 20
            conteneur_main_window.update_idletasks()
            time.sleep(1)

        if count_answer == 0:

            label_file_explorer.configure(text="Your selected file is located : file type error")
            error_text = 'Your file is not in apache format, try an other file'
            show_text.insert(END, error_text)
            my_progress.place_forget()
            label_wait.place_forget()
            my_label_wait_img.place_forget()
            label_backgroung_dowload.place_forget()

        else:
            content_file = file_content.read()
            show_text.insert(END, content_file)

            label_file_explorer.configure(text="Your selected file is located : " + open_file_name)
            my_progress.place_forget()
            label_wait.place_forget()
            my_label_wait_img.place_forget()
            label_backgroung_dowload.place_forget()

def save_as_file():
    # Variable needed to save the file
    global open_status_name

    # Check if the file is opened
    if not open_status_name:
        messagebox.showinfo(title="File not open", message="No file opened. \n \nIf you need help, click on help menu at the top \nof the application.", icon='error')
    else:
        # Save as file part
        save_as_file_path = filedialog.asksaveasfilename(defaultextension=".log", initialdir="/", title="Save File As", filetypes=(("Log File", "*.log"), ("Text File", "*.txt")))

        if save_as_file_path:
            open_status_name = save_as_file_path
            save_as_file_name = save_as_file_path
            save_as_file_name.replace("/", "")
            save_as_file_path = open(save_as_file_path, 'w')
            save_as_file_path.write(show_text.get(1.0, END))
            save_as_file_path.close()
            # Chek if the user want to opened the new file or not
            msgbox_confirm_save = messagebox.askquestion(title="Opened save as file", message="Do you want to open the save as file you just created?", icon='question')
            if msgbox_confirm_save == 'yes':
                # Open the new file
                show_text.delete("1.0", END)
                path_open_save_as = open(save_as_file_name, 'r')
                open_file_read = path_open_save_as.read()
                label_file_explorer.configure(text="Your selected file is located : " + save_as_file_name)
                label_file_explorer.configure()
                show_text.grid(row=0, columnspan=10, pady=30, padx=15, sticky=NSEW)
                show_text.insert(END, open_file_read)
                save_as_file_path.close()

def save_file():
    #Variable needed to save the file
    global open_status_name

    #Check if the file is opened
    if not open_status_name:
        messagebox.showinfo(title="File not open", message="No file opened. \n \nIf you need help, click on help menu at the top \nof the application.", icon='error')
    else:
        # Confirm file overwrite
        msgbox_confirm_save = messagebox.askquestion(title="Save the changes", message="Are you sure you want to modified the original file ?", icon='warning')
        if msgbox_confirm_save == 'yes':
            filename = open(open_status_name, 'w')
            filename.write(show_text.get(1.0, END))
            filename.close()
            messagebox.showinfo(title="File saved", message="The file was saved", icon='info')
        else:
            messagebox.showinfo(title="File not modified", message="The file was not modified", icon='info')

def export_to_csv():

    global open_status_name

    # Check if the file is opened
    if not open_status_name:
        messagebox.showinfo(title="File not open", message="No file opened. \n \nIf you need help, click on help menu at the top \nof the application.", icon='error')
    else:
        show_text.insert(1.0, 'IP address | Date | Time zone | Time zone | Methode | Request path | HTTP version | Return code | Response size | Referrer | User agent\n')
        rawdata = show_text.get(1.0, END).replace(";", "")
        my_list = rawdata.split("|")

        i = 0
        while os.path.exists("export/Export file %s.csv" % i):
            i += 1

        csvfile = open("export/Export file %s.csv" % i, "w", newline='')

        spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        spamwriter.writerow(my_list)
        csvfile.close()
        messagebox.showinfo(title="File exported", message="Your file has been successfully exported.\nAccess the export folder of the application.", icon='info')


def open_text_search():
    global open_status_name

    show_text.delete("1.0", END)
    path_open_save_as = open(open_status_name, 'r')
    open_file_read = path_open_save_as.read()
    label_file_explorer.configure(text="Your selected file is located : " + open_status_name)
    label_file_explorer.configure()
    show_text.grid(row=0, columnspan=10, pady=30, padx=15, sticky=NSEW)
    show_text.insert(END, open_file_read)

def open_text_regex():
    global open_status_name

    show_text.delete("1.0", END)
    path_open_save_as = open(open_status_name, 'r')
    open_file_read = path_open_save_as.read()
    label_file_explorer.configure(text="Your selected file is located : " + open_status_name)
    label_file_explorer.configure()
    show_text.grid(row=0, columnspan=10, pady=30, padx=15, sticky=NSEW)
    show_text.insert(END, open_file_read)


def search_by_regex():

    #Get the text and the user regex
    user_file = show_text.get(1.0, END)
    regex_user = entry_regex_field.get()
    button_open_text_regex = Button(labelframe_free_field, font="Arial 11", text="Show initial file", command=open_text_regex, width=12)
    button_open_text_regex.place(x=140, y=85)

    x = re.findall(regex_user, user_file)

    l = len(x)

    if l == 0:
        show_text.delete("1.0", END)
        text = "Any field match to your regex. Click on Show file to retry"
        show_text.insert(END, text)
    else:
        show_text.delete("1.0", END)
        for i in range(l):
            toto = re.findall(regex_user, user_file)[i]

            if type(toto) is tuple:
                format_tuple = '{}\n'.format(' | '.join(toto))
                show_text.insert(END, format_tuple)
            else:
                format1 = ("%s |\n" % (toto))
                show_text.insert(END, format1)

def rb_ip():

    button_rb_user_agent.grid_forget()
    button_rb_return_code.grid_forget()
    button_rb_methode.grid_forget()
    button_rb_date.grid_forget()

    button_rb_ip.grid(pady=10, padx=10, sticky=NW)

def rb_date():

    button_rb_ip.grid_forget()
    button_rb_user_agent.grid_forget()
    button_rb_return_code.grid_forget()
    button_rb_methode.grid_forget()
    button_rb_date.grid(pady=10, padx=10, sticky=NW)

def rb_methode():

    button_rb_ip.grid_forget()
    button_rb_user_agent.grid_forget()
    button_rb_return_code.grid_forget()
    button_rb_date.grid_forget()
    button_rb_methode.grid(pady=10, padx=10, sticky=NW)

def rb_return_code():

    button_rb_ip.grid_forget()
    button_rb_user_agent.grid_forget()
    button_rb_methode.grid_forget()
    button_rb_date.grid_forget()
    button_rb_return_code.grid(pady=10, padx=10, sticky=NW)

def rb_user_agent():

    button_rb_ip.grid_forget()
    button_rb_return_code.grid_forget()
    button_rb_methode.grid_forget()
    button_rb_date.grid_forget()
    button_rb_user_agent.grid(pady=10, padx=10, sticky=NW)

def toggle_state(*_):

    if (entry_regex_field.var.get()) and (entry_regex_field.var.get() != " "):
        button_regex['state'] = 'normal'
        button_open_text_regex['state'] = 'normal'
        button_delete_regex['state'] = 'normal'
    else:
        button_regex['state'] = 'disabled'
        button_open_text_regex['state'] = 'disabled'
        button_delete_regex['state'] = 'disabled'

    if (entry_information_field.var.get()) and (entry_information_field.var.get() != " "):
        button_rb_ip['state'] = 'normal'
        button_open_text_search['state'] = 'normal'
        button_rb_date['state'] = 'normal'
        button_rb_methode['state'] = 'normal'
        button_rb_return_code['state'] = 'normal'
        button_rb_user_agent['state'] = 'normal'
        button_delete_search['state'] = 'normal'
    else:
        button_rb_ip['state'] = 'disabled'
        button_open_text_search['state'] = 'disabled'
        button_rb_date['state'] = 'disabled'
        button_rb_methode['state'] = 'disabled'
        button_rb_return_code['state'] = 'disabled'
        button_rb_user_agent['state'] = 'disabled'
        button_delete_search['state'] = 'disabled'

    if entry_information_field.var.get() == "   ":
        my_label_wait_img_ea3.place(x=150, y=80)

    if entry_regex_field.var.get() == "   ":
        my_label_wait_img_ea3.place(x=150, y=80)

def fly_over_image(e):
    lunch_fly_over_image = Image.open("easter_egg/easter_egg.png")
    resized_fly_over_image = lunch_fly_over_image.resize((150, 150), Image.ANTIALIAS)
    fly_over_image_lunch_img = ImageTk.PhotoImage(resized_fly_over_image)
    my_label_img.config(image=fly_over_image_lunch_img)
    my_label_img.image = fly_over_image_lunch_img
    my_label_img.grid(column=2, sticky=NE)

def change_back(e):
    lunch_fly_over_image = Image.open("image/principale.png")
    resized_fly_over_image = lunch_fly_over_image.resize((150, 150), Image.ANTIALIAS)
    fly_over_image_lunch_img = ImageTk.PhotoImage(resized_fly_over_image)
    my_label_img.config(image=fly_over_image_lunch_img)
    my_label_img.image = fly_over_image_lunch_img
    my_label_img.grid(column=2, sticky=NE)

def fly_over_image_help(e):
    lunch_fly_over_image_help = Image.open("easter_egg/easter_egg 2.png")
    resized_fly_over_image_help = lunch_fly_over_image_help.resize((400, 250), Image.ANTIALIAS)
    fly_over_image_lunch_img_help = ImageTk.PhotoImage(resized_fly_over_image_help)
    label_img.config(image=fly_over_image_lunch_img_help)
    label_img.image = fly_over_image_lunch_img_help
    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)

def change_back_help(e):
    lunch_fly_over_image = Image.open("tutorial/1_accueil.png")
    resized_fly_over_image = lunch_fly_over_image.resize((400, 250), Image.ANTIALIAS)
    fly_over_image_lunch_img = ImageTk.PhotoImage(resized_fly_over_image)
    label_img.config(image=fly_over_image_lunch_img)
    label_img.image = fly_over_image_lunch_img
    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)

def forward(image_number, text_number):
    global label_img
    global button_forward
    global button_back
    global image_list
    global label_list
    global label_txt

    label_img.grid_forget()
    label_txt.place_forget()

    label_img = Label(labelframe_viewer, image=image_list[image_number-1])
    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='left', text=label_list[text_number-1])

    button_forward = Button(labelframe_viewer, font="Arial 11", text=">>", command=lambda: forward(image_number+1, text_number+1))
    button_back = Button(labelframe_viewer, font="Arial 11", text="<<", command=lambda: back(image_number-1, text_number-1))

    if image_number == 11:
        button_forward = Button(labelframe_viewer, font="Arial 11", text=">>", state=DISABLED)

    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)
    label_txt.place(x=300, y=275)
    button_back.grid(row=0, column=0)
    button_back.place(x=140, y=125)
    button_forward.grid(row=0, column=8)
    button_forward.place(x=775, y=125)

def back(image_number, text_number):
    global label_img
    global button_forward
    global button_back
    global image_list
    global label_list
    global label_txt

    label_img.grid_forget()
    label_txt.place_forget()

    label_img = Label(labelframe_viewer, image=image_list[image_number - 1])
    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='left', text=label_list[text_number - 1])

    button_forward = Button(labelframe_viewer, font="Arial 11", text=">>", command=lambda: forward(image_number + 1, text_number + 1))
    button_back = Button(labelframe_viewer, font="Arial 11", text="<<", command=lambda: back(image_number - 1, text_number - 1))

    if image_number == 1:
        button_back = Button(labelframe_viewer, font="Arial 11", text="<<", state=DISABLED)

    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)
    label_txt.place(x=300, y=275)
    button_back.grid(row=0, column=0)
    button_back.place(x=140, y=125)
    button_forward.grid(row=0, column=8)
    button_forward.place(x=775, y=125)

def open_q_img(e):
    global label_img
    global image_list
    global label_list
    global label_txt
    global label_open_q

    label_img.grid_forget()
    label_txt.place_forget()

    label_img = Label(labelframe_viewer, image=image_list[0])
    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='left', text=label_list[0])

    label_open_q.configure(fg="#A569BD")

    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)
    label_txt.place(x=300, y=275)


def label_open_extension_img(e):
    global label_img
    global image_list
    global label_list
    global label_txt
    global label_open_extension

    label_img.grid_forget()
    label_txt.place_forget()

    label_img = Label(labelframe_viewer, image=image_list[1])
    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='left', text=label_list[1])

    label_open_extension.configure(fg="#A569BD")

    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)
    label_txt.place(x=300, y=275)


def label_int_regex_img(e):
    global label_img
    global image_list
    global label_list
    global label_txt
    global label_int_regex

    label_img.grid_forget()
    label_txt.place_forget()

    label_img = Label(labelframe_viewer, image=image_list[2])
    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='left', text=label_list[2])

    label_int_regex.configure(fg="#A569BD")

    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)
    label_txt.place(x=300, y=275)


def label_int_rb_img(e):
    global label_img
    global image_list
    global label_list
    global label_txt
    global label_int_radio

    label_img.grid_forget()
    label_txt.place_forget()

    label_img = Label(labelframe_viewer, image=image_list[3])
    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='left', text=label_list[3])

    label_int_radio.configure(fg="#A569BD")

    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)
    label_txt.place(x=300, y=275)

def label_int_interact_img(e):
    global label_img
    global image_list
    global label_list
    global label_txt
    global label_int_interact

    label_img.grid_forget()
    label_txt.place_forget()

    label_img = Label(labelframe_viewer, image=image_list[4])
    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='left', text=label_list[4])

    label_int_interact.configure(fg="#A569BD")

    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)
    label_txt.place(x=300, y=275)

def label_int_fn_img(e):
    global label_img
    global image_list
    global label_list
    global label_txt
    global label_int_fn

    label_img.grid_forget()
    label_txt.place_forget()

    label_img = Label(labelframe_viewer, image=image_list[5])
    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='left', text=label_list[5])

    label_int_fn.configure(fg="#A569BD")

    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)
    label_txt.place(x=300, y=275)

def label_save_as_q_img(e):
    global label_img
    global image_list
    global label_list
    global label_txt
    global label_save_as_q

    label_img.grid_forget()
    label_txt.place_forget()

    label_img = Label(labelframe_viewer, image=image_list[6])
    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='left', text=label_list[6])

    label_save_as_q.configure(fg="#A569BD")

    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)
    label_txt.place(x=300, y=275)

def label_label_csv_q1(e):
    global label_img
    global image_list
    global label_list
    global label_txt
    global label_save_as_q

    label_img.grid_forget()
    label_txt.place_forget()

    label_img = Label(labelframe_viewer, image=image_list[9])
    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='left', text=label_list[9])

    label_csv_q1.configure(fg="#A569BD")

    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)
    label_txt.place(x=300, y=275)

def label_label_csv_q2(e):
    global label_img
    global image_list
    global label_list
    global label_txt
    global label_save_as_q

    label_img.grid_forget()
    label_txt.place_forget()

    label_img = Label(labelframe_viewer, image=image_list[10])
    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='left', text=label_list[10])

    label_csv_q2.configure(fg="#A569BD")

    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)
    label_txt.place(x=300, y=275)

def label_save_as_extension_img(e):
    global label_img
    global image_list
    global label_list
    global label_txt
    global label_save_as_extension

    label_img.grid_forget()
    label_txt.place_forget()

    label_img = Label(labelframe_viewer, image=image_list[7])
    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='left', text=label_list[7])

    label_save_as_extension.configure(fg="#A569BD")

    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)
    label_txt.place(x=300, y=275)


def label_save_as_open_img(e):
    global label_img
    global image_list
    global label_list
    global label_txt
    global label_save_as_open

    label_img.grid_forget()
    label_txt.place_forget()

    label_img = Label(labelframe_viewer, image=image_list[8])
    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='left', text=label_list[8])

    label_save_as_open.configure(fg="#A569BD")

    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)
    label_txt.place(x=300, y=275)


def label_faq_1_multiple(e):
    global show_answer
    global label_faq_1
    global labelframe_faq

    label_faq_1.configure(fg="#A569BD")
    show_answer.config(text="")
    show_answer.config(text='No, you can only open one file at a time.')

def label_faq_2_save_as(e):
    global show_answer
    global label_faq_2

    label_faq_2.configure(fg="#A569BD")
    show_answer.config(text='If you want to open a save-as file you can click \n on yes when you saved it or you can click\n on open an choose your file')

def label_faq_3_save_as(e):
    global show_answer
    global label_faq_3

    label_faq_3.configure(fg="#A569BD")
    show_answer.config(text='If you want to close your file click on open\n and choose a new file. If you don\'t want to\n open a new file then close the application.')


def label_faq_4_regex(e):
    global show_answer
    global label_faq_4

    label_faq_4.configure(fg="#A569BD")
    show_answer.config(text="When you used the regex field you can't use\n an operator is only your text which \nis taken into account ")

def regex_ip():
    # Get the text and the user regex
    user_file = show_text.get(1.0, END)
    var_regex_IP = entry_information_field.get()
    button_open_text_search = Button(labelframe_free_field, font="Arial 11", text="Show initial file", command=open_text_search, width=12)
    button_open_text_search.place(x=141, y=212)

    regex_user = '(?P<ip>' + var_regex_IP + ') - - \[(?P<date>.*?) (?P<time_zone>[-+](.*?))\] "(?P<method>\w+) (?P<request_path>.*?) HTTP/(?P<http_version>.*?)" (?P<return_code>\d+) (?P<response_size>\d+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'

    x = re.findall(regex_user, user_file)
    l = len(x)

    if l == 0:
        show_text.delete("1.0", END)
        text = "Any field match to your regex. Click on Show file to retry"
        show_text.insert(END, text)
    else:
        show_text.delete("1.0", END)
        for i in range(l):
            toto = re.findall(regex_user, user_file)[i]
            format_tuple = "{}\n".format(" | ".join(toto))
            show_text.insert(END, format_tuple)

def regex_date():
    # Get the text and the user regex
    user_file = show_text.get(1.0, END)
    var_regex_Date = entry_information_field.get()
    button_open_text_search = Button(labelframe_free_field, font="Arial 11", text="Show initial file", command=open_text_search, width=12)
    button_open_text_search.place(x=141, y=212)

    regex_user ='(?P<ip>[(\d\.)]+) - - \[(?P<date>' + var_regex_Date + ') (?P<time_zone>[-+](.*?))\] "(?P<method>\w+) (?P<request_path>.*?) HTTP/(?P<http_version>.*?)" (?P<return_code>\d+) (?P<response_size>\d+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
    x = re.findall(regex_user, user_file)

    l = len(x)

    if l == 0:
        show_text.delete("1.0", END)
        text = "Any field match to your regex. Click on Show file to retry"
        show_text.insert(END, text)
    else:
        show_text.delete("1.0", END)
        for i in range(l):
            toto = re.findall(regex_user, user_file)[i]
            format_tuple = "{}\n".format(" | ".join(toto))
            show_text.insert(END, format_tuple)

def regex_method():
    # Get the text and the user regex
    user_file = show_text.get(1.0, END)
    var_regex_Method = entry_information_field.get()
    button_open_text_search = Button(labelframe_free_field, font="Arial 11", text="Show initial file", command=open_text_search, width=12)
    button_open_text_search.place(x=141, y=212)

    regex_user = '(?P<ip>[(\d\.)]+) - - \[(?P<date>.*?) (?P<time_zone>[-+](.*?))\] "(?P<method>' + var_regex_Method + ') (?P<request_path>.*?) HTTP/(?P<http_version>.*?)" (?P<return_code>\d+) (?P<response_size>\d+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
    x = re.findall(regex_user, user_file)

    l = len(x)

    if l == 0:
        show_text.delete("1.0", END)
        text = "Any field match to your regex. Click on Show file to retry"
        show_text.insert(END, text)
    else:
        show_text.delete("1.0", END)
        for i in range(l):
            toto = re.findall(regex_user, user_file)[i]
            format_tuple = "{}\n".format(" | ".join(toto))
            show_text.insert(END, format_tuple)


def regex_return_code():
    # Get the text and the user regex
    user_file = show_text.get(1.0, END)
    var_regex_RC = entry_information_field.get()
    button_open_text_search = Button(labelframe_free_field, font="Arial 11", text="Show initial file", command=open_text_search, width=12)
    button_open_text_search.place(x=141, y=212)

    regex_user = '(?P<ip>[(\d\.)]+) - - \[(?P<date>.*?) (?P<time_zone>[-+](.*?))\] "(?P<method>\w+) (?P<request_path>.*?) HTTP/(?P<http_version>.*?)" (?P<return_code>' + var_regex_RC + ') (?P<response_size>\d+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'

    x = re.findall(regex_user, user_file)

    l = len(x)

    if l == 0:
        show_text.delete("1.0", END)
        text = "Any field match to your regex. Click on Show file to retry"
        show_text.insert(END, text)
    else:
        show_text.delete("1.0", END)
        for i in range(l):
            toto = re.findall(regex_user, user_file)[i]
            format_tuple = "{}\n".format(" | ".join(toto))
            show_text.insert(END, format_tuple)

def regex_user_agent():
    # Get the text and the user regex
    user_file = show_text.get(1.0, END)
    var_regex_User_Agent = entry_information_field.get()
    button_open_text_search = Button(labelframe_free_field, font="Arial 11", text="Show initial file", command=open_text_search, width=12)
    button_open_text_search.place(x=141, y=212)

    var_regex_User_Agent = var_regex_User_Agent.replace("(", "\(")
    var_regex_User_Agent = var_regex_User_Agent.replace("+", "\+")
    var_regex_User_Agent = var_regex_User_Agent.replace(")", "\)")

    regex_user = '(?P<ip>[(\d\.)]+) - - \[(?P<date>.*?) (?P<time_zone>[-+](.*?))\] "(?P<method>\w+) (?P<request_path>.*?) HTTP/(?P<http_version>.*?)" (?P<return_code>\d+) (?P<response_size>\d+) "(?P<referrer>.*?)" "(?P<user_agent>.*?' + var_regex_User_Agent + '.*?)"'

    x = re.findall(regex_user, user_file)

    l = len(x)

    if l == 0:
        show_text.delete("1.0", END)
        text = "Any field match to your regex. Click on Show file to retry"
        show_text.insert(END, text)
    else:
        show_text.delete("1.0", END)
        for i in range(l):
            toto = re.findall(regex_user, user_file)[i]
            format_tuple = "{}\n".format(" | ".join(toto))
            show_text.insert(END, format_tuple)

def delete_search():
    entry_information_field.delete(0, END)

def delete_regex():
    entry_regex_field.delete(0, END)

def forget_img_ea3(e):
    my_label_wait_img_ea3.place_forget()

def reset_help_windows():
    global label_open_q
    global label_open_extension
    global label_int_regex
    global label_int_radio
    global label_int_interact
    global label_int_fn
    global label_save_as_q
    global label_save_as_extension
    global label_save_as_open
    global label_faq_1
    global label_faq_2
    global label_faq_3
    global label_faq_4
    global label_img
    global label_txt
    global button_back
    global label_csv_q1
    global label_csv_q2


    label_open_q.configure(fg="#2471A3")
    label_open_extension.configure(fg="#2471A3")
    label_int_regex.configure(fg="#2471A3")
    label_int_radio.configure(fg="#2471A3")
    label_int_interact.configure(fg="#2471A3")
    label_int_fn.configure(fg="#2471A3")
    label_save_as_q.configure(fg="#2471A3")
    label_save_as_extension.configure(fg="#2471A3")
    label_save_as_open.configure(fg="#2471A3")
    label_faq_1.configure(fg="#2471A3")
    label_faq_2.configure(fg="#2471A3")
    label_faq_3.configure(fg="#2471A3")
    label_faq_4.configure(fg="#2471A3")
    label_csv_q1.configure(fg="#2471A3")
    label_csv_q2.configure(fg="#2471A3")
    show_answer.config(text="")
    label_img.grid_forget()
    label_txt.place_forget()
    label_img = Label(labelframe_viewer, image=image_list[0])
    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='left', text=label_list[0])
    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)
    label_txt.place(x=300, y=275)
    button_back = Button(labelframe_viewer, font="Arial 11", text="<<", command=back, state=DISABLED)
    button_back.grid(row=0, column=0)
    button_back.place(x=140, y=125)

def help_windows():
    # Global variable
    global lunch_img1
    global lunch_img2
    global lunch_img3
    global lunch_img4
    global lunch_img5
    global lunch_img6
    global lunch_img7
    global lunch_img8
    global lunch_img9
    global lunch_img10
    global lunch_img11
    global label_img
    global image_list
    global labelframe_viewer
    global button_forward
    global button_back
    global label_list
    global txt_img_1
    global label_txt
    global label_open_q
    global labelframe_menu_open
    global label_open_extension
    global label_int_regex
    global label_int_radio
    global label_int_interact
    global label_int_fn
    global label_save_as_q
    global label_save_as_extension
    global label_save_as_open
    global show_answer
    global label_faq_1
    global label_faq_2
    global label_faq_3
    global label_faq_4
    global labelframe_faq
    global label_csv_q1
    global label_csv_q2

    # Window
    aboutwindow = Toplevel()
    aboutwindow.title('Ellopy - HELP PAGE')
    aboutwindow.geometry('1024x600')
    aboutwindow.resizable(width=False, height=False)
    aboutwindow.iconbitmap('image/information.ico')

    # init controller
    conteneur_about_window = Frame(aboutwindow)
    conteneur_about_window.columnconfigure(0, minsize=200)
    conteneur_about_window.columnconfigure(1, minsize=200)
    conteneur_about_window.columnconfigure(2, minsize=200)
    conteneur_about_window.columnconfigure(3, minsize=200)
    conteneur_about_window.rowconfigure(1, minsize=40)
    conteneur_about_window.rowconfigure(2, minsize=10)
    conteneur_about_window.grid(row=3, column=3, sticky=NS + EW, padx=5, pady=5)
    aboutwindow.columnconfigure(2)

    # Viewer
    labelframe_viewer = LabelFrame(conteneur_about_window, text=" View tutorial image : ", font=("Arial", 11))
    labelframe_viewer.grid(row=0, columnspan=7, sticky='WE', padx=20, pady=10, ipadx=5, ipady=10)
    show_image = Label(labelframe_viewer, bg="black", font=("Arial", 11), width=60, height=15)
    show_image.grid(row=0, columnspan=8, padx=200, pady=10, sticky='NSEW')

    #Viewer img
    img1_open = Image.open("tutorial/1_accueil.png")
    img1_resized = img1_open.resize((400, 250), Image.ANTIALIAS)
    lunch_img1 = ImageTk.PhotoImage(img1_resized)
    label_img = Label(labelframe_viewer, image=lunch_img1)
    label_img.grid(row=0, column=2)
    label_img.place(x=275, y=13)

    label_img.bind("<Enter>", fly_over_image_help)
    label_img.bind("<Leave>", change_back_help)

    img2_open = Image.open("tutorial/2_open.png")
    img2_resized = img2_open.resize((400, 250), Image.ANTIALIAS)
    lunch_img2 = ImageTk.PhotoImage(img2_resized)

    img3_int = Image.open("tutorial/3_int.png")
    img3_resized = img3_int.resize((400, 250), Image.ANTIALIAS)
    lunch_img3 = ImageTk.PhotoImage(img3_resized)

    img4_int = Image.open("tutorial/4_int.png")
    img4_resized = img4_int.resize((400, 250), Image.ANTIALIAS)
    lunch_img4 = ImageTk.PhotoImage(img4_resized)

    img5_int = Image.open("tutorial/5_int.png")
    img5_resized = img5_int.resize((400, 250), Image.ANTIALIAS)
    lunch_img5 = ImageTk.PhotoImage(img5_resized)

    img6_int = Image.open("tutorial/6_int.png")
    img6_resized = img6_int.resize((400, 250), Image.ANTIALIAS)
    lunch_img6 = ImageTk.PhotoImage(img6_resized)

    img7_saveas = Image.open("tutorial/7_save_as.png")
    img7_resized = img7_saveas.resize((400, 250), Image.ANTIALIAS)
    lunch_img7 = ImageTk.PhotoImage(img7_resized)

    img8_saveas = Image.open("tutorial/8_save_as.png")
    img8_resized = img8_saveas.resize((400, 250), Image.ANTIALIAS)
    lunch_img8 = ImageTk.PhotoImage(img8_resized)

    img9_saveas = Image.open("tutorial/9_save_as.png")
    img9_resized = img9_saveas.resize((400, 250), Image.ANTIALIAS)
    lunch_img9 = ImageTk.PhotoImage(img9_resized)

    img10_saveas = Image.open("tutorial/10_export_to_CSV.png")
    img10_resized = img10_saveas.resize((400, 250), Image.ANTIALIAS)
    lunch_img10 = ImageTk.PhotoImage(img10_resized)

    img11_saveas = Image.open("tutorial/11_export_to_CSV.png")
    img11_resized = img11_saveas.resize((400, 250), Image.ANTIALIAS)
    lunch_img11 = ImageTk.PhotoImage(img11_resized)

    image_list = [lunch_img1, lunch_img2, lunch_img3, lunch_img4, lunch_img5, lunch_img6, lunch_img7, lunch_img8, lunch_img9,lunch_img10, lunch_img11]

    #Viewer button
    button_back = Button(labelframe_viewer, font="Arial 11", text="<<", command=back, state=DISABLED)
    button_back.grid(row=0, column=0)
    button_back.place(x=140, y=125)
    button_forward = Button(labelframe_viewer, font="Arial 11", text=">>", command=lambda: forward(2, 2))
    button_forward.grid(row=0, column=8)
    button_forward.place(x=775, y=125)

    #Viewer label

    txt_img_1 = 'How can I open a file?'
    txt_img_2 = 'What type of extension can I open?'
    txt_img_3 = 'Interface functionality: search by regex'
    txt_img_4 = 'Interface functionality: search using radio buttons'
    txt_img_5 = 'Interface functionality: Interact with the file without modifying it'
    txt_img_6 = 'Interface functionality: see the name of the file and its path'
    txt_img_7 = 'What file extensions can I use to save-as?'
    txt_img_8 = 'Can I open my save-as file without clicking on file > open?'
    txt_img_9 = 'How can I save a save-as file?'
    txt_img_10 = 'Where to find my exported file?'
    txt_img_11 = 'What name for the exported file?'

    label_list = [txt_img_1, txt_img_2, txt_img_3, txt_img_4, txt_img_5, txt_img_6, txt_img_7, txt_img_8, txt_img_9, txt_img_10, txt_img_11]

    label_txt = Label(labelframe_viewer, font=("Arial", 11, "italic"), fg="#A04000", justify='center', text=label_list[0])
    label_txt.place(x=300, y=275)


    # Menu option
    labelframe_menu_open = LabelFrame(conteneur_about_window, text=" (Menu) File > Open : ", font=("Arial", 11))
    labelframe_menu_open.grid(row=1, column=0, sticky=NSEW, padx=12)
    label_open_q = Label(labelframe_menu_open, font=("Arial", 11), justify='left', text="How can I open a file?", fg="#2471A3")
    label_open_q.grid(row=4, column=0, padx=5, pady=5, sticky='W')
    label_open_q.bind('<Button-1>', open_q_img)
    label_open_extension = Label(labelframe_menu_open, font=("Arial", 11), fg="#2471A3", text="What type of extension can I open?")
    label_open_extension.grid(row=5, column=0, padx=5, pady=2, sticky='W')
    label_open_extension.bind('<Button-1>', label_open_extension_img)

    labelframe_int = LabelFrame(conteneur_about_window, text=" Interface functionality : ", font=("Arial", 11))
    labelframe_int.grid(row=1, column=1, sticky=NSEW, padx=12)
    label_int_regex = Label(labelframe_int, font=("Arial", 11), justify='left', text="Search by regex", fg="#2471A3")
    label_int_regex.grid(row=4, column=0, padx=5, pady=1, sticky='W')
    label_int_regex.bind('<Button-1>', label_int_regex_img)
    label_int_radio = Label(labelframe_int, font=("Arial", 11), justify='left', text="Search using radio buttons", fg="#2471A3")
    label_int_radio.grid(row=6, column=0, padx=5, pady=1, sticky='W')
    label_int_radio.bind('<Button-1>', label_int_rb_img)
    label_int_interact = Label(labelframe_int, font=("Arial", 11), justify='left', text="Interact with the file", fg="#2471A3")
    label_int_interact.grid(row=7, column=0, padx=5, pady=1, sticky='W')
    label_int_interact.bind('<Button-1>', label_int_interact_img)
    label_int_fn = Label(labelframe_int, font=("Arial", 11), justify='left', text="File name and path", fg="#2471A3")
    label_int_fn.grid(row=8, column=0, padx=5, pady=1, sticky='W')
    label_int_fn.bind('<Button-1>', label_int_fn_img)

    labelframe_menu_save_as = LabelFrame(conteneur_about_window, text=" (Menu) File > Save As : ", font=("Arial", 11))
    labelframe_menu_save_as.grid(row=1, column=2, sticky=NSEW, padx=12)
    label_save_as_q = Label(labelframe_menu_save_as, font=("Arial", 11), justify='left', text="How can I save-as a file?", fg="#2471A3")
    label_save_as_q.grid(row=4, column=0, padx=5, pady=5, sticky='W')
    label_save_as_q.bind('<Button-1>', label_save_as_q_img)
    label_save_as_extension = Label(labelframe_menu_save_as, font=("Arial", 11), justify='left', text="How can I open my saved-as file?", fg="#2471A3")
    label_save_as_extension.grid(row=5, column=0, padx=5, pady=2, sticky='W')
    label_save_as_extension.bind('<Button-1>', label_save_as_extension_img)
    label_save_as_open = Label(labelframe_menu_save_as, font=("Arial", 11), justify='left', text="How can I save a save-as file?", fg="#2471A3")
    label_save_as_open.grid(row=6, column=0, padx=5, pady=2, sticky='W')
    label_save_as_open.bind('<Button-1>', label_save_as_open_img)

    labelframe_menu_csv = LabelFrame(conteneur_about_window, text=" (Menu) File > Export to CSV : ", font=("Arial", 11))
    labelframe_menu_csv.grid(row=1, column=3, sticky=NSEW, padx=12)
    label_csv_q1 = Label(labelframe_menu_csv, font=("Arial", 11), justify='left', text="Where to find my exported file?", fg="#2471A3")
    label_csv_q1.grid(row=4, column=0, padx=5, pady=5, sticky='W')
    label_csv_q1.bind('<Button-1>', label_label_csv_q1)
    label_csv_q2 = Label(labelframe_menu_csv, font=("Arial", 11), justify='left', text="What name for the exported file?", fg="#2471A3")
    label_csv_q2.grid(row=5, column=0, padx=5, pady=2, sticky='W')
    label_csv_q2.bind('<Button-1>', label_label_csv_q2)

    #FAQ part

    labelframe_faq = LabelFrame(conteneur_about_window, text="Frequently asked question : ", font=("Arial", 11))
    labelframe_faq.grid(row=2, columnspan=7, sticky='WE', padx=15, pady=10, ipadx=5, ipady=5)

    label_faq_1 = Label(labelframe_faq, font=("Arial", 11), justify='left',  fg="#2471A3")
    label_faq_1.configure(text="Can I open multiple files?")
    label_faq_1.grid(row=6, sticky='W', padx=5, pady=2)
    label_faq_1.bind('<Button-1>', label_faq_1_multiple)

    label_faq_2 = Label(labelframe_faq, font=("Arial", 11), justify='left', fg="#2471A3")
    label_faq_2.configure(text="Can I open my save-as file?")
    label_faq_2.grid(row=6, column=1, sticky='W', padx=5, pady=2)
    label_faq_2.bind('<Button-1>', label_faq_2_save_as)

    label_faq_3 = Label(labelframe_faq, font=("Arial", 11), justify='left', fg="#2471A3")
    label_faq_3.configure(text="Can I close my file without exiting the application?")
    label_faq_3.grid(row=7, sticky='W', padx=5, pady=2)
    label_faq_3.bind('<Button-1>', label_faq_3_save_as)

    label_faq_4 = Label(labelframe_faq, font=("Arial", 11), justify='left', fg="#2471A3")
    label_faq_4.configure(text="Can I use an operator in the field regex?")
    label_faq_4.grid(row=7, column=1, sticky='W', padx=5, pady=0)
    label_faq_4.bind('<Button-1>', label_faq_4_regex)

    show_answer = Label(labelframe_faq, bg="white", font=("Arial", 11), width=35, height=3)
    show_answer.grid()
    show_answer.place(x=620, y=1)

    #Menu - Exit

    menubar_help = Menu(aboutwindow)
    file_help = Menu(menubar_help, tearoff=0)
    menubar_help.add_cascade(label='Exit', menu=file_help, font="Arial 11")
    file_help.add_command(label='Exit', command=aboutwindow.destroy, font="Arial 11")
    help_ = Menu(menubar_help, tearoff=0)
    menubar_help.add_cascade(label='Reset', menu=help_, font="Arial 11")
    help_.add_command(label='Reset', command=reset_help_windows, font="Arial 11")

    aboutwindow.config(menu=menubar_help)

# Window
mainwindow = Tk()
mainwindow.title('Ellopy')
mainwindow.geometry('1024x600')
mainwindow.resizable(width=False, height=False)
mainwindow.iconbitmap('image/principale.ico')

# init controller
conteneur_main_window = Frame(mainwindow)
conteneur_main_window.columnconfigure(0, minsize=300)
conteneur_main_window.columnconfigure(1, minsize=200)
conteneur_main_window.columnconfigure(2, minsize=485)
conteneur_main_window.rowconfigure(1, minsize=230)
conteneur_main_window.grid(row=0, column=2, sticky=NS + EW, padx=5, pady=5)
mainwindow.columnconfigure(2)

# Labelframe
labelframe_table_field = LabelFrame(conteneur_main_window, text=" Table field ", font=("Arial", 11))
labelframe_table_field.grid_forget()
labelframe_operator = LabelFrame(conteneur_main_window, text=" Operator ", font=("Arial", 11))
labelframe_operator.grid_forget()
labelframe_free_field = LabelFrame(conteneur_main_window, text=" Free field ", font=("Arial", 11))
labelframe_free_field.grid_forget()

# Label
label_main = Label(conteneur_main_window, text='Welcome to Ellopy' + '\n' + 'To begin click on file and open', font=("Arial", 20), justify='center', fg='#6F7676')
label_main.grid(rowspan=1, columnspan=3, pady=180)

# Label Frame
label_file_explorer = Label(mainwindow, font=("Arial", 11), fg="#12A7C3")
label_file_explorer.place(x=15, y=7)
label_table_field = Label(labelframe_table_field, text="\n Select one item : \n", font=("Arial", 11))
labelframe_table_field.grid_forget()
label_operator = Label(labelframe_operator, text="\n Select one operator : \n", font=("Arial", 11))
labelframe_operator.grid_forget()
label_regex_field = Label(labelframe_free_field, text="\n Enter your regex here : \n", font=("Arial", 11))
label_information_field = Label(labelframe_free_field, text="\n Enter the information you want to check : \n", font=("Arial", 11))

# Image
lunch_image = Image.open("image/principale.png")
resized = lunch_image.resize((150, 150), Image.ANTIALIAS)
new_lunch_img = ImageTk.PhotoImage(resized)
my_label_img = Label(conteneur_main_window, image=new_lunch_img)
my_label_img.grid(column=2, sticky=NE)
my_label_img.bind("<Enter>", fly_over_image)
my_label_img.bind("<Leave>", change_back)


# Show the log text
show_text = ScrolledText(conteneur_main_window, bg="white", fg="black", font=("Arial", 11), width=13, height=13)
show_text.grid_forget()

show_text_save_file_as = ScrolledText(conteneur_main_window, bg="white", fg="black", font=("Arial", 11), width=13, height=13)
show_text_save_file_as.forget()

# Radio button
svRadio_operator = StringVar()
svRadio_operator.set('1')
radiobutton_egale = Radiobutton(labelframe_operator, text='=', variable=svRadio_operator, value='1', font=("Arial", 11))
svRadio_table_field = StringVar()
svRadio_table_field.set('1')
radiobutton_IP = Radiobutton(labelframe_table_field, text="IP", variable=svRadio_table_field, value='1', font=("Arial", 11), command=rb_ip)
radiobutton_Date = Radiobutton(labelframe_table_field, text="Date", variable=svRadio_table_field, value='2', font=("Arial", 11), command=rb_date)
radiobutton_Methode = Radiobutton(labelframe_table_field, text="Method", variable=svRadio_table_field, value='3', font=("Arial", 11), command=rb_methode)
radiobutton_RC = Radiobutton(labelframe_table_field, text="Return Code", variable=svRadio_table_field, value='4', font=("Arial", 11), command=rb_return_code)
radiobutton_UA = Radiobutton(labelframe_table_field, text="User Agent", variable=svRadio_table_field, value='5', font=("Arial", 11), command=rb_user_agent)

# Free field
entry_regex_field = Entry(labelframe_free_field, width=70)
entry_regex_field.focus_set()
entry_regex_field.var = StringVar()
entry_regex_field['textvariable'] = entry_regex_field.var
entry_regex_field.var.trace_add('write', toggle_state)
entry_information_field = Entry(labelframe_free_field, width=70)
entry_information_field.focus_set()
entry_information_field.var = StringVar()
entry_information_field['textvariable'] = entry_information_field.var
entry_information_field.var.trace_add('write', toggle_state)

# Button
button_regex = Button(labelframe_free_field, font="Arial 11", text="Run regex", command=search_by_regex, width=12, state='disabled')
button_open_text_regex = Button(labelframe_free_field, font="Arial 11", text="Show initial file", command=open_text_regex, width=12, state='disabled')
button_delete_regex = Button(labelframe_free_field, font="Arial 11", text="Delete", command=delete_regex, width=12, state='disabled')
button_rb_ip = Button(labelframe_free_field, font="Arial 11", text="Start a research", width=12, state='disabled', command=regex_ip)
button_rb_user_agent = Button(labelframe_free_field, font="Arial 11", text="Start a research", width=12, state=DISABLED, command=regex_user_agent)
button_rb_return_code = Button(labelframe_free_field, font="Arial 11", text="Start a research", width=12, state=DISABLED, command=regex_return_code)
button_rb_methode = Button(labelframe_free_field, font="Arial 11", text="Start a research", width=12, state=DISABLED, command=regex_method)
button_rb_date = Button(labelframe_free_field, font="Arial 11", text="Start a research", width=12, state=DISABLED, command=regex_date)
button_open_text_search = Button(labelframe_free_field, font="Arial 11", text="Show initial file", command=open_text_search, width=12, state='disabled')
button_delete_search = Button(labelframe_free_field, font="Arial 11", text="Delete", command=delete_search, width=12, state='disabled')


lunch_wait_image_ea_3 = Image.open("easter_egg/easter_egg 3.png")
resized_wait_image_ea_3 = lunch_wait_image_ea_3.resize((700, 390), Image.ANTIALIAS)
new_lunch_wait_img_ea3 = ImageTk.PhotoImage(resized_wait_image_ea_3)
my_label_wait_img_ea3 = Label(conteneur_main_window, image=new_lunch_wait_img_ea3, bg='black')
my_label_wait_img_ea3.place_forget()
my_label_wait_img_ea3.bind('<Button-1>', forget_img_ea3)

# Creating Menubar
menubar = Menu(mainwindow)
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file, font="Arial 11")
file.add_command(label='Open', command=open_file, font="Arial 11")
file.add_command(label='Save', command=save_file, font="Arial 11")
file.add_command(label='Save as', command=save_as_file, font="Arial 11")
file.add_command(label='Export to CSV', command=export_to_csv, font="Arial 11")
file.add_separator()
file.add_command(label='Exit', command=mainwindow.destroy, font="Arial 11")
help_ = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=help_, font="Arial 11")
help_.add_command(label='Help', command=help_windows, font="Arial 11")

# display Menu
mainwindow.config(menu=menubar)
mainloop()
