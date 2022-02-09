
import re
import random
import smtplib, ssl

from colorama import Fore, init,Back
from termcolor import colored



#===============================================================================
'''                    INFORMACION                                          '''
#===============================================================================

horario = [""]
tutores={"182121":"QUINTANILLA PORTUGAL ROXANA LISETTE","152320":"ALZAMORA PAREDES ROBERT WILBERT","121549":"CARBAJAL LUNA JULIO CESAR","152623":"ENCISO RODAS LAURO"}
enlaces = {"182121":"http://dina.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do;jsessionid=f564431f36070c2b4a0e4a590b74?id_investigador=40930\n",
"152320":"http://dina.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do;jsessionid=4a5ff14ed01cd079308c0dc3a5f3?id_investigador=48884\n",
"121549":"http://dina.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do;jsessionid=d042918fe619ed09ce172b453642?id_investigador=11558\n",
"152623":"http://dina.concytec.gob.pe/appDirectorioCTI/VerDatosInvestigador.do;jsessionid=3e617986f444056280d649b14806?id_investigador=48985"}
mensaje = ""
Areas =["\nAqui tienes el enlace del documento con la informacion de las areas de especializacion: \n LINK AREA DE ESPECIALIZACION\n"]
proyectos=["\nAqui tienes el enlace del documento con consejos para realizar informes academicos: \n https://docs.google.com/document/d/e/2PACX-1vR2IPzqz9L_ZFO-setVEdQos25yo6dDkUiqQcZxmymx2D1hOv-IlACLmDRe_-IrjNY5B4frfLH9sq6v/pub\n ",
"\nAqui tienes el enlace del documento con consejos para realizar articulos cientificos: \n https://docs.google.com/document/d/e/2PACX-1vSK4waYhyQjdstlqGbuu8lYKbFYTXC6at2C2vcmdyvgoJNyKYQl-2czweFOOj-XsnQNQchyoqTr5uMI/pub \n",
"\nAqui tienes el enlace del documento con consejos para realizar tesinas : \n https://docs.google.com/document/d/e/2PACX-1vRudaXGNK7cck_4IsUqA9KdW89i0flFS-Zh0jAdKuGEHB2P8HlDOyn4YPLAqe43gALuy9puJkBFh8K_/pub \n",
"\nAqui tienes el enlace del documento con consejos para realizar ensayos: \n https://docs.google.com/document/d/e/2PACX-1vRQyw0PmrY1lcRgbr87NB5ocFYRRKXZ-ZSdwws89z2Rj64lkyBEz6a-T58V4FXYJqj9Pjj3F5PFYhaN/pub\n ",
"\nAqui tienes el enlace del documento con algunas herramientas de apoyo: \n https://docs.google.com/document/d/e/2PACX-1vSgtmeGTwRfoI7JC2P2NdCl_Q7NlGU6NbIABwqgseu6AgPFy8casoktW3IAWZhppZ7XruJP5bSvVe9B/pub\n "
]
infoPostgrado =["\nAqui tienes el enlace del documento con informacion del postgrado: \n http://postgrado.unsaac.edu.pe/laescuela/doc/ReglamentoAdmisionEPG.pdf\n"]
gruposEstudio =["\nAqui tienes el enlace del documento con informacion de los grupos de estudio de la escuela:\n https://www.facebook.com/ACMUNSAAC/ \n"]
Formulario = ["\nAqui tienes el link del formulario: \n https://docs.google.com/forms/d/e/1FAIpQLScHTbfS_cbiUnmuxpPtjksLt3kOF6hSXM24B6UNtJhvRKjfyQ/viewform \n"]

#modulos para procesar la informacion y las respuestas

#===============================================================================
'''              Modulo para recuperar codigo ingresado               '''
#===============================================================================

def Buscar_codigo(mensaje):
    cod = ""
    for i in mensaje:
        if(i in ['0','1','2','3','4','5','6','7','8','9']):
            cod = cod + i
    return cod.strip()
#main
#===============================================================================
'''              Modulo para recuperar respuesta del usuario              '''
#===============================================================================
def get_respuesta(user_input):

    codigo=Buscar_codigo(user_input)
    if codigo == "" and len(codigo)<2:
        codigo ="" 
    split_mensaje = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower())
    response = revisar_todos_sms(split_mensaje,codigo)
    return response

