from decimal import *
import numpy as np

def main():
    dictionary={}
    object = open("POSTaggedTrainingSet-Unix.txt","r")
    str = object.readlines()

    file1 = open("file1.txt", 'w')
    file1.truncate()
    for eachline in str:
        for word in eachline.split():
            parts=word.split("_")

            #write to new file
            file1.write(parts[0]+ " ")

            if len(parts)==2:
                if parts[0] in dictionary.keys():
                    if parts[1] in dictionary[parts[0]].keys():
                        dictionary[parts[0]][parts[1]] += 1
                    else:
                        dictionary[parts[0]][parts[1]] = 1
                else:
                    dictionary[parts[0]] = {}
                    dictionary[parts[0]][parts[1]] = 1
        file1.write("\n")

    file1.close()

    #print "####################################"
    #filter top tag
    for anyword in dictionary.keys():
        max_count = 0
        max_pos = ""
        #print anyword, " - ",
        for pos in dictionary[anyword].keys():
            temp_count = dictionary[anyword].pop(pos)
            if(temp_count > max_count):
                max_count = temp_count
                max_pos = pos
        dictionary[anyword][max_pos] = max_count
        #print max_pos," : ",dictionary[anyword][max_pos]
        #print "\n"

    return dictionary
#new file which contains word with the tag which appearied maximum number of times in the corpus.
def new_tag_file(dictionary):

    object = open("file1.txt","r")
    str = object.readlines()

    file1 = open("file2.txt", 'w')
    file1.truncate()

    for eachline in str:
        for word in eachline.split():
            #create new tagged file
            #print dictionary[word].items()
            for key, value in dictionary[word].items():
                file1.write(word + "_" + key + " ")
        file1.write("\n")

    file1.close()

def compute_error_rate(org_file,new_tag_file):
    old_file_ob = open(org_file,"r")
    file1_ob = open(new_tag_file, "r")
    lines_file1 = old_file_ob.readlines()
    lines_file2 = file1_ob.readlines()

    error_dict= {}
    word_count = 0
    error_count = 0
    for line1, line2 in zip(lines_file1, lines_file2):
        wordlist1 = line1.split()
        wordlist2 = line2.split()

        for word1, word2 in zip(wordlist1, wordlist2):
            word_count += 1
            word1_word = word1.split("_")[0]

            if(word1_word=="'s"):
                continue

            word2_word = word2.split("_")[0]
            word1_pos = word1.split("_")[1]
            word2_pos = word2.split("_")[1]
            if(word1_word == word2_word):

                if(word1_pos != word2_pos):
                    error_count += 1
                    if word1_word in error_dict.keys():
                        error_dict[word1_word]['error_count'] += 1
                        error_dict[word1_word]['total_count'] += 1
                    else:
                        error_dict[word1_word] = {'error_count':1, 'total_count':1, 'rev_error_count':0}
                else: #if POS is same but it was wrong once.......i.e part of the error_dict.
                    if word1_word in error_dict.keys():
                        error_dict[word1_word]['total_count'] += 1

    #getcontext().prec = 3
    #print "word_count : ",word_count," error_count : ",error_count
    #print "error_rate : ",(Decimal(error_count)/word_count)*100,"%"


    #for name, score in sorted(error_dict.iteritems(), key=lambda (k, v): (-v, k))[:5]:
    #    print name, score

    error_list=[]
    error_list1=[]
    for key in sorted(error_dict, key=lambda x: error_dict[x]['error_count'], reverse=True)[:5]:
        error_list.append([key, error_dict[key]['error_count'], error_dict[key]['total_count'], error_dict[key]['rev_error_count']])
        error_list1.append([key, 100.0*error_dict[key]['error_count']/error_dict[key]['total_count']])#, error_dict[key]['rev_error_count']])

    print "The words with the top 5 errornous words w.r.t POS are as below with %::"
    print np.array(error_list1)#[:, 0]
    return error_list

