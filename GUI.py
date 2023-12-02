#Ryan Fleury
#Lawrence Tech University
#Senior Project Sprint 2022
#Emotion Predictive Text Editor
#"I have neither given nor received unauthorized aid in completing this 
# work, nor have I presented someone else's work as my own."


from tkinter import *
from tkinter import filedialog
#import text2emotion as te
#import nltk
from textblob import TextBlob
from APIRequests import GenFile
import docx

from emotion import buildKernal
from consts import FEATURE_NUMBER
from consts import init
import consts
filetypes = (
        ('text files', '*.txt'),
        ('Word Document', '*.docx'),
        ('All files', '*.*')
)
print(type(filetypes))

def open_txt(): #create open_txt(): function
  
    File = filedialog.askopenfilename(initialdir = "D:\vsCode\Code", title = "Open Files", filetypes = filetypes ) 
    
    try: #opening a text file
        textFile = open(File, 'r')
        data = textFile.read()
        my_text.insert(END, data)
        textFile.close()
    except: #opening a word file
        textFile = docx.Document(File)
        data = textFile.paragraphs
        for para in data:
            my_text.insert(END, para.text + "\n")

    #my_text.insert(END, data)
    #textFile.close()

def save_txt(): #create save_txt() function
    textFile = filedialog.asksaveasfilename(initialdir = "D:\vsCode\Code", title = "Open Text File", filetypes = filetypes )
    textFile = open(textFile, 'w')
    textFile.write(my_text.get(1.0, END))
    textFile.close()