#===============================================================================
'''              Modulo para recuperar la probabilidad del mensaje           '''
#===============================================================================
def probabilidad_mensaje(mensaje_usuario, palabras_reconocidas, respuestas_sencillas=False, palabras_requeridas=[]):
    asertividad_mensaje = 0
    tiene_palabras_requeridas = True

    for palabra in mensaje_usuario:
        if palabra in palabras_reconocidas:
            asertividad_mensaje +=1

    #porcentaje de que la respuesta que se este dando sea la mas aproximada
    percentaje = float(asertividad_mensaje) / float (len(palabras_reconocidas))

    for palabra in palabras_requeridas:
        if palabra not in mensaje_usuario:
            tiene_palabras_requeridas = False#el mensaje no cumple algunas de las palabras requeridas
            break
    if tiene_palabras_requeridas or respuestas_sencillas:
        return int(percentaje * 100)#retornar aquel que tiene un mayor porcentaje
    else:
        return 0

#===============================================================================
'''              Modulo para revisar todos los mensajes                  '''
#===============================================================================
def revisar_todos_sms(message,codigo):       
        probabilidad_mayor = {}       
        def respuesta(bot_respuesta, lista_de_palabras, respuesta_simple = False, palabras_requeridas = [],caracter = []):
            nonlocal probabilidad_mayor
            probabilidad_mayor[bot_respuesta] = probabilidad_mensaje(message, lista_de_palabras, respuesta_simple, palabras_requeridas)
        
        ##=======================mensajes a mostrar ====================================================   
        mensajeMenu = 'En que te puedo ayudar hoy ...??\nTengo las siguientes opciones: \n\r\r\r-Quiero conocer mas sobre mi tutor\n\r\r\r-Ayuda en algunos puntos en el ambito academico\n\r\r\r-Quiero agendar una cita '
        mensajefinal ='Espero haberte ayudado :) y espero nos volvamos a ver pronto'
        mensajevolver = '¿En que mas te puedo ayudar hoy :v ?\nTengo las siguientes opciones: \n\r\r\r-Quiero conocer mas sobre mi tutor\n\r\r\r-Ayuda en algunos puntos en el ambito academico\n\r\r\r-Quiero agendar una cita '
        mensajeSINO ="¿Te puedo ayudar en algo mas?\n\r\r\r-SI,\n\r\r-NO"
        mensajeElegirHorario = "Horarios:\n\r\r-Mañana\n\r\r-Tarde"
        mensajeAyudaAcademica ='Puedes elegir las siguientes opciones:\n\r\r-Conocer mas las area de especializacion\n\r\r-Consejos para realizar algunos proyectos\n\r\r-Informacion sobre el postgrado\n\r\r-Informacion sobre grupos de estudio'
        mensajeTipsProyetos ='Puedes elegir las siguientes opciones:\nTips, ideas y herramientas:\n\r\r-Para informes academicos\n\r\r-Para articulos cientificos\n\r\r-Para tesinas\n\r\r-Para Ensayos\n\r\r-Algunas herramientas de apoyo'
        mesajeRellenarFormulario ='Por favor, rellene el formulario accediendo al siguiente link:\n\r\rojo: "Es de suma importacia rellenar el formulario para agendar su cita, caso contrario su cita no procedera"\nf'

        ##==================Respuestas por parte del chatboot =============================================
        respuesta(mensajeMenu, ['hola', 'hello', 'saludos', 'buenas','hi','holi'], respuesta_simple = True)
        #para obtener info del docente       
        respuesta('Por favor :)\nIngresa tu código en este formato, ej= "codigo : 182121" : ', ['conocer','tutor','sobre'], respuesta_simple=True)
        #para ayuda academica 
        respuesta(mensajeAyudaAcademica, ['ayuda','ambito','academico' ], respuesta_simple=True)
        respuesta('En este enlace podras encontrar mas informacion sobre las areas de especializacion :\n'+Areas[0]+mensajeSINO, ['conocer','mas','areas','especializacion' ], respuesta_simple=True)
        #para tipos de proyecto
        respuesta(mensajeTipsProyetos, ['consejos','realizar','algunos','proyectos' ], respuesta_simple=True)
        respuesta('Para informes academicos: '+proyectos[0]+mensajeSINO, ['informes'], respuesta_simple=True)
        respuesta('\nPara articulos cientificos: '+proyectos[1]+mensajeSINO, ['articulos','cientificos'], respuesta_simple=True)
        respuesta('Para tesinas : '+proyectos[2]+mensajeSINO, ['tesinas','tesina'], respuesta_simple=True)
        respuesta('Para  Ensayos: '+proyectos[3]+mensajeSINO, ['ensayos','ensayo'], respuesta_simple=True)
        respuesta('Algunas herramientas de apoyo: '+proyectos[4]+mensajeSINO, ['herramientas','apoyo'], respuesta_simple=True)
        #para info postgrado
        respuesta('En este enlace podras encontrar informacion del postgrado:\n'+infoPostgrado[0]+mensajeSINO, ['informacion','postgrado','sobre'], respuesta_simple=True)
        #para info grupos de estudio
        respuesta('En este enlace podras encontrar informacion de los grupos de estudio :\n'+   gruposEstudio[0]+mensajeSINO, ['informacion','grupos','estudio','sobre'], respuesta_simple=True)
        #mensajes de retorno menu prinicpal y salir
        respuesta(mensajevolver, ['si'], respuesta_simple=True)
        respuesta(mensajefinal, ['no'], respuesta_simple=True)

        #para agendar cita
        respuesta(mesajeRellenarFormulario+Formulario[0]+mensajeElegirHorario, ['agendar','cita'], respuesta_simple=True)
        respuesta('Se tiene los siguientes horarios:\n\r\r- 7am a 9am\n\r\r- 9am a 10am\n\r\r- 10am a 11am\nElige uno de los horarios', ['mañana'], respuesta_simple=True)
        respuesta('Se tiene los siguientes horarios:\n\r\r- 1pm a 2pm\n\r\r- 3pm a 5pm\n\r\r- 5pm a 7pm\nIngrese un horario elegido en formato ej:"6am a 7am"', ['tarde'], respuesta_simple=True)


        respuesta('Espera la notificación del docente para que te confirme la cita'+mensajeSINO, ['7am','a', '9am'], respuesta_simple=True)
        respuesta('Espera la notificación del docente para que te confirme la cita'+mensajeSINO, ['9am','a','10am'], respuesta_simple=True)
        respuesta('Espera la notificación del docente para que te confirme la cita'+mensajeSINO, ['10am','a','11am'], respuesta_simple=True)
    
        respuesta('Espera la notificación del docente para que te confirme la cita'+mensajeSINO, ['1pm','a','2pm'], respuesta_simple=True)
        respuesta('Espera la notificación del docente para que te confirme la cita'+mensajeSINO, ['3pm','a','5pm'], respuesta_simple=True)
        respuesta('Espera la notificación del docente para que te confirme la cita'+mensajeSINO, ['5pm','a','7pm'], respuesta_simple=True)               

        #para informacion del tutor
        if(codigo != " " and len(codigo) >2):
            respuesta("\nDatos del Tutor: \n"+tutores[codigo]+"\nPuede obtener mas informacion en el siguiente enlace:\n"+enlaces[codigo]+mensajeSINO, ['codigo',':'],  respuesta_simple=True)

        #buscando maximo entre la probabilidad
        buscando_maximo = max(probabilidad_mayor, key=probabilidad_mayor.get)
        
        #si la probabilidad del buscado maximo es menor a 1 devolver desconocido
        #caso contrario devolver la mejor respuesta(la qu mejor encaja)
        return desconocido() if probabilidad_mayor[buscando_maximo] < 1 else buscando_maximo

