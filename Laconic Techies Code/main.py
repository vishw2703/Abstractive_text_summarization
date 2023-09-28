# from crypt import methods
from operator import methodcaller
from pydoc_data.topics import topics
from turtle import title
from pprint import pprint
from webbrowser import get
import requests
import urllib.parse as urlparse
from importlib.resources import contents
from bs4 import BeautifulSoup
from pprint import pprint
import requests_html
from posixpath import split
from cgitb import text
from os import link
from traceback import print_tb
from newspaper import Article
from flask_cors import CORS
from flask import Flask, render_template, request, url_for, redirect
import googletrans
from googletrans import *
from flask_cors import cross_origin
from summary import article_summary
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import PyPDF2 
from summary import article_summary
import os
from docx import Document


translator = googletrans.Translator()
language_detection=Translator()
website_links_at_last=[]
text_web_list=[]
input_by_user=""
A=[]
detc=''
app = Flask(__name__)

a=''
v=''
b=''


@app.route('/')
def home():
    from movingtitle import scroll_news
    global A
    titles_for_scroll_on_page=scroll_news()

    A=[]

    for i in range(10):
        title_scr=titles_for_scroll_on_page[i]
        A.append(title_scr)

    return render_template('index.html',A1=A[1],A2=A[2],A3=A[3],A4=A[4],A5=A[5],A6=A[6],A7=A[7],A8=A[8],A9=A[9],A10=A[0])


app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")



@app.route('/upload', methods=['GET',"POST"])
def upload():
    global A
    form = UploadFileForm()
    if form.validate_on_submit():

        global b
        file = form.file.data # First grab the file

        z=str(file)

        a=z.replace("<FileStorage: ","")
        b=a.replace(" ('application/pdf')>","")

        print(b)

        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        return render_template('button.html',A=A)
    

    return render_template("upload.html", form=form, A=A)



@app.route('/summary')
def summary():
    global bs
    global A

    W_commas=b.replace("'","")

    file_location=("static/files/"+W_commas)

    print(file_location)

    from re import search

    str=file_location

    if search(".pdf", str):
        pdfFileObj = open(file_location, 'rb')

        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        number_of_pages = pdfReader.getNumPages()

        pageObj = pdfReader.getPage(0)

        data=(pageObj.extractText())

        print(data)

        data_string=data

        word_count_file=len(data_string.split())

        pdfFileObj.close()

        summary_of_file=article_summary(data)

        Summary_string=summary_of_file

        word_count_summary=len(Summary_string.split())

        

        return render_template("summaryfile.html", summary_of_file=summary_of_file, A=A,word_count_file=word_count_file,word_count_summary=word_count_summary)

    elif search(".docx", str):

        # 'static/files/data.docx (application/vnd.openxmlformats-officedocument.wordprocessingml.document)>'

        docx_loc=file_location.replace(" (application/vnd.openxmlformats-officedocument.wordprocessingml.document)>","")

        path_to_file=docx_loc
        
        #Creating a word file object
        doc_object = open(path_to_file, "rb")

        #creating word reader object
        doc_reader = Document(doc_object)
        data = ""

        for p in doc_reader.paragraphs:
            data += p.text+"\n"

        print(data)

        data_string=data

        word_count_file=len(data_string.split())

        summary_of_file=article_summary(data)

        Summary_string=summary_of_file

        word_count_summary=len(Summary_string.split())
          

        return render_template("summaryfile.html", summary_of_file=summary_of_file, A=A,word_count_file=word_count_file,word_count_summary=word_count_summary)

        

    elif search(".txt", str):

        # 'data.txt' ('text/plain')>

        txt_location=file_location.replace(" (text/plain)>","")

        # print(txt_location)

        file_location_txt=txt_location

        f=open(file_location_txt,'r')

        with open(txt_location) as f:
            data = f.read()
            # print(contents)

        print(data)
        data_string=data

        word_count_file=len(data_string.split())

        summary_of_file=article_summary(data)

        Summary_string=summary_of_file

        word_count_summary=len(Summary_string.split())


        return render_template("summaryfile.html", summary_of_file=summary_of_file, A=A,word_count_file=word_count_file,word_count_summary=word_count_summary)


    else:
        
        return "<h1>Please enter a pdf file</h1>"


    os.remove(file_location_txt)

@app.route('/link')
def link():
    global A
    return render_template("link.html",A=A)

@app.route('/sumlink',methods=["POST"])
def sumlink():
    global A
    from link import get_text_article

    web_link=request.form.get("link")

    link_data=get_text_article(web_link)

    from summary import article_summary

    link_summary=article_summary(link_data)

    return render_template("sumlink.html",link_summary=link_summary,A=A)




input_text=""

@app.route('/text')
def text():
    global A
   
    return render_template("text.html",A=A)

@app.route('/sumarizing',methods=["POST"])
def sumarizing():
    global input_text
    global A

    input_text=request.form.get("text_user")

    data_string=str(input_by_user)

    word_count_file=len(data_string.split())

    text_summary=article_summary(input_text)

    Summary_string=text_summary

    word_count_summary=len(Summary_string.split())



    return render_template("text_2.html",text_summary=text_summary, A=A,word_count_file=word_count_file,word_count_summary=word_count_summary)





@app.route('/topic')
def topic():

    global A

    return render_template('topic.html',A=A)