def analize_text(): #create analize_text() function
    #--------------------sediment gathering and processing--------------------
    #=========================================================================================================================================================
    #get text from tkinter class
    roughSediment = my_text.get("1.0", END)
    #print(roughSediment)

    #-----break responce characters into list of words
    wordSediment = convert(roughSediment)
    #print("printing word level")
    #print(wordSediment)

    #remove first instance on reddit pull
    if (consts.redditBool == True):
        wordSediment.pop(0)#delete body, text
    
    #-----breaks responce into sentence level
    sentSediment = sentenceStruct(wordSediment)
    #print("print sentence sediment")
    #print(len(sentSediment))
    #print(sentSediment)
        
    if (consts.redditBool == True):
        #print("hello")
        #remove all entries that were less than two characters in length
        sentSediment = [x for x in sentSediment if len(x) >= 2]
        #removes numbers from reddit pull
        sentSediment = list(map(lambda x: x.replace("0,",'').replace("1,",'').replace("2,",'').replace("3,",'').replace("4,",'').replace("5,",'').replace("6,",'').replace("7,",'').replace("8,",'').replace("9,",'').replace("10,",''),sentSediment))

    #-----breaks responce into paragraph
    fullSediment = fullStructure(sentSediment)
    #print("aftwe full structure")
    #print(fullSediment)

    #-----cleans the gathered sedinent
    # finalSediment = listClense(sentSediment)
    # print("aftwe list clense")
    # print(finalSediment)
    #=========================================================================================================================================================



    # #--------------------Texb Blob documnet scoring--------------------
    # #=========================================================================================================================================================
    blob_text = TextBlob(fullSediment)
    #tags = blob_text.tags
    #print("Textblob tags")
    #print(tags)

    #polarity of the sediment (1 for negative 1 for positive)
    #sentiment = blob_text.sentiment 
    #print(sentiment)

    polarity = blob_text.polarity
    #print("Documnet polarity")
    #print(polarity)

    subjectivity = blob_text.subjectivity
    #print("Documnet subjectivity")
    #print(subjectivity)

    #semtence level postitive and negative feedback https://hackernoon.com/how-to-perform-emotion-detection-in-text-via-python-lk383tsu
    positive_feedbacks = []
    negative_feedbacks = []
    for feedback in sentSediment:
        feedback_polarity = TextBlob(feedback).sentiment.polarity
        if feedback_polarity>0:
            positive_feedbacks.append(feedback)
            continue
        negative_feedbacks.append(feedback)
  
    # print('Positive_feebacks Count : {}'.format(len(positive_feedbacks)))
    # #print(positive_feedbacks)
    # print('Negative_feedback Count : {}'.format(len(negative_feedbacks)))
    # # print(negative_feedbacks)

    polarity  = round(polarity, 5)
    subjectivity  = round(subjectivity, 5)
    stringNegative = 'Negative Feedbacks: ' + str(len(negative_feedbacks))
    stringPositive = 'Positive Feedbacks: ' + str(len(positive_feedbacks))
    stringPolarity = 'Polarity: ' + str(polarity)
    stringSubjectivity = 'Subjectivity: ' + str(subjectivity)

    #overwrite the labels for some document grading
    negativeLabel = Label(
    text=stringPositive,
    bg='#f0f0f0',
    font=(30)
    )
    negativeLabel.place(x = 1600, y =(52 + 220))

    positiveLabel = Label(
    text=stringNegative,
    bg='#f0f0f0',
    font=(30)
    )
    positiveLabel.place(x = 1600, y = (52 + 260))

    polarityLabel = Label(
    text=stringPolarity,
    bg='#f0f0f0',
    font=(30)
    )
    polarityLabel.place(x = 1600, y = (52 + 300))

    subjectivityLabel = Label(
    text=stringSubjectivity,
    bg='#f0f0f0',
    font=(30)
    )
    subjectivityLabel.place(x = 1600, y = (52 + 340))
    # #=========================================================================================================================================================



    # #--------------------text to emotion library-------------------- 
    # #=========================================================================================================================================================
    # textToEmotionVar = te.get_emotion(fullSediment)
    # print(textToEmotionVar)
        #NOT USED CURRENTLY IN PROJECT
    # #=========================================================================================================================================================

   

    # #--------------------SVM cutom emotion grading-------------------- 
    # #=========================================================================================================================================================
    clf = buildKernal()
    testVect = transformData(sentSediment)   
    prediction = clf.predict(testVect)
    #print(prediction)
    # #=========================================================================================================================================================
    


    # #--------------------clears the text box to to be rewritten-------------------- 
    # #=========================================================================================================================================================
    def clear_frame():
        my_text.delete('1.0', END)

    clear_frame()
    # #=========================================================================================================================================================



    # #--------------------rewrite the text to the screen with highlights-------------------- 
    # #=========================================================================================================================================================
    def write_frame():
        ins = 0
        #create text tags based on emotion
        my_text.tag_config("neutral", background= "white", foreground= "black")
        my_text.tag_config("non-neutral", background= "gray", foreground= "black")
        my_text.tag_config("fear", background= "pale violet red", foreground= "black")
        my_text.tag_config("disgust", background= "green yellow", foreground= "black")
        my_text.tag_config("surprise", background= "gold", foreground= "black")
        my_text.tag_config("joy", background= "spring green", foreground= "black")
        my_text.tag_config("anger", background= "maroon", foreground= "black")

        #sentSediment[ins] + "\n" to break higlights apart with a endline
        for entry in prediction:
            if(entry == "neutral"):
                my_text.insert(INSERT, sentSediment[ins] ,("neutral"),)
            elif(entry == "non-neutral"):
                my_text.insert(INSERT, sentSediment[ins] ,("non-neutral"),)
            elif(entry == "fear"):
                my_text.insert(INSERT, sentSediment[ins] ,("fear"),)
            elif(entry == "disgust"):
                my_text.insert(INSERT, sentSediment[ins] ,("disgust"),)
            elif(entry == "surprise"):
                my_text.insert(INSERT, sentSediment[ins] ,("surprise"),)
            elif(entry == "joy"):
                my_text.insert(INSERT, sentSediment[ins] ,("joy"),)
            elif(entry == "anger"):
                my_text.insert(INSERT, sentSediment[ins] ,("anger"),)
            else:
                my_text.insert(INSERT, sentSediment[ins] )
                
            ins = ins +1

    write_frame()
    # #=========================================================================================================================================================



#Extract the TfidfVectorizer features from the text that is in the text box
def transformData(sentenceData):
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorBoi = TfidfVectorizer(max_features=FEATURE_NUMBER, stop_words= "english")
        trainVext = vectorBoi.fit_transform(sentenceData) #transforming of training sentences
        return trainVext



#convert from list of string characters to list of words
def convert(s):
    # initialization of string to ""
    new = ""
    myList = []
    # traverse in the string 
    var = 0
    for x in s:
        if(s[var] == " " or s[var] == "\n"):
            myList.append(new)
            #print(new)
            new = ""
        
        new = new + x 
        var = var + 1; 
        
    # return string 
    return myList


#convert from list of words to list of sentences
def sentenceStruct(list):
    new = ""
    list2 = []
    for word in list:
        #print(word)
        if "." in word or "!" in word or "?" in word:
             new = new + word
             list2.append(new)
             new = "" 
        elif "\n" in word:
             list2.append(new)
             new = "" 
             word = word.replace("\n", "")
             new = new + word
        else:
            new = new + word

    list2.append(new)
        
    return list2


