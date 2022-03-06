from distutils import text_file
from email.policy import default
from fileinput import filename
from pydoc import text
from tracemalloc import start
from click import command
import pyttsx3
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import END, Tk, filedialog, ttk, messagebox
import PyPDF2
from pdfminer import high_level




root = tk.Tk()
root.title('My Text-Speech')

window_width = 700
window_height = 280

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# root.geometry('700x280')
root.configure(bg='#ffffff')
root.resizable(0,0)




def convertAndPlay():

    voices = bot.getProperty('voices')
    bot.setProperty('voice','english+f4')
    bot.setProperty('rate', speed_scale.get())
    text = text_box.get(0.0,tk.END)

    if len(text)>1:
        bot.say(text)
        bot.runAndWait()
    else:
        messagebox.showwarning('Warning', 'enter words to convert to audio')





def saveAudio():

    bot = pyttsx3.init()
    voices = bot.getProperty('voices')
    bot.setProperty('voice',voices[voice_var.get()])
    bot.setProperty('rate', speed_scale.get())
    text = text_box.get(0.0,tk.END)

    if len(text.strip())>1:
        filename = filedialog.asksaveasfilename(defaultextension='.mp3')
        
        if filename:
            bot.save_to_file(text, filename)
            bot.runAndWait()
            messagebox.showinfo('saved ok')
    else:
        messagebox.showwarning('Warning', 'enter words to convert to audio')





# function for opening textFile
def open_txt():
    txt_file = filedialog.askopenfilename(

        initialdir="/home/ayukjohn/Documents/", 
        title="Open Text File", 
        filetypes=(("Text Files", "*.txt"),)
        )
    txt_file = open(txt_file,'r')
    box = txt_file.read()
    text_box.insert(END, box)

    txt_file.close()



# function for opening pdfFile
def open_pdf():
    txt_file = filedialog.askopenfilename(

        initialdir="/home/ayukjohn/Documents/", 
        title="Open PDF File", 
        filetypes=(("PDF Files", "*.pdf"),)
        )
    
    if txt_file:
        # pdf_file = PyPDF2.PdfFileReader(txt_file)

        page =[]

        page_extract = high_level.extract_text(txt_file, "",page )

        text_box.insert(END, page_extract)





bot = pyttsx3.init()
voice_var = tk.IntVar()

text_box = ScrolledText(
    root, font=('Sitka Small',11), bd=2, relief=tk.GROOVE, wrap=tk.WORD,
    undo=True
)

text_box.place(x=5, y=5, height=270, width=390)

frame = tk.Frame(root, bd=0.3, relief=tk.SUNKEN)
frame.place(x=395, y=3, height=270, width=800)



change_speed_frame = ttk.LabelFrame(frame, text='Change Speed')
change_speed_frame.grid(row=0, column=0, pady=5, padx=4)

speed_scale = tk.Scale(change_speed_frame, from_=100, to=300, orient=tk.HORIZONTAL, bg='#ffffff')
speed_scale.set(170)
speed_scale.grid(row=1, columnspan=1, ipady=5, ipadx=5)



# frame3 = ttk.LabelFrame(frame, text='Change Voice')
# frame3.grid(row=1, column=0, pady=5)

# R1 = tk.Radiobutton(frame3, text='Male', variable=voice_var, value= 'english')
# R1.grid(row=0, column=0, ipady=5, ipadx=7, padx=5 )

# R2 = tk.Radiobutton(frame3, text='Female', variable=voice_var ,value='english+f4' )
# R2.grid(row=0, column=1, ipady=5, ipadx=7, padx=5 )




frame_holding_btns = tk.Frame(frame, bd=1, relief=tk.SUNKEN)
frame_holding_btns.grid(row=2, column=0, pady=10, ipadx=10)
# frame_holding_btns.place(height=2, width=10)


convert_play_button = ttk.Button(frame_holding_btns, text='Convert & Play', width=15, command= lambda :threading.Thread(target=convertAndPlay, daemon=True).start())
convert_play_button.grid(row=0, column=0, ipady=5, pady=4, padx=5 )



save_audio_btn = ttk.Button(frame_holding_btns,text='Save as Audio', width=15, command=saveAudio)
save_audio_btn.grid(row=1, column=0, ipady=5, pady=4, padx=5 )



clear_btn = ttk.Button(frame_holding_btns,text='Clear', width=5, command = lambda: text_box.delete(1.0, END))
# btn_3 = ttk.Button(frame_holding_btns,text='Clear', width=5, command = clear_all)

clear_btn.grid(row=2, column=0, ipady=5, pady=4, padx=5 )

openFile = ttk.Button(frame_holding_btns,text='open_txtFile', width=10, command=open_txt  )
openFile.grid(row=2, column=2, ipady=2,  pady=2, padx=1 )

openPDF = ttk.Button(frame_holding_btns,text='open_pdf_file', width=10, command=open_pdf  )
openPDF.grid(row=1, column=2, ipady=2,  pady=2, padx=1 )


exit_button = ttk.Button(frame_holding_btns,text='Exit', width=4, command=lambda: root.quit())
exit_button.grid(row=0, column=2, ipady=1, pady=1, padx=2 )





root.mainloop()