#===============================================================================
'''              Modulo para mensajes desconocidos                 '''
#===============================================================================

def desconocido():
    response = [':''v puedes decirlo de nuevo?', ':( No estoy seguro de lo quieres','Lo siento :''(  no conozco este tema'][random.randrange(3)]
    return response

#===============================================================================
'''                       PROGRAMA PRINCIPAL                                '''
#===============================================================================

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[10m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

init()
print(color.BOLD+Back.LIGHTYELLOW_EX+Fore.RED+"\nTuto-Bot : )"+Back.RESET)
print(color.BOLD+Back.LIGHTYELLOW_EX+Fore.BLACK+"Hola!!!, soy tu amigo Tuto_bot :)\n"+Back.RESET)

codigo = ""
while True:
    init()
    mensaje =input(color.BOLD+Fore.LIGHTMAGENTA_EX+'Yo: ')
    print(" ")
    init()
    print(color.BOLD+Back.LIGHTYELLOW_EX+Fore.RED+"Tuto-Bot: " )
    #encontrar respuesta para la consulta
    print(color.BOLD+Back.LIGHTYELLOW_EX+Fore.BLACK + get_respuesta(mensaje)+Back.RESET)
    
    print(" ")

    #Recuperar codigo del estudiante
    if('codigo' in mensaje ):
        codigo = Buscar_codigo(mensaje)
    
    #Recuperar el horario que eligio el estudiante
    if(mensaje=='7am a 9am' or mensaje=='9am a 10am' or mensaje=='10am a 11am' or mensaje=='1pm a 2pm'or mensaje=='3pm a 5pm' or mensaje=='5pm a 7pm'):
        horario[0]=mensaje
        #Enviar notificacion al correo del docente tutor
        username= "mermahuamannoheminatalia"
        password= "135mateal58-"
        context= ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as server:
            server.login(username,password)
            #print("inició sesión !")
            destinatario="182920@unsaac.edu.pe"
            mensaje=codigo+"\n"+horario[0]
            server.sendmail(username,destinatario,mensaje)
            #print("mensaje enviado ")