def retag_file(dictionary):
    object = open("POSTaggedTrainingSet-Unix.txt", "r")
    str = object.readlines()

    file1 = open("file3.txt", 'w')
    file1.truncate()

    print "\n" "Rules to change the errornous words above::"
    print "WORD\t\tTAG\t\tPREVIOUS TAG"
    print "that\t\tDT\t\tIN"
    print "-\t\tWDT\t\tNN/NNS/NNP"
    print "have\t\tVB\t\tMD"
    print "more\t\tRBR\t\tVBD/CC/NN"
    print "plans\t\tNNS\t\tNN/IN"
    print "up\t\tRB\t\tNN/IN"
    print "-\t\tIN\t\tVBN/VBD/VBG/VBP\n"

    for eachline in str:
        line_start_flag = 0
        prev_word_pos = ""

        for word in eachline.split():
            parts = word.split("_")
            if(line_start_flag == 0 ):
                prev_word_pos = parts[1]
                line_start_flag = 1
                if(parts[0] == "That"):
                    file1.write(parts[0] + "_" + "DT" + " ")
                else:
                    file1.write(word + " ")
                continue

            #new rules
            if(parts[0] == "that"):
                if(prev_word_pos == "IN"):
                    file1.write(parts[0] + "_" + "DT" + " ")
                if (prev_word_pos in ('NN' ,'NNS', 'NNP')):
                    file1.write(parts[0] + "_" + "WDT" + " ")
            else:
                if (parts[0] == "have"):
                    if (prev_word_pos == "MD"):
                        file1.write(parts[0] + "_" + "VB" + " ")
                else:
                    if (parts[0] == "more"):
                        if (prev_word_pos in ('VBD','CC','NN')):
                            file1.write(parts[0] + "_" + "RBR" + " ")
                    else:
                        if (parts[0] == "plans"):
                            if (prev_word_pos in ('IN','NN')):
                                file1.write(parts[0] + "_" + "NNS" + " ")
                        else:
                            if (parts[0] == "up"):
                                if (prev_word_pos in ('IN', 'NN')):
                                    file1.write(parts[0] + "_" + "RB" + " ")
                                if (prev_word_pos in ('VBN','VBD','VBG','VBP')):
                                    file1.write(parts[0] + "_" + "IN" + " ")
                            else:
                                for key, value in dictionary[parts[0]].items():
                                    file1.write(parts[0] + "_" + key + " ")

            prev_word_pos = parts[1]

        file1.write("\n")
    file1.close()

def recompute_error_rate(org_file, final_tagged_file, error_list):
    old_file_ob = open(org_file, "r")
    file1_ob = open(final_tagged_file, "r")
    lines_file1 = old_file_ob.readlines()
    lines_file2 = file1_ob.readlines()

    for line1, line2 in zip(lines_file1, lines_file2):
        wordlist1 = line1.split()
        wordlist2 = line2.split()

        for word1, word2 in zip(wordlist1, wordlist2):
            word1_word = word1.split("_")[0]

            if(word1_word in ('that','have','more','plans','up')):
                word2_word = word2.split("_")[0]
                word1_pos = word1.split("_")[1]
                word2_pos = word2.split("_")[1]

                #find word in top 5 table

                if (word1_word == word2_word):
                    if (word1_pos != word2_pos):
                        index = [index for index, row in enumerate(error_list) if word1_word in row]
                        #print row in enumerate(error_list)
                        error_list[index[0]][3] += 1

    return error_list

def print_error_list(error_list):
    print "Revised_Error_Rate is Error after Most Probable assigning POS and applying rules.\n"
    print "Word\tTotal_count\tError_count\tError_Rate(%)\tRevised_Error_count\tRevised_Error_Rate(%)\tReduction_Err_Rates"
    getcontext().prec = 3
    for row in range(0, error_list.__len__()):
        old_error_rate = (Decimal(error_list[row][1])/error_list[row][2])*100
        new_error_rate = (Decimal(error_list[row][3])/error_list[row][2])*100
        print error_list[row][0],"\t",error_list[row][2],"\t\t",error_list[row][1],"\t\t",old_error_rate,"\t\t",error_list[row][3],"\t\t\t",new_error_rate,"\t\t\t", old_error_rate - new_error_rate

if __name__ == "__main__":
    dictionary = main()
    new_tag_file(dictionary)
    error_list = compute_error_rate("POSTaggedTrainingSet-Unix.txt","file2.txt")
    retag_file(dictionary)
    error_list = recompute_error_rate("POSTaggedTrainingSet-Unix.txt", "file3.txt", error_list)
    print_error_list(error_list)
