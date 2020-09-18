#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time

# BIBLIOTECA PARA INTERFACE
from tkinter import *
import pandas as pd 
from tkinter.ttk import *
import re
from textblob import TextBlob
from tqdm.auto import tqdm
from tkinter import Label

from tkinter.filedialog import askopenfile

from clientepy import Cliente

serialName = "COM3" 
#serialName = "COM2"  
               # Windows(variacao de)

def int_byte(n):
    return (int(n)).to_bytes(1, byteorder='big')

content = None
def open_file(): 
    global content
    file= askopenfile(mode ='r', filetypes =[('Todos arquivos', '.*')]) 
    if file is not None: 
        file_name = file.name
        print(file_name)
        #file_text.insert(END, file_name)
        content = file_name
        
  
#btn = Button(root, text ='Open', command = lambda:open_file()) 
#btn.pack()  


def main():
    print("cria interface")
    
    root = Tk() 
    root.geometry('400x150') 
    #file_text = Text(root, height=0.5, width=22)
    root.title("Cliet - Server")
    
    btn = Button(root, text ='Open', command = lambda:open_file()) 
    btn.pack() 
    
    #file_text.pack(pady = 22)
    
    root.mainloop()
    

    print(content)
    
    if content is not None:
        
        
        try:


            com1 = Cliente("COM3")
            print("COM1 Declarado")
            
            com1.start()
            print("Comunicação ativa")

            # Endereço da imagem a ser transmitida
            imageR = content
            
            #Carrega imagem
            print("Carregando imagem para transmissão :")
            print (" - {}".format(imageR))        
            print("-----------------------")
            txBuffer = open(imageR, "rb").read()

            
        
            
            
            
            # Endereço da imagem a ser transmitida
            # TESTE CLASSES--------------------
            
            #imageR = content 
            #com1.manda_tamanho(imageR)
            #com1.envia_dado(imageR)
            
            #-----------------------------------
            
            # Envia HANDSHEKE
            com1.handshake()
            print("enviou o HANDSHAKE!!!")

            
            resp = com1.verifica_re_handshake() 
            if resp == False:
                X= input("Servidor inativo. Tentar novamente? ")
                if X == "sim":
                    com1.handshake()
                    resp = com1.verifica_re_handshake()
                else:
                    resp = False 
            else: 
                pass
            
            if resp == False:
                pass 
                    
                
            
            print("-------------------------------------------")
            print(resp)
            print("Verifiquei a RESPOSTA do Handshake")
            print("------------------------------------------")
            
            if resp == True:
                #ENVIA DADO
                print("Vou começar a enviar o dado")
                qtd_pac, ultimo = com1.quantos_pacotes(txBuffer)
                numero_pac = 1
                print(qtd_pac)
                print(ultimo)
                byte_dado = 0
                correcao = 0
                while numero_pac <= qtd_pac:
                    EOP = int_byte(1) + int_byte(1)+ int_byte(1) +int_byte(1)
                    print("numero do pacote {}".format(numero_pac))
                    #envia primeiro pacote
                    if numero_pac == 1:
                        print("vou enviar o pacote 1")
                        header_pacote, pay_end_pacote= com1.prepara_dado(txBuffer, numero_pac, byte_dado, qtd_pac, ultimo, EOP)
                        print("preparou pacotes")
                        com1.envia_pacote(header_pacote)
                        print("enviou")
                        print(len(header_pacote))
                    
                        time.sleep(0.2)
                        # ENVIA DADO
                        com1.envia_pacote(pay_end_pacote)
                        print("enviou pac") 
                        print(len(pay_end_pacote))                       
                        
                        numero_pac +=1
                        byte_dado += header_pacote[1]

                        pacote_verificacao = com1.recebe_pacote(14)
                        print("Recebi a verificação")
                    
                    else:    
                    # VERIFICA SE PODE ENVIAR
                        #print("entrei no else")
                        if correcao != 2:
                            v, qual_erro, qual_reenviar = com1.verifica_envia(pacote_verificacao)
                        if  v== True:
                            print("vou enviar o pacote {}".format(numero_pac))
                            if correcao ==0:
                                #numero_pac+=1
                                EOP = int_byte(0) + int_byte(1)+ int_byte(1) +int_byte(1)
                            correcao = 1
                            header_pacote, pay_end_pacote= com1.prepara_dado(txBuffer, numero_pac, byte_dado, qtd_pac, ultimo, EOP)
                            print("preparou pacotes")
                            time.sleep(2)
                            com1.envia_pacote(header_pacote)
                            print("enviou")

                            time.sleep(0.3)
                            # ENVIA DADO
                            com1.envia_pacote(pay_end_pacote)
            
                            print("enviou dado")

                            numero_pac +=1
                            byte_dado += header_pacote[1]

                            pacote_verificacao = com1.recebe_pacote(14)

                        else: 
                            print("server avisou que há um ERRO!!!")
                            numero_pac = qual_reenviar
                            print("O pacote a ser enviado é o {}".format(numero_pac))
                            numero_erro = qual_erro
                            print("O pacote errado é o {}".format(numero_erro))
                            if numero_pac ==numero_erro:
                                byte_dado = byte_dado -114
                            else:
                                byte_dado = byte_dado - ((numero_erro - numero_pac)*114)
                            correcao = 2
                            v = True
                            
                            
  
                
                print("ENVIEI O DADO")
                
                S =com1.recebe_pacote(14)
                if S[0] == 8:
                    print("Recebi mensagem final: TRANSMISSÃO FEITA COM SUCESSO!!!")
                
            else: 
                print("NÃO PUDE ENVIAR O DADO")
                pass
            
            
            
            
            
           #  # Carrega imagem
           #  print("Carregando imagem para transmissão :")
           #  print (" - {}".format(imageR))        
           #  print("-----------------------")
           #  txBuffer = open(imageR, "rb").read()
        
           #  # COMEÇA A CONTAR O TEMPO
           #  inicio = time.time()
             
           #  # ENVIAR PRIMEIRO O TAMANHO
           #  #time.sleep(0.1)
           #  txLen = len(txBuffer)
           #  dado = (int(txLen)).to_bytes(2, byteorder='big')
           #  com1.sendData(dado)
           #  print("Enviou tamanho da imagem")
           #  print("-------------------------")
            
            
            
           # # ENVIA IMAGEM
           #  com1.sendData(txBuffer)
           #  print("Enviou IMAGEM")
           #  print("-------------------------")
            
           #  while (com1.tx.getIsBussy()):
           #      pass
    
          
           #  # Tempo final      
           #  fim = time.time()
            
           #  rxBuffer, nRx = com1.getData(2)
           #  print("Recebeu tamanho")   
           #  confere = int.from_bytes(rxBuffer, byteorder='big')
           #  if confere == txLen:
           #      print ("Deu certo!!!")
           #      print("-------------------------")
           #  else:
           #      print("ERRO")
           #      print("-------------------------")
             
            
            # tempo = fim - inicio
            # print("Time: {}".format(tempo))
            # print("-------------------------")
            
            # transm = (txLen+2)/tempo
            # print("Baud rate: {} bytes/s".format(transm))
            
            # resp = None
            # inicio_1 = time.time()
            # fim_1=0
            # while resp == None and fim_1<5:
            #     fim_1 = time.time() - inicio_1
            #     print(fim_1)
            #     resp = com1.verifica_re_handshake()

            #     #passou 5 segundo
            # if resp == None:
            #     X= input("“Servidor inativo. Tentar novamente? ")
            #     if X == "sim":
            #         inicio_2 = time.time()
            #         fim_2=0
	           #     
            #         while resp == None and fim_2<5:
            #             fim_2 = time.time() - inicio_2
            #             resp = com1.verifica_re_handshake()    
            #             #passou 5 segundo
            #     else:
            #         pass
            # if resp == None:
            #     resp = False
            
            #print(txBuffer)
            print("-------------------------")
            print("Comunicação encerrada")
            print("-------------------------")
            com1.end()
            
        except Exception as ex:
            print(ex)
            print("ops! :-\\")
            com1.end()
            
if __name__ == "__main__":
    main()
