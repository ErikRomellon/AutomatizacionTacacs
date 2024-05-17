#Programa realizado por Erik Jesús Romellón Lorenzana

#Probado en modelos Cisco SG350, SG550
#SG350 v2.5.9.13
#SG550 v2.5.9.13
#SG500 v1.4.x.x

#Probado en modelos dell
#6.3 o inferior
#6.4 o superior

import paramiko, os, subprocess, re
from time import sleep

#Variables
authListEnable = 'tacp'
authListLogin = 'tacplus'
address = '148.209.142.57'
key = 'RXdQ=GOk7Fwc86P17O+#8oO#aFM8Am'


listaIP = []
print("Bienvenido al menu de configuracion de TACACS.\nIngresa un rango de direcciones ip para escanear\n")

#realizar una busqueda por ping de los equipos activos
def busqueda():
    ip_inicio = input("Ingresa ip de inicio: ")
    ip_final = input("Ingresa ip de final: ")

    def Get_Host(x):
        puntos = 0
        posContador = 0

        for i in x:
            if i == ".":
                puntos = puntos + 1
            if puntos == 3:
                return (x[0:posContador + 1], x[posContador + 1:])
                break
            posContador += 1

    Network, primerHost = Get_Host(ip_inicio)
    Network, ultimoHost = Get_Host(ip_final)

    emptyString = ""

    Counter = 0

    print("REALIZANDO BUSQUEDA DE HOSTS ACTIVOS EN "+Network +primerHost+" - "+ultimoHost)
    for i in range(int(primerHost), int(ultimoHost) + 1):
        proceso = subprocess.getoutput("ping -n 1 " + Network + str(i))
        emptyString += proceso
        buscar = re.compile(r"TTL=")
        mo = buscar.search(emptyString)
        try:
            if mo.group() == "TTL=":
                print("Host " + Network + str(i) + " está Up")
                ip = Network + str(i)
                listaIP.append(ip)
        except:
            print("Host " + Network + str(i) + " está Down")

        emptyString = ""
    sleep(1)
busqueda()

#Despliegue de elementos encontrados
if listaIP:
    print("\nSE HAN ENCONTRADO LOS SIGUIENTES HOSTS ACTIVOS:")
    for ip in listaIP:
        print(ip)
    enter = input("Presione enter para inciar la configuracion ")

#En realidad son comandos de las ultimas versiones de firmware, no de esos modelos en especifico y estos comandos
#son compatibles con modelos sg200,sg300,sg500
def comandosCiscoSG350_SG550():
    print(f"\tConfigurando equipo {ip} ...\n")
    devices_access.send("configure terminal\n")
    sleep(1)
    devices_access.send("aaa authentication enable " + authListEnable + " tacacs enable\n")
    sleep(1)
    devices_access.send("aaa authentication login authorization " + authListLogin + " tacacs local\n")
    sleep(1)
    devices_access.send("tacacs-server host " + address + "\n")
    sleep(1)
    devices_access.send("tacacs-server key " + key + "\n")
    sleep(1)
    devices_access.send("line ssh\n")
    sleep(1)
    devices_access.send("login authentication " + authListLogin + "\n")
    sleep(1)
    devices_access.send("enable authentication " + authListEnable + "\n")
    sleep(1)
    devices_access.send("end\n")
    sleep(1)
    devices_access.send("wr\n")
    sleep(5)
    devices_access.send("y\n")
    sleep(5)
    devices_access.send("y\n")
    sleep(5)
    devices_access.send("\n")
    output = devices_access.recv(2000)
    outputConv = output.decode("utf-8")
    print("\n\tSE HA REALIZADO LA CONFIGURACION CON LOS SIGUIENTES COMANDOS: \n")
    print(outputConv)


#faltaria agregar comandos para equipos cisco cuando estos son diferentes por la version de firmware