@app.route('/title', methods=["POST"])
def title():
    from title_of_web import title_for_second
    
    global detc
    global input_by_user
    global text_web_list
    global website_links_at_last
    global A
    
    input_by_user = request.form.get("input_by_user")
    print(input_by_user)
    

    a=title_for_second(input_by_user)
    
    title_web1=a[0] 
    t1=title_web1
    

    title_web2=a[1]
    t2=title_web2

    title_web3=a[2]
    t3=title_web3
    
    title_web4=a[3]
    t4=title_web4

    title_web5=a[4]
    t5=title_web5

    title_web6=a[5]
    t6=title_web6

    title_web7=a[6]
    t7=title_web7

    title_web8=a[7]
    t8=title_web8

    title_web9=a[8]
    t9=title_web9

    title_web10=a[9]
    t10=title_web10
    

    text_web_list=[]
    for i in range(10,20):
        text_web_list.append(a[i])

    website_links_at_last=[]
    for i in range(20,30):
        website_links_at_last.append(a[i])
    
    
    
    return render_template("title.html",title_web1=t1,title_web2=t2,title_web3=t3,title_web4=t4,title_web5=t5,title_web6=t6,title_web7=t7,title_web8=t8,title_web9=t9,title_web10=t10, A=A)


@app.route('/first')
def first():
    from summary import article_summary
    
    global A
    global website_links_at_last
    
    global text_web_list

    article_summary_1=article_summary(text_web_list[0])

    s1=article_summary_1

    return render_template("first.html", article_summary_1=s1,web_link1=website_links_at_last[0], A=A)


@app.route('/second')
def second():
    from summary import article_summary

    global A
    
    global text_web_list

    article_summary_2=article_summary(text_web_list[1])


    s2=article_summary_2


    return render_template("second.html", article_summary_2=s2,web_link2=website_links_at_last[1], A=A)
    #article_summary_1=article_summary_1,article_summary_2=article_summary_2,article_summary_3=article_summary_3,article_summary_4=article_summary_4,article_summary_5=article_summary_5,article_summary_6=article_summary_6,article_summary_7=article_summary_7,article_summary_8=article_summary_8,article_summary_9=article_summary_9,article_summary_10=article_summary_10)

@app.route('/third')
def third():
    from summary import article_summary
    
    global A

    global text_web_list

    article_summary_3=article_summary(text_web_list[2])

    s3=article_summary_3

    return render_template("third.html", article_summary_3=s3,web_link3=website_links_at_last[2], A=A)

@app.route('/fourth')
def fourth():
    from summary import article_summary
    
    global A

    global text_web_list

    article_summary_4=article_summary(text_web_list[3])

    s4=article_summary_4

    return render_template("fourth.html", article_summary_4=s4,web_link4=website_links_at_last[3], A=A)
   

@app.route('/fifth')
def fifth():
    from summary import article_summary
    
    global A

    global text_web_list

    article_summary_5=article_summary(text_web_list[4])

    s5=article_summary_5

    return render_template("fifth.html", article_summary_5=s5,web_link5=website_links_at_last[4], A=A)

@app.route('/sixth')
def sixth():
    from summary import article_summary
    
    global A

    global text_web_list

    article_summary_6=article_summary(text_web_list[5])

    s6=article_summary_6

    return render_template("sixth.html", article_summary_6=s6,web_link6=website_links_at_last[5], A=A)
    

@app.route('/seventh')
def seventh():
    from summary import article_summary
    
    global A

    global text_web_list

    article_summary_7=article_summary(text_web_list[6])

    s7=article_summary_7
    
    return render_template("seventh.html", article_summary_7=s7,web_link7=website_links_at_last[6], A=A)
    

@app.route('/eighth')
def eighth():
    from summary import article_summary
    
    global A

    global text_web_list

    article_summary_8=article_summary(text_web_list[7])

    s8=article_summary_8
    

    return render_template("eighth.html", article_summary_8=s8,web_link8=website_links_at_last[7], A=A)
   

@app.route('/ninth')
def ninth():
    from summary import article_summary
    
    global A

    global text_web_list

    article_summary_9=article_summary(text_web_list[8])
    s9=article_summary_9

    return render_template("ninth.html", article_summary_9=s9,web_link9=website_links_at_last[8], A=A)
    

@app.route('/tenth')
def tenth():
    from summary import article_summary
    
    global A

    global text_web_list

    article_summary_10=article_summary(text_web_list[9])

    s9=article_summary_10

    return render_template("tenth.html", article_summary_10=s9,web_link10=website_links_at_last[9], A=A)

@app.route('/weblink1')
def weblink1():
    return redirect(website_links_at_last[0])

@app.route('/weblink2')
def weblink2():
    return redirect(website_links_at_last[1])
    

@app.route('/weblink3')
def weblink3():
    return redirect(website_links_at_last[2])

@app.route('/weblink4')
def weblink4():
    return redirect(website_links_at_last[3])

@app.route('/weblink5')
def weblink5():
    return redirect(website_links_at_last[4])

@app.route('/weblink6')
def weblink6():
    return redirect(website_links_at_last[5])

@app.route('/weblink7')
def weblink7():
    return redirect(website_links_at_last[6])

@app.route('/weblink8')
def weblink8():
    return redirect(website_links_at_last[7])

@app.route('/weblink9')
def weblink9():
    return redirect(website_links_at_last[8])

@app.route('/weblink10')
def weblink10():
    return redirect(website_links_at_last[9])




if __name__ == "__main__":
        app.run(debug=True)