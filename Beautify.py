from swda import CorpusReader
import os
import re

clean_folder = "NEW_CLEAN_FILES"
file_output = "output.tsv"

corpus = CorpusReader("swda")

a = corpus.iter_transcripts()

nb_files = 0

#########
MAX_FILES = 50 # total number of transcripts being parsed before stopping
#########

new_path = new_path = os.path.join(clean_folder, file_output)
file = open(new_path, "w") # open the final file


for script in a:

	nb_files += 1

	filename = os.path.split(script.swda_filename)[-1]
	
	print(" NEW FILE ", filename)

	old_caller = None
	is_sentence_finished = True
	is_sentence_continue = False
	is_new_caller = False
	sentence_waiting = ""  # contains the part of the sentence not finished


	full_text = []  # list containing all the sentences that will be written 
	current_sentence = "" # current sentence being treated
	
	for utt in script.utterances:

		if old_caller is None:
			old_caller = utt.caller
			current_sentence += ""

		data = utt.text

		# remove everything between "<" and ">"
		data = re.sub(r"[ <]?<[^<]*>", "", data)

		# remove the "()" and keep the letters inside
		data = re.sub(r"\(\((?P<A>[a-zA-Z -}{]+)\)\)", "\\g<A>", data)

		# remove the end "/"
		data = data.replace("/", "")

		# remove the "#"
		data = data.replace("#", "")

		# remove the "{}" and keep the letter inside
		data = re.sub(r"({[FCDE] (?P<OK>[a-zA-Z .,]*,?) })", "\\g<OK>", data)

		# sentence was interrupted, now is finishing
		if data[0:2] == "--":
			is_sentence_continue = True;
		else:
			is_sentence_continue = False  # FIXME maybe put this at the beginning of the loop...

		# sentence is interrupted
		if "--" in data[-3:]:
			is_sentence_finished = False
			sentence_waiting = data.replace("--", "")  # saving the sentence not finished
		else:
			is_sentence_finished = True


		# remove the "--""
		data = data.replace("--", "")


		if (old_caller != utt.caller):
			is_new_caller = True
		else:
			is_new_caller = False


		if is_sentence_continue:
			is_sentence_continue = False
			current_sentence += sentence_waiting # maybe it is not the best spot to put this ?


		# write only if the sentence is finished
		if is_sentence_finished:
			if len(data) > 3:
				if is_new_caller:
					full_text.append(current_sentence)  # newline
					current_sentence = ""
					# current_sentence += utt.caller+" "  # caller letter
					old_caller = utt.caller

				current_sentence += data


	for a in range(len(full_text)):

		data = full_text[a]

		# remove the "[]" and keep only the second part
		# do it two times to get rid of "[[]]"
		for _ in range(2):
			data = re.sub(r"\[(?P<A>([a-zA-Z]| |,|-|')*) \+ (?P<B>([a-zA-Z]| |,|-|')*)\]", "\\g<B>", data)


		# WHAT IF THERE ARE STILL "[ + ]"
		data = data.replace("[", "")
		data = data.replace("]", "")
		data = data.replace("+", "... ")

		# replace every "-" at the end of a sentence by a "..."
		data = re.sub(r"-$", "...", data)

		# replace every "," at the end of a sentence by a "."
		data = re.sub(r",$", ".", data)

		data = data.strip() # remove any space at the beginning/end

		# replace every caracter (not ?!.) at the end of a sentence by itself + "."
		data = re.sub(r"(?P<A>[^\.\?!])$", "\\g<A>.", data)

		# replace every " - " by a blank
		data = data.replace(" - ", " ")
		
		# replace every ", ..." by "..."
		data = re.sub(r", \.\.\.", "...", data)

		# replace every ",." by "."
		data = re.sub(r",\.", ".", data)

		# replace every "-." by a "."
		data = data.replace("-.", ".")

		# Make all the first words after a ". " to be capitalized
		data = re.sub(r"(?P<A>\. [a-z])", lambda x: x.group().upper(), data) 

		# delete all the more-than-one spaces
		data = re.sub(r"[ ]{2,}", " ", data)

		full_text[a] = data

	
	for a in range(len(full_text)):
		# write each sentence with its answer in the output file
		if a != 0:
			to_write = full_text[a-1] + "\t" + full_text[a] + "\n"
			file.write(to_write)

	
	if nb_files == MAX_FILES: # parse a limited amount of file
		break
	

file.close() # close the file
