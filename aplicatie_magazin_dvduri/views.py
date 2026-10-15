from django.shortcuts import render
from django.http import HttpResponse, Http404
from datetime import datetime
from urllib.parse import urlparse
from collections import Counter
import re


# Create your views here.

ZILE = ["Luni", "Marti", "Miercuri", "Joi", "Vineri", "Sambata", "Duminica"]
LUNI = ["Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie", "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie"]
FORMAT_IMPLICIT = "%A, %-d %B %Y"

def formateaza_data(data, format=FORMAT_IMPLICIT):
    def inlocuieste(m):
        c = m.group(1)
        if c == "A":
            return ZILE[data.weekday()]
        if c == "a":
            return ZILE[data.weekday()][:3]
        if c == "B":
            return LUNI[data.month - 1]
        if c == "b":
            return LUNI[data.month -1][:3]
        if c == "-d":
            return str(data.day)
        return m.group(0)
    format_ro = re.sub(r"%(-d|.)", inlocuieste, format)
    return data.strftime(format_ro)

class Accesare:
    contor = 1
    def __init__(self, ip_client, url="", parametri={}):
        self.id=Accesare.contor
        Accesare.contor+=1
        self.ip_client=ip_client
        self.url = url
        self.parametrii = parametri
        self.data = datetime.now()
        
    def __str__(self):
        return f"Accesare. ID:{self.id}"
    
    def lista_parametrii(self):
        return [
            (nume, valoare if valoare!= "" else None)
            for nume, valoare in self.parametrii.items()
        ]
    
    def string_url(self):
        return self.url
    
    def pagina(self):
        return urlparse(self.url).path
    
    def calculeaza_data(self, format=FORMAT_IMPLICIT):
        return formateaza_data(self.data, format)
    
ACCESARI = []
PROPRIETATI = ["id", "ip_client", "url", "parametrii", "data"]



def index(request):
    return render(request, "index.html",{
        "ip":request.ip,
        "param":request.GET.getlist("param"),
        "a":Accesare(""),
    })

#prima data cu datele
# def info(request):
#     a=request.GET.get("data")
    
#     acum = datetime.now()
#     zi_saptamana = ZILE[acum.weekday()]
#     luna = LUNI[acum.month -1 ]
#     data_ora = (
#         f"{zi_saptamana}, {acum.day} {luna} {acum.year}, "
#         f"{acum.strftime('%H:%M:%S')}"
#     )
    
#     return HttpResponse(f"""
#         <html><head><title>Informatii despre server</title></head><body><h1>Informatii despre server</h1><p>{a}</p><h2>Data si ora</h2><p>{data_ora}</p></body></html>
#         """)

def info(request):
    return render(request, "info.html",{
        "a":request.GET.get("data", ""),
        "data_ora":formateaza_data(datetime.now(), FORMAT_IMPLICIT + ", %H:%M:%S"),
    })
    
def istoric(request):
    return render(request, "in_lucru.html")

def despre(request):
    return render(request, "despre.html")
    
def accesare(request, id):
    for a in ACCESARI:
        if a.id == int(id):
            return render(request, "accesare.html", {
                "a": a,
                "data_ora":a.calculeaza_data(FORMAT_IMPLICIT + ", %H:%M:%S"),
            })
    raise Http404("Nu exista accesarea cautata")

def exemplu_template(request):
    return render(request,"template.html",
        {
            "titlu_tab":"Titlu fereastra",
            "titlu_articol":"Titlu afisat",
            "continut_articol":"Continut text"
        }
    )
    
def exemplu_template2(request):
    return render(request,"template2.html",
    )


#ex 1 partea 1
# def log(request):
#     k = len(ACCESARI)
#     ultimele = request.GET.get("ultimele")
#     eroare =""
#     afisate = ACCESARI
    
#     if ultimele is not None:
#         if not ultimele.isdigit():
#             return render(request, "log.html", {
#                 "eroare" : f"Parametrul ultimele trebuie sa fie un numar intreg (primit: {ultimele})"
#             })
#         n = int(ultimele)
#         afisate = ACCESARI[-n:] if n else []
#         if n > k:
#             eroare = f"Exista doar {k} accesari fata de {n} accesari cerute"
#     return render(request, "log.html", {"accesari": afisate, "eroare": eroare})


#ex 2 partea 1
# def log(request):
#     afisate = ACCESARI
    
