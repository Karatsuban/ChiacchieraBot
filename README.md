# ChiacchieraBot
Using the power of machine learning to train a chatbot on a set of telephonic conversations


# Dependencies

This project uses the following packages and library :

-swda (https://github.com/cgpotts/swda)

-tkinter

-typing

-allennlp (https://github.com/allenai/allennlp-guide)

# How to use

## Train the model

-Make sure that AllenNLP and all its dependencies have been properly installed. You can refer to this page https://pypi.org/project/allennlp/ for all information.
-Execute the Beautify.py with the command :
$ python Beautify.py
-Copy the file "output.tsv" and paste it in the folder "nla_semparse/data" (from the code cloned from the allennlp-guide repo)
-Copy the "seq2seq_config.json" file provided in the folder "nla_semparse/training_config"
-Finally, execute the command :
$ allennlp train training_config/seq2seq_config.json -s DEST_FOLDER --include-package allennlp_models --include-package nla_semparse
Replacing DEST_FOLDER by a folder of your choice
The generated model will be stored at this location under the name "model.tar.gz"

## Evaluate the model (chat with the bot)

Copy the "model.tar.gz" file to the folder containing ChiaccheraBot.py and execute :
$ python ChiaccheraBot.py


# TODO

-Change the way the model is being evaluated (not the best answer first everytime)

-Change the input from the user to match the lowercase, space-separated input from the input data

-Change the output of the network so that it matches the rules of the English languages

-Work a bit on the interface to make it prettier
