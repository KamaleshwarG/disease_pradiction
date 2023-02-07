import json
from tkinter import *
from tkinter import messagebox
import numpy as np
import pandas as pd
import tkinter.scrolledtext as st
import tkinter as tk
from pymongo import MongoClient
from bson.objectid import ObjectId 
#mongodb connection establishment
client = MongoClient('mongodb://localhost:27017')

db = client.get_database('diseasepredict')

data = db.data
records= db.history
users = db.users
test = db.Testing
train = db.Training

idOne = "63d29cac0b09b54f74fc931e"
symQuerry = {"_id":ObjectId(idOne)}

idTwo = "63d29dd10b09b54f74fc931f"
disQuerry = {"_id":ObjectId(idTwo)}

def disease_p(usernam):

    symtoms = data.find(symQuerry)

    diseaseFetch = data.find(disQuerry)

    l1 = symtoms[0]["symtoms"]

    disease =   diseaseFetch[0]["disease"]

    testing = test.find({},{"_id":0})
    # print(testing)
    training =  train.find({},{"_id":0})
    # print(training)
    l2=[]
    for x in range(0,len(l1)):
        l2.append(0)
    # print(l1)
    # print(l2)
    tr=pd.DataFrame(testing)
    # print(tr)
    tr.replace({'prognosis':{'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
    'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
    'Migraine':11,'Cervical spondylosis':12,
    'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
    'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
    'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
    'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
    '(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
    'Impetigo':40}},inplace=True)

    X_test= tr[l1]
    y_test = tr[["prognosis"]]
    np.ravel(y_test)

    df=pd.DataFrame(training)

    df.replace({'prognosis':{'Fungal infection':0,'Allergy':1,'GERD':2,'Chronic cholestasis':3,'Drug Reaction':4,
    'Peptic ulcer diseae':5,'AIDS':6,'Diabetes ':7,'Gastroenteritis':8,'Bronchial Asthma':9,'Hypertension ':10,
    'Migraine':11,'Cervical spondylosis':12,
    'Paralysis (brain hemorrhage)':13,'Jaundice':14,'Malaria':15,'Chicken pox':16,'Dengue':17,'Typhoid':18,'hepatitis A':19,
    'Hepatitis B':20,'Hepatitis C':21,'Hepatitis D':22,'Hepatitis E':23,'Alcoholic hepatitis':24,'Tuberculosis':25,
    'Common Cold':26,'Pneumonia':27,'Dimorphic hemmorhoids(piles)':28,'Heart attack':29,'Varicose veins':30,'Hypothyroidism':31,
    'Hyperthyroidism':32,'Hypoglycemia':33,'Osteoarthristis':34,'Arthritis':35,
    '(vertigo) Paroymsal  Positional Vertigo':36,'Acne':37,'Urinary tract infection':38,'Psoriasis':39,
    'Impetigo':40}},inplace=True)

    X= df[l1]

    y = df[["prognosis"]]
    np.ravel(y)

    def message():
        if (Symptom1.get() == "None" and  Symptom2.get() == "None" and Symptom3.get() == "None" and Symptom4.get() == "None" and Symptom5.get() == "None"):
            messagebox.showinfo("OPPS!!", "ENTER  SYMPTOMS PLEASE")
        else :
            NaiveBayes()

    def NaiveBayes():
        from sklearn.naive_bayes import MultinomialNB
        gnb = MultinomialNB()
        gnb=gnb.fit(X,np.ravel(y))
        from sklearn.metrics import accuracy_score
        y_pred = gnb.predict(X_test)

        psymptoms = [Symptom1.get(),Symptom2.get(),Symptom3.get(),Symptom4.get(),Symptom5.get()]

        for k in range(0,len(l1)):
            for z in psymptoms:
                if(z==l1[k]):
                    l2[k]=1

        inputtest = [l2]
        predict = gnb.predict(inputtest)
        predicted=predict[0]

        h='no'
        for a in range(0,len(disease)):
            if(disease[predicted] == disease[a]):
                psymptoms = {
                 'name':usernam,
                 'Symptom1':Symptom1.get(),
                 'Symptom2':Symptom2.get(),
                 'Symptom3':Symptom3.get(),
                 'Symptom4':Symptom4.get(),
                 'Symptom5':Symptom5.get(),
                 'Disease': disease[predicted],
                }
                records.insert_one(psymptoms)
                if ((Symptom1.get()=="high_fever" or Symptom2.get()=="high_fever" or Symptom3.get()=="high_fever" or Symptom4.get()=="high_fever" or Symptom5.get()=="high_fever") and (Symptom1.get()=="cough" or Symptom2.get()=="cough" or Symptom3.get()=="cough" or Symptom4.get()=="cough" or Symptom5.get()=="cough") and (Symptom1.get()=="breathlessness" or Symptom2.get()=="breathlessness" or Symptom3.get()=="breathlessness" or Symptom5.get()=="breathlessness")):
                    disease[predicted]="corona"
                h='yes'
                break

        if (h=='yes'):
            t3.delete("1.0", END)
            t3.insert(END, disease[a])
        else:
            t3.delete("1.0", END)
            t3.insert(END, "No Disease")
    
    def history():
     
        newWindow = Toplevel(root)
 
        newWindow.title("History")
 
        newWindow.geometry("500x500")
 
        text_area = st.ScrolledText(newWindow,
                            width = 45, 
                            height = 20, 
                            font = ("Times New Roman",
                                    15))
  
        text_area.grid(column = 0, pady = 10, padx = 10)

        s = records.find({"name":usernam})

        j = ""

        for i in s:
            j += i["Symptom1"]+" "+i["Symptom2"]+" "+i["Symptom3"]+" "+i["Symptom4"]+" "+i["Symptom5"]+" "+i["Disease"]+"\n\n"
        
        text_area.insert(tk.INSERT,j)
        
        text_area.configure(state ='disabled')

