import tkinter as tk
from tkinter.scrolledtext import *

from typing import List
from allennlp.predictors import Predictor
from allennlp.models.archival import load_archive
from allennlp_models.generation import (
    ComposedSeq2Seq,
)  # Need this for loading model archive


from nla_metric import (
    NlaMetric,
)  # Need this for loading model archive


# MODEL CODE ################################

archive = load_archive("model.tar.gz")
predictor = Predictor.from_archive(archive, "seq2seq")


def translate_nla(source: str) -> str:
    prediction_data = predictor.predict_json({"source": source})
    return " ".join(prediction_data["predicted_tokens"])


# TEXT VARIABLE #############################

all_conv = []  # this variable holds ALL the content of the conversation between the user and the bot


# INTERFACE CODE ############################

root = tk.Tk()

# specify size of window.
root.geometry("500x400")
root.resizable(False, False)

# make a scrollbar
w = tk.Scrollbar(root)

# Create principal text widget and specify size.
textBoxPrincipal = ScrolledText(root, height = 20, width = 52, wrap=tk.WORD, state=tk.NORMAL)

w.config(command=textBoxPrincipal.yview)

# create small text widget
entryInput = tk.Entry(root)

# Create label
l = tk.Label(root, text = "Conversation with a bot")
l.config(font =("Courier", 14))


def postAnswer():
    global all_conv

    userInput = entryInput.get()
    if userInput == "":
        return
    entryInput.delete(0,'end')

    # print the EXACT sentence written by the user
    textBoxPrincipal.config(state="normal")
    textBoxPrincipal.insert(tk.END, "USER: ")
    textBoxPrincipal.insert(tk.END, userInput)
    textBoxPrincipal.insert(tk.END, "\n\n")
    textBoxPrincipal.config(state="disabled")
    textBoxPrincipal.yview(tk.END) # scroll text into view


    userInput = treatEntry(userInput)
    all_conv.append(userInput)


    # if the loaded model has been trained with the A => B corpus
    #botAnswer = getBotAnswer(userInput)

    # if the loaded model has been trained with the B A => B corpus
    if len(all_conv) > 1:
        botAnswer = getBotAnswer(all_conv[-2] + " " + all_conv[-1])
    else:
        botAnswer = getBotAnswer(all_conv[-1])


    botAnswer = treatOutput(botAnswer) # beautify the bot's output
    all_conv.append(botAnswer)


    # write the answer by the bot
    textBoxPrincipal.config(state="normal")
    textBoxPrincipal.insert(tk.END, "CCC-BOT: ")
    textBoxPrincipal.insert(tk.END, botAnswer)
    textBoxPrincipal.insert(tk.END, "\n\n")

    textBoxPrincipal.config(state="disabled")
    textBoxPrincipal.yview(tk.END)



def getBotAnswer(userInput):
    # get the bot's answer to our sentence
    output = translate_nla(userInput)
    return output


def treatEntry(input):
    # the goal of this function will be to make sure that what is sent to 
    return input


def treatOutput(output):
    return output

# Create button for sending input
b1 = tk.Button(root, text = "Send", command=postAnswer)


root.bind_all("<Return>", lambda event: postAnswer()) # bind the Enter key to sending the message

w.pack(side=tk.RIGHT, fill=tk.Y)
l.pack()
textBoxPrincipal.pack()
entryInput.pack()
b1.pack()


entryInput.focus_set()

tk.mainloop()