#     if "iduri" in request.GET:
#         dubluri = request.GET.get("dubluri") == "true"
#         ids = []
#         for valoare in request.GET.getlist("iduri"):
#             for i in valoare.split(","):
#                 if i.isdigit() and (dubluri or int(i) not in ids):
#                     ids.append(int(i))
#         afisate = [a for i in ids for a in ACCESARI if a.id == i]
#     k = len(afisate)
#     ultimele = request.GET.get("ultimele")
#     eroare =""
#     if ultimele is not None:
#         if not ultimele.isdigit():
#             return render(request, "log.html", {
#                 "eroare" : f"Parametrul ultimele trebuie sa fie un numar intreg (primit: {ultimele})"
#             })
#         n = int(ultimele)
#         afisate = afisate[-n:] if n else []
#         if n > k:
#             eroare = f"Exista doar {k} accesari fata de {n} accesari cerute"
            
#     nr = len(ACCESARI) if request.GET.get("accesari") == "nr" else None
#     return render(request, "log.html", {"accesari": afisate, "eroare": eroare, "nr": nr})

#ex 3 partea 1
# def log(request):
#     afisate = ACCESARI
    
#     if "iduri" in request.GET:
#         dubluri = request.GET.get("dubluri") == "true"
#         ids = []
#         for valoare in request.GET.getlist("iduri"):
#             for i in valoare.split(","):
#                 if i.isdigit() and (dubluri or int(i) not in ids):
#                     ids.append(int(i))
#         afisate = [a for i in ids for a in ACCESARI if a.id == i]
#     k = len(afisate)
#     ultimele = request.GET.get("ultimele")
#     eroare =""
#     if ultimele is not None:
#         if not ultimele.isdigit():
#             return render(request, "log.html", {
#                 "eroare" : f"Parametrul ultimele trebuie sa fie un numar intreg (primit: {ultimele})"
#             })
#         n = int(ultimele)
#         afisate = afisate[-n:] if n else []
#         if n > k:
#             eroare = f"Exista doar {k} accesari fata de {n} accesari cerute"
            
#     optiuni = request.GET.getlist("accesari")
#     nr = len(ACCESARI) if "nr" in optiuni else None
#     detalii = None
#     if "detalii" in optiuni:
#         detalii = [a.calculeaza_data(FORMAT_IMPLICIT + ", %H:%M:%S") for a in afisate]
#     parametrii = list(request.GET.keys())
    
#     return render(request, "log.html", {
#         "accesari": afisate, "eroare": eroare, "nr":nr,
#         "detalii": detalii, "parametrii": parametrii
#     })

#ex 4 partea 1
def log(request):
    afisate = ACCESARI
    
    if "iduri" in request.GET:
        dubluri = request.GET.get("dubluri") == "true"
        ids = []
        for valoare in request.GET.getlist("iduri"):
            for i in valoare.split(","):
                if i.isdigit() and (dubluri or int(i) not in ids):
                    ids.append(int(i))
        afisate = [a for i in ids for a in ACCESARI if a.id == i]
    k = len(afisate)
    ultimele = request.GET.get("ultimele")
    eroare =""
    if ultimele is not None:
        if not ultimele.isdigit():
            return render(request, "log.html", {
                "eroare" : f"Parametrul ultimele trebuie sa fie un numar intreg (primit: {ultimele})"
            })
        n = int(ultimele)
        afisate = afisate[-n:] if n else []
        if n > k:
            eroare = f"Exista doar {k} accesari fata de {n} accesari cerute"
            
    optiuni = request.GET.getlist("accesari")
    nr = len(ACCESARI) if "nr" in optiuni else None
    detalii = None
    if "detalii" in optiuni:
        detalii = [a.calculeaza_data(FORMAT_IMPLICIT + ", %H:%M:%S") for a in afisate]
    parametrii = list(request.GET.keys())
    
    coloane = randuri = None
    if "tabel" in request.GET:
        cerute = ",".join(request.GET.getlist("tabel")).split(",")
        coloane = PROPRIETATI if "tot" in cerute else [c for c in cerute if c in PROPRIETATI]
        randuri = [[getattr(a,c) for c in coloane] for a in afisate]
        
    contor = Counter(a.pagina() for  a in ACCESARI).most_common()
    mai_mult = contor[0][0]
    mai_putin = contor[-1][0]
    
    return render(request, "log.html", {
        "accesari": afisate, "eroare": eroare, "nr":nr,
        "detalii": detalii, "parametrii": parametrii,
        "coloane": coloane, "randuri": randuri,
        "mai_mult": mai_mult, "mai_putin": mai_putin,
    })