#comandos para switches dell en versiones iguales o anteriores a la 6.3
def comandosDell6dot3():
    ##Comandos
    devices_access.send("configure\n")
    sleep(1)
    devices_access.send("aaa authentication login "+authListLogin+" tacacs\n")
    sleep(1)
    devices_access.send("aaa authentication enable "+authListEnable+" tacacs\n")
    sleep(1)
    devices_access.send("tacacs-server host " +address+"\n")
    sleep(1)
    devices_access.send("key "+key+"\n")
    sleep(1)
    devices_access.send("exit\n")
    sleep(1)
    devices_access.send("line ssh\n")
    sleep(1)
    devices_access.send("login authentication "+authListLogin+"\n")
    sleep(1)
    devices_access.send("enable authentication "+authListEnable+"\n")
    sleep(1)
    devices_access.send("end\n")
    sleep(1)
    devices_access.send("wr\n")
    sleep(5)
    devices_access.send("y\n")
    sleep(5)
    devices_access.send("y\n")
    sleep(5)
    devices_access.send("\n")
    sleep(5)
    output = devices_access.recv(2000)
    outputConv = output.decode("utf-8")
    print("\n\tSE HA REALIZADO LA CONFIGURACION CON LOS SIGUIENTES COMANDOS: \n")
    print(outputConv)

#comandos en switches dell con version de firmware igual o superior a 6.4
def comandosDell6dot4():
    ##Comandos
    devices_access.send("configure\n")
    sleep(1)
    devices_access.send("aaa authentication login "+authListLogin+" tacacs\n")
    sleep(1)
    devices_access.send("aaa authentication enable "+authListEnable+" tacacs\n")
    sleep(1)
    devices_access.send("tacacs-server host " +address+"\n")
    sleep(1)
    devices_access.send("key "+key+"\n")
    sleep(1)
    devices_access.send("exit\n")
    sleep(1)
    devices_access.send("line ssh\n")
    sleep(1)
    devices_access.send("login authentication "+authListLogin+"\n")
    sleep(1)
    devices_access.send("enable authentication "+authListEnable+"\n")
    sleep(1)
    devices_access.send("end\n")
    sleep(1)
    devices_access.send("wr\n")
    sleep(5)
    devices_access.send("y\n")
    sleep(5)
    devices_access.send("y\n")
    sleep(5)
    devices_access.send("\n")
    sleep(5)
    output = devices_access.recv(2000)
    outputConv = output.decode("utf-8")
    print("\n\tSE HA REALIZADO LA CONFIGURACION CON LOS SIGUIENTES COMANDOS: \n")
    print(outputConv)