#prediction ui
    root = Toplevel()
    root.title(" Disease Prediction From Symptoms")
    root.geometry('5000x1500')
    my = Label(root,bg= "#88cffa")
    my.place(x=0,y=0,relwidth=1, relheight=1)
    Symptom1 = StringVar()
    Symptom1.set(None)
    Symptom2 = StringVar()
    Symptom2.set(None)
    Symptom3 = StringVar()
    Symptom3.set(None)
    Symptom4 = StringVar()
    Symptom4.set(None)
    Symptom5 = StringVar()
    Symptom5.set(None)

    w2 = Label(root, justify=LEFT, text=" Disease Prediction From Symptoms ",bg= "#88cffa")
    w2.config(font=("Courier", 30))
    w2.place(x=320,y=0)

    '''label = Label(root, text="DISEASE PREDICTION FROM SYMPTOMS",font=("Times", "28", "bold"),fg="white",bg="#5489dd",height=2)
    label.place(x=250,y=0)'''

    NameLb1 = Label(root, text="")
    NameLb1.config(font=("Courier", 20))
    NameLb1.grid(row=5, column=2, pady=10,  sticky=W)

    S1Lb = Label(root,  text="SYMPTOM 1",bg= "#88cffa")
    S1Lb.config(font=("Courier", 20))
    S1Lb.place(x=400,y=150)

    S2Lb = Label(root,  text="SYMPTOM 2",bg= "#88cffa")
    S2Lb.config(font=("Courier", 20))

    S2Lb.place(x=400,y=210)

    S3Lb = Label(root,  text="SYMPTOM 3",bg= "#88cffa")
    S3Lb.config(font=("Courier", 20))
    S3Lb.place(x=400,y=270)

    S4Lb = Label(root,  text="SYMPTOM 4",bg= "#88cffa")
    S4Lb.config(font=("Courier", 20))
    S4Lb.place(x=400,y=330)

    S5Lb = Label(root,  text="SYMPTOM 5",bg= "#88cffa")
    S5Lb.config(font=("Courier", 20))
    #S5Lb.grid(row=14, column=1, pady=10, sticky=W)
    S5Lb.place(x=400,y=390)

    lr = Button(root, text="PREDICT",height=2, width=20, command=message)
    lr.config(font=("Courier", 15))
    #lr.grid(row=17, column=2,pady=20)
    lr.place(x= 550,y=450)

    historybutton = Button(root, text="See History",height=1, width=15, command=history)
    historybutton.config(font=("Courier", 15))
    #lr.grid(row=17, column=2,pady=20)
    historybutton.place(x= 5,y=5)

    OPTIONS = sorted(l1)

    S1En = OptionMenu(root, Symptom1,*OPTIONS)
    #S1En.grid(row=10, column=2)
    S1En.place(x=900,y=150)


    S2En = OptionMenu(root, Symptom2,*OPTIONS)
    #S2En.grid(row=11, column=2)
    S2En.place(x=900,y=210)

    S3En = OptionMenu(root, Symptom3,*OPTIONS)
    #S3En.grid(row=12, column=2)
    S3En.place(x=900,y=270)

    S4En = OptionMenu(root, Symptom4,*OPTIONS)
    #S4En.grid(row=13, column=2)
    S4En.place(x=900,y=330)

    S5En = OptionMenu(root, Symptom5,*OPTIONS)
    #S5En.grid(row=14, column=2)
    S5En.place(x=900,y=390)

    '''NameLb = Label(root, text="")
    NameLb.config(font=("Elephant", 20))
    NameLb.grid(row=13, column=1, pady=10,  sticky=W)

    NameLb = Label(root, text="")
    NameLb.config(font=("Elephant", 15))
    NameLb.grid(row=18, column=1, pady=10,  sticky=W)'''

    t3 = Text(root, height=2, width=30)
    t3.config(font=("Elephant", 20))
    t3.grid(row=22, column=2 , padx=10)
    t3.place(x= 400,y=550)
    root.mainloop()
