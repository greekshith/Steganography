from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

import math
import os

from Encryption import Encryption
from Decryption import Decryption
from StegToolTip import StegToolTip

SELECT_BMP_FILE = 'Select Bitmap (bmp) File'
IMG_SIZE_ERR = 'This image is too short to hide message.'
OPEN_BMP_FIRST = 'Please open a bitmap file first.'


def createtooltip(widget, text):
    tooltip = StegToolTip(widget)

    def enter(event):
        tooltip.showtip(text)

    def leave(event):
        tooltip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


class HiddenInPlainSightApp(Frame):
    def __init__(self, master=None):
        self.file_name_bmp = ''
        Frame.__init__(self,
                       master,
                       borderwidth=1,
                       highlightbackground="black",
                       highlightthickness=1)
        self.pack(fill="both", expand=True)
        self.create_main_window()

    def open_bmp_file(self):
        self.file_name_bmp = askopenfilename(filetypes=[(SELECT_BMP_FILE, '*.bmp')])

        print('selected file name is:' + self.file_name_bmp)

        if not self.file_name_bmp:
            return

        self.name_label['text'] = 'Name: ' + self.file_name_bmp

        if self.message_box.get('1.0', END) != '':
            self.message_box.delete('1.0', END)

        global left_image
        left_image = None
        global left_photo
        left_photo = None
        global right_image
        right_image = None
        global right_photo
        right_photo = None

        left_image = Image.open(self.file_name_bmp)
        w, h = left_image.size
        self.dimensions_label['text'] = 'Dimensions: ' + str(w) + 'x' + str(h)

        self.size_label['text'] = 'Size: ' + str(os.path.getsize(self.file_name_bmp)) + 'Bytes'

        str_av_size_for_steg_bytes = 'Available Size For Stegnography: 0 Bytes'
        str_steg_size = 'Available Size For Stegnography: '
        if left_image.mode == 'L':
            mode8bit_p_bw = 'Mode: 8-Bit Pixels, Black and White'
            self.mode_label['text'] = mode8bit_p_bw
            self.available = int((w * h) / 8 - 4)
            if self.available <= 0:
                self.available_label['text'] = str_av_size_for_steg_bytes
            else:
                self.available_label['text'] = str_steg_size + str(self.available) + 'Bytes'
        elif left_image.mode == 'RGB':
            mode3x8bit_p_tc = 'Mode: 3x8-Bit Pixels, True Color'
            self.mode_label['text'] = mode3x8bit_p_tc
            self.available = int((w * h * 3) / 8 - 4)
            if self.available <= 0:
                self.available_label['text'] = str_av_size_for_steg_bytes
            else:
                self.available_label['text'] = str_steg_size + str(self.available) + 'Bytes'
        else:
            self.mode_label['text'] = 'Mode: ' + left_image.mode

        # resizing the image
        scale_width = image_display_width / w
        scale_height = image_display_height / h
        scale = min(scale_width, scale_height)
        new_width = math.ceil(scale * w)
        new_height = math.ceil(scale * h)
        left_image = left_image.resize((new_width, new_height), Image.NEAREST)

        left_photo = ImageTk.PhotoImage(left_image)

        self.left_image_canvas.create_image(image_display_width / 2,
                                            image_display_height / 2,
                                            anchor=CENTER,
                                            image=left_photo)

    def decrypt(self):
        if self.file_name_bmp == '':
            if self.message_box.get('1.0', END) != '':
                self.message_box.delete('1.0', END)
            self.message_box.insert(END, OPEN_BMP_FIRST)
            return 0
        elif self.available < 1:
            if self.message_box.get('1.0', END) != '':
                self.message_box.delete('1.0', END)
            self.message_box.insert(END, IMG_SIZE_ERR)
            return 0
        else:
            self.invoke_decrypt()

    def invoke_decrypt(self):
        decryption = Decryption(self.file_name_bmp)
        decry_msg = decryption.run()
        if self.message_box.get('1.0', END) != '':
            self.message_box.delete('1.0', END)
        self.message_box.insert(END, 'Hidden message: "' + decry_msg + '".')

    def encrypt(self):
        hide_msg = self.message_box.get('1.0', END).replace('\n', '')
        if self.file_name_bmp == '':
            if hide_msg != '':
                self.message_box.delete('1.0', END)
            self.message_box.insert(END, OPEN_BMP_FIRST)
            return 0
        elif hide_msg == '':
            self.message_box.insert(END, 'Input hidden message here.')
            return 0
        elif len(hide_msg) > self.available:
            if self.message_box.get('1.0', END) != '':
                self.message_box.delete('1.0', END)
            self.message_box.insert(END, 'Input hidden message is larger than ' + str(self.available) + ' bytes.')
            return 0
        else:
            self.invoke_encrypt(hide_msg)

    def invoke_encrypt(self, hide_msg):
        origin_file_name = self.file_name_bmp
        new_file_name = self.file_name_bmp[:-4] + '_hidden' + self.file_name_bmp[-4:]
        encryption = Encryption(origin_file_name,
                                new_file_name,
                                hide_msg)
        encryption.run()
        global right_image
        right_image = Image.open(self.file_name_bmp)
        w, h = right_image.size
        # resize image
        scale_width = image_display_width / w
        scale_height = image_display_height / h
        scale = min(scale_width, scale_height)
        new_width = math.ceil(scale * w)
        new_height = math.ceil(scale * h)
        img = right_image.resize((new_width, new_height), Image.NEAREST)
        global right_photo
        right_photo = ImageTk.PhotoImage(img)
        self.right_image_canvas.create_image(image_display_width / 2,
                                             image_display_height / 2,
                                             anchor=CENTER,
                                             image=right_photo)
        if self.message_box.get('1.0', END) != '':
            self.message_box.delete('1.0', END)
        self.message_box.insert(END, 'Saved the new file into ' + new_file_name + '.')

    def clearFrame(self):
        # destroy all widgets from frame
        for widget in self.winfo_children():
            widget.destroy()

        # this will clear frame and frame will be empty
        # if you want to hide the empty panel then
        # self.pack_forget()

    def switch_to_home(self):
        self.clearFrame()
        self.create_main_window()

    def switch_to_image(self):
        self.clearFrame()
        self.create_widgets_for_image()

    def create_main_window(self):
        main_frame = Frame(self,
                           borderwidth=1,
                           highlightbackground="black",
                           highlightthickness=1)
        main_frame.pack(side='top')

        load = Image.open("./Img/steganography0.jpg")
        render = ImageTk.PhotoImage(load)
        main_img = Label(main_frame, image=render)
        main_img.image = render
        main_img.place(x=0, y=0)
        main_img.pack(side='top')
        createtooltip(main_img,
'''Steganography is the technique of hiding secret data within an ordinary,
non-secret, file or message in order to avoid detection. The secret data
is then extracted at its destination. The use of steganography can be 
combined with encryption as an extra step for hiding or protecting data.''')

        img_button = Button(main_frame,
                            text="                 START STEGANOGRAPHY              ",
                            command=self.switch_to_image)

        img_button.pack(side='top')
        createtooltip(img_button, 'Press this button to start steganography')

    def create_widgets_for_image(self):
        top_frame = Frame(self,
                          borderwidth=1,
                          highlightbackground="black",
                          highlightthickness=1)
        top_frame.pack(side=TOP,
                       fill="both",
                       expand=False)

        tpl_frame = Frame(top_frame,
                          borderwidth=1,
                          highlightbackground="black",
                          highlightthickness=1)
        tpl_frame.pack(side=LEFT,
                       fill="both",
                       expand=True)
        tpr_frame = Frame(top_frame,
                          borderwidth=1,
                          highlightbackground="black",
                          highlightthickness=1)
        tpr_frame.pack(side=RIGHT,
                       fill="both",
                       expand=True)
        open_dialog_frame = Frame(tpl_frame,
                                  borderwidth=1,
                                  highlightbackground="black",
                                  highlightthickness=1)
        open_dialog_frame.pack(side=TOP,
                               fill="both",
                               expand=False)
        home_button = Button(open_dialog_frame,
                             text=' Home ',
                             command=self.switch_to_home)

        home_button.pack(side=LEFT)
        createtooltip(home_button, 'Go back to start page')

        open_dialog_label = Label(open_dialog_frame,
                                  text='Open BMP File:')
        open_dialog_label.pack(side=LEFT)
        open_button = Button(open_dialog_frame,
                             text='Open',
                             command=self.open_bmp_file)
        open_button.pack(side=LEFT)
        createtooltip(open_button, 'Open the image file')

        show_frame = Frame(tpl_frame,
                           borderwidth=1,
                           highlightbackground="black",
                           highlightthickness=1)
        show_frame.pack(side=BOTTOM,
                        fill="both",
                        expand=True)
        self.name_label = Label(show_frame,
                                text='Name: ')
        self.name_label.pack(side=TOP)

        self.dimensions_label = Label(show_frame, text='Dimensions: ')
        self.dimensions_label.pack(side=TOP)

        self.size_label = Label(show_frame, text='Size: ')
        self.size_label.pack(side=TOP)

        self.mode_label = Label(show_frame, text='Available Size For Stegnography: ')
        self.mode_label.pack(side=TOP)

        self.available_label = Label(show_frame, text='Mode: ')
        self.available_label.pack(side=TOP)

        en_de_button_frame = Frame(tpr_frame,
                                   borderwidth=1,
                                   highlightbackground="black",
                                   highlightthickness=1)
        en_de_button_frame.pack(side=TOP,
                                fill="both",
                                expand=True)

        decrypt_button = Button(en_de_button_frame,
                                text='Decryption',
                                command=self.decrypt)
        decrypt_button.pack(side=LEFT,
                            fill='x',
                            expand=True)
        createtooltip(decrypt_button, 'Decrypt text from image')

        encrypt_button = Button(en_de_button_frame,
                                text='Encryption',
                                command=self.encrypt)
        encrypt_button.pack(side=LEFT,
                            fill='x',
                            expand=True)
        createtooltip(encrypt_button, 'Encrypt text into image')

        message_frame = Frame(tpr_frame,
                              borderwidth=1,
                              highlightbackground="black",
                              highlightthickness=1)
        message_frame.pack(side=BOTTOM,
                           fill="both",
                           expand=True)

        self.message_box = Text(message_frame,
                                width=23,
                                height=7)
        self.message_box.pack(side=TOP,
                              fill="both",
                              expand=True)

        cen_frame = Frame(self, borderwidth=1,
                          highlightbackground="black",
                          highlightthickness=1)
        cen_frame.pack(side=BOTTOM,
                       fill="both",
                       expand=True)

        left_frame = Frame(cen_frame,
                           borderwidth=1,
                           highlightbackground="black",
                           highlightthickness=1)
        left_frame.pack(side=LEFT,
                        fill="both",
                        expand=True)

        self.left_image_canvas = Canvas(left_frame,
                                        bg='grey',
                                        width=image_display_width,
                                        height=image_display_height)
        self.left_image_canvas.pack(side=BOTTOM,
                                    fill="both",
                                    expand=True)

        right_frame = Frame(cen_frame,
                            borderwidth=1,
                            highlightbackground="black",
                            highlightthickness=1)
        right_frame.pack(side=RIGHT,
                         fill="both",
                         expand=True)

        self.right_image_canvas = Canvas(right_frame,
                                         bg='grey',
                                         width=image_display_width,
                                         height=image_display_height)
        self.right_image_canvas.pack(side=BOTTOM,
                                     fill="both",
                                     expand=True)


left_image = None
left_photo = None
right_image = None
right_photo = None
image_display_width = 300
image_display_height = 200


def create_app():
    global app
    app = HiddenInPlainSightApp(master=root)
    app.master.title('Hidden In Plain Sight')


if __name__ == "__main__":
    root = Tk()
    root.geometry("1300x800")
    create_app()
    app.mainloop()