def verificaciones():

    #Realiza las verificaciones de la marca del switch y modelo
    devices_access.send("show system\n")
    sleep(5)
    #almacena en una string lo obtenido por consola
    output = devices_access.recv(1000).decode("utf-8")
    #expresion con busqueda regular en output que busca SG\d+, donde d+ es un valor entero
    modeloCisco = re.findall(r'(SG\d+)', output)
    modeloDell = re.findall(r'Dell', output)
    sleep(5)

    #Si encuentra que es modelo cisco
    if modeloCisco:
        # Versiones de cisco probadas
        devices_access.send("show version\n")
        sleep(5)

        # Versiones de ios en SG250, SG350 y SG550 son iguales
        if modeloCisco[0] == 'SG350' or modeloCisco[0] == 'SG550' or modeloCisco[0] == 'SG250':
            output = devices_access.recv(1000).decode("utf-8")
            #sabiendo la marca y modelo busca la version de firmware para aplicar los comandos pertinentes
            versionIos = re.findall(r'Version:\s*([\d.]+)', output)
            if versionIos:
                #si se tiene la cadena{[2.4.6]} lo que hace esta funcion es buscar todos los puntos y a partir de ahi separar
                #en mas subcadenas quedando {[2], [4], [6]}

                #nota, se usa el elemento 0 del vector ya que si se cumple la condicion de entrada siempre habrá minimo
                #un elemento en la posicion 0 de este
                versionIosSplit = versionIos[0].split('.')

                #se utiliza la cadena que fue partida antes para obtener la version de firmware
                versionFinal = versionIosSplit[0] + versionIosSplit[1]
                versionFinal = int(versionFinal)
                #24 representa 2.4, hecho de esta forma ya que en pruebas buscando por 2.x habia que realizar muchos if
                #y esta es la forma mas optima
                if versionFinal <= 24:
                    opcion = input(f"Version de firmware no probada {versionIos[0]} ¿Deseas continuar aplicando los comandos? s/n: ")
                    opcion = opcion.lower()
                    if opcion == 's':
                        comandosCiscoSG350_SG550()
                    if opcion == 'n':
                        print(" Comandos de configuracion no enviados ")
                else:
                    comandosCiscoSG350_SG550()

        #Versiones de firmware en SG500, SG300 y SG200 son iguales
        elif modeloCisco[0] == 'SG500' or modeloCisco[0] == 'SG300' or modeloCisco[0] == 'SG200':
            output = devices_access.recv(1000).decode("utf-8")
            versionIos = re.findall(r'1.\d+', output)
            if versionIos:
                versionIosSplit = versionIos[0].split('.')
                versionFinal = versionIosSplit[0] + versionIosSplit[1]
                versionFinal = int(versionFinal)
                if versionFinal <= 13:
                    opcion = input(f"Version de firmware no probada {versionIos[0]} ¿Deseas continuar aplicando los comandos? s/n: ")
                    opcion = opcion.lower()
                    if opcion == 's':
                        comandosCiscoSG350_SG550()
                    if opcion == 'n':
                        print(" Comandos de configuracion no enviados ")
                else:
                    comandosCiscoSG350_SG550()
        else:
            print("Modelo de switch no compatible con el catalogo actual")


    #Comprobacion de equipos Dell
    if modeloDell:
        devices_access.send("q")
        devices_access.send("\n")
        devices_access.send("show version\n")
        sleep(5)
        output = devices_access.recv(1000).decode("utf-8")
        versionIos = re.findall(r'1 \s*([\d.]+)', output)
        if versionIos:
            versionIosSplit = versionIos[0].split('.')
            versionFinal = versionIosSplit[0] + versionIosSplit[1]
            versionFinal = int(versionFinal)
            if versionFinal <= 63:
                comandosDell6dot3()
            else:
                comandosDell6dot4()
        else:
            print("No se ha podido encontrar la version del firmware")


#Inicio de configuracion
if listaIP:
    for ip in listaIP:
        print(f"\n\tCONFIGURANDO {ip}")
        usuario = input(f"Ingrese nombre de usuario de {ip}: ")
        password = input(f"Ingrese el password de {ip}: ")

        # conexion por SSH
        try:
            print(f"\nIntentando establecer conexion con {ip}")
            cliente = paramiko.SSHClient()
            cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            cliente.connect(hostname=ip, port=22, username=usuario, password=password)
            devices_access = cliente.invoke_shell()
            print("Conexion realizada vía SSH!!!\n\n")
            sleep(1)
            os.system("cls")
            print(f"\n\tVerificando compatibilidad de {ip} ...\n")
            sleep(1)
            output = devices_access.recv(100).decode("utf-8")
            verificar = re.findall('>', output)
            if verificar:
                if verificar[0] == '>':
                    enable = input("Ingresa contraseña enable: ")
                    devices_access.send("enable\n")
                    sleep(10)
                    devices_access.send(enable+"\n")
            sleep(1)
            verificaciones()

        #Excepciones
        except paramiko.ssh_exception.AuthenticationException:
            print(f"No fue posible hacer conexion con {ip}, usuario o contraseña incorrecta ")
        except paramiko.ssh_exception.NoValidConnectionsError:
            print(f"\nERROR!! : No se puede conectar al puerto 22 en {ip}")
        except TimeoutError:
            print("Se produjo un error durante el intento de conexión ya que la parte conectada no respondió adecuadamente tras un periodo de tiempo, o bien se produjo un error en la conexión establecida ya que el host conectado no ha podido responder")
else:
    print("\n\n\tNo se ha encontrado ningun equipo en la red, verifica conexion o rango de direccion ip")

print("\n\n\tEjecucion de programa finalizado")
fin = input("Presiona enter para cerrar el programa")