#convert from list of sentences to a paragraph form. aka one big string.
def fullStructure(list): 
    # initialize an empty string
    str1 = " " 
    # return string
    return (str1.join(list))
        

#cleans a list of all \n characters       
def listClense(list): 
    for x in list:
        if '\n' in x:
            x.replace("\n", "")


if __name__ == "__main__":

    init()#initilization function
    root = Tk() #tkinter object 
    root.title("Senior Project - Text Editor") #title of the window
    root.geometry("1920x1080")#size of window        

    #top button 1
    openTextButton = Button(root, text = "Open Text File", command = open_txt)
    openTextButton.place(x=0, y=0)
    # openTextButton.grid(row=1,column=0)

    #top button 2
    openSaveButton = Button(root, text = "Save File", command = save_txt)
    openSaveButton.place(x=86, y=0)
    # openSaveButton.grid(row=1,column=2)

    #top button 3
    analyzeButton = Button(root, text = "Analyze", command = analize_text)
    analyzeButton.place(x=143, y=0)
    # analyzeButton.grid(row=1,column=3)

    #top button 4
    RedditPullButton = Button(root, text = "Pull Reddit File", command = GenFile)
    RedditPullButton.place(x=195, y=0)
    # RedditPullButton.grid(row=1,column=4)


    #label for the text editor box
    frame = Label(
        text='Text Editor - Write Text or Open file for tone/emotion analysis',
        bg='#f0f0f0',
        font=(30)
    )
    frame.place(x = 70, y = 30)#place text box frame

    
    #create text editing box
    my_text = Text(root, width = 112, height= 38, font = ("Helventica", 18))
    my_text.place(x=70, y=52) #pady == vert didtance between elements
    #print(type(my_text))
    

    #add a scrollbar to text editing box
    scrollbar = Scrollbar(root)
    scrollbar.pack( side = RIGHT, fill = Y )
    scrollbar.config( command = my_text.yview )


    #A tabled that contains the emotion color grading legend
    fontSize =  30
    legend = Label(root,
    text="            Legend         ",
     fg= "black",font=(fontSize))
    legend.place(x = 1600, y = 52)

    neutraLabel = Label(root,
    text="  Neutral is White                ",
    bg= "white", fg= "black",font=(fontSize))
    neutraLabel.place(x = 1600, y = (52 + 25))

    nonNeutralLabel = Label(root,
    text="  Non-Neutral is Gray         ",
    bg= "gray", fg= "black",font=(fontSize))
    nonNeutralLabel.place(x = 1600, y = (52 + 48))

    fearLabel = Label(root,
    text="  Fear is Pink                      ",
    bg= "pale violet red", fg= "black",font=(fontSize))
    fearLabel.place(x = 1600, y = (52 + 72))

    disgustllLabel = Label(root,
    text="  Disgust is green yellow   ",
    bg= "green yellow", fg= "black",font=(fontSize))
    disgustllLabel.place(x = 1600, y = (52 + 96))

    surpriseLabel = Label(root,
    text="  Suprise is gold                 ",
    bg= "gold", fg= "black",font=(fontSize))
    surpriseLabel.place(x = 1600, y = (52 + 120))

    joyLabel = Label(root,
    text="  Joy is spring green          ",
    bg= "spring green", fg= "black",font=(fontSize))
    joyLabel.place(x = 1600, y = (52 + 144))

    angerLabel = Label(root,
    text= "  Anger is maroon              ",
    bg= "maroon", fg= "black",font=(30))
    angerLabel.place(x = 1600, y =(52 + 168))


    #placeholder labels string
    stringNegative = 'Negative Feedbacks: ' 
    stringPositive = 'Positive Feedbacks: ' 
    stringPolarity = 'Polarity: ' 
    stringSubjectivity = 'Subjectivity: '

    #placeholder labels apended to GUI
    negativeLabel = Label(
    text=stringPositive,
    bg='#f0f0f0',
    font=(30)
    )
    negativeLabel.place(x = 1600, y =(52 + 220))

    positiveLabel = Label(
    text=stringNegative,
    bg='#f0f0f0',
    font=(30)
    )
    positiveLabel.place(x = 1600, y = (52 + 260))

    polarityLabel = Label(
    text=stringPolarity,
    bg='#f0f0f0',
    font=(30)
    )
    polarityLabel.place(x = 1600, y = (52 + 300))

    subjectivityLabel = Label(
    text=stringSubjectivity,
    bg='#f0f0f0',
    font=(30)
    )
    subjectivityLabel.place(x = 1600, y = (52 + 340))

    root.mainloop()