#click listener
def signup():
    database = []
    for i in users.find({}):
        my_dict = {
        'name': i['name'],
        'password' : i['password']
        }
        database.append(my_dict)
    #print(len(database))
    f=0
    for i in range(len(database)):
        if (username.get() == database[i]['name'] and password.get() == database[i]['password']):
            f=1
            disease_p(username.get())
            break
        else:
            continue
    if f==0:
        new_user = {'name': username.get(), 'password':password.get()}
        users.insert_one(new_user)
        messagebox.showinfo("registered")
    myquery = { "name": username.get(),"password":password.get() }
    print(username.get())
    print(password.get())

    mydoc = users.find(myquery)

    for x in mydoc:
        print(x)
#login module
tkWindow = Tk()  
tkWindow.geometry('5000x1500')  
tkWindow.title('disease prediction.org')

my = Label(tkWindow,bg="#88cffa")
my.place(x=0,y=0,relwidth=1, relheight=1)

predictLabel = Label(tkWindow, text="DISEASE PREDICTION SYSTEM",bg="#88cffa",font=("Courier", 35)).place(x=330, y=150)

usernameLabel = Label(tkWindow, text="User Name",bg="#88cffa",font=("Courier", 20)).place(x=450, y=300)
username = StringVar()
usernameEntry = Entry(tkWindow, textvariable=username,width=20,font=("Courier", 20)).place(x=630, y=300)  

passwordLabel = Label(tkWindow,text="Password",bg="#88cffa",font=("Courier", 20)).place(x=450, y=360)  
password = StringVar()
passwordEntry = Entry(tkWindow, textvariable=password, show='*',width=20,font=("Courier", 20)).place(x=630, y=360)  

signupButton = Button(tkWindow, text="Sign up", command=signup,font=("Courier", 15)).place(x=630, y=420)
loginButton = Button(tkWindow, text="Login", command=signup,font=("Courier", 15)).place(x=750, y=420)

tkWindow.mainloop()
