from sqlite3 import Timestamp
from turtle import title
from types import NoneType
from django.shortcuts import render
from django.http import HttpResponse as hr
from .models import File,Element
import csv
import glob
import pandas as pd
import mimetypes
import os
path=r'D:\Vs code\Web Development Back-end\django\internship_question\practic\media'
file=glob.glob
def data_store():
    file=glob.glob(path + "/*.csv")
    print(type(file))
    data=pd.read_csv(file[0])
    print(len(data.index))
    image_name=data['image_name'].tolist()
    objects_detected=data["objects_detected"].tolist()
    time_stamp=data["timestamp"].tolist()
    for i in range(0,len(image_name)):
        time=time_stamp[i];
        Element(image_name=image_name[i],objects_detected=objects_detected[i],timestamp=time_stamp[i]).save();
    print("done");
def index(request):
    myfile=request.FILES.get("file")
    dic={
           "mes": "File added"
        }
    filename=request.POST.get("download","")
    if type(myfile)!=NoneType:
        File(file_name=myfile).save()
        data_store()
        return render(request,"index.html",dic)
    if filename != '':
        try:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filepath = BASE_DIR + '\\Files\\' + 'report.csv'
            path = open(filepath, 'rb')
            mime_type, _ = mimetypes.guess_type(filepath)
            response = hr(path, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % "report.csv"
            return response
        except:
            return render("index.html")
    delete=request.POST.get("delete","default")
    if(delete !="default"):
        file=File.objects.all()
        data=Element.objects.all()
        data.delete()
        file.delete()
        return render(request,"index.html")
    try:
        start=request.POST.get("start")
        end=request.POST.get("end")
        x=Element.objects.filter(timestamp__gte = start , timestamp__lte=end)
        l1=[]
        for i in x:
            j=i.objects_detected
            a=j.split(",")
            for j in a:
                l1.append(j)
        l2=[]
        count={}
        for i in l1:
            if i in l2:
                count[i]+=1;
            else:
                l2.append(i);
                count[i]=1;
        save_path=r"D:\Vs code\Web Development Back-end\django\internship_question\practic\Files"
        completeName=os.path.join(save_path,"report"+".csv")
        f=open(completeName,'w',newline="")
        fieldname=["threat","occurance"]
        writer = csv.DictWriter(f, fieldnames=fieldname)
        writer.writeheader()
        for i in count:
            writer.writerow({"threat" :i ,"occurance":count[i]})
        f.close()
        if len(x)!=0:
            data={
                "ele":x,
                "mes":"File added"
            }
            return render(request,"index.html",data)
    except:
        return render(request,"index.html")




   

