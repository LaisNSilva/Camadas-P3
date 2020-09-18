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
#import binascii

from servidor import Servidor


serialName = "COM4"

                # Windows(variacao de)
def int_byte(n):
    return (int(n)).to_bytes(1, byteorder='big')


def main():
    try:
 
        # com2 = enlace('COM2')
        # print("COM2 declarado")
        
    
        # com2.enable()
        # print("Comunicação ativa")
        
        com2 = Servidor("COM4")
        print("COM2 Declarado")
            
        com2.start()
        print("Comunicação ativa")
        
        
        
        #Endereço da imagema ser salva
        imageW = "./imgs/imageRecebida.png"
        print('imageW')
        
        
        # Recebe e responde HANDSHAKE
        print("vou receber o handshke")
        hdsk = com2.pega_handshake()
        print("Recebi HANDSHAKE")
        print(hdsk)
        tipo = hdsk[0]
        print("tipo de mensagem {}".format(tipo))
        com2.re_handshake(hdsk[0])
        print("RESPONDI o handskhe ")

        verifica_pacote = 1
        
        # RECEBE O PRIMERO HEAD:
        tam_payload, num_pacote, qtd_total_pac = com2.recebe_header_dado()
        print(tam_payload)
        print("Recebeu o primeiro haeder")

        #recebe primeiro pacoteeee
        tam = tam_payload+4
        print(tam_payload+4)
        dadoEOP = com2.recebe_pacote(tam) 
        print("recebi o pacote 1")     
        dado = dadoEOP[0:tam_payload]
        #print(dado)          
        verifica_pacote+=1     

        
        print("recebeu o primeiro pacote")
        com2.deu_certo()    
        print("enviou a verificação do pacote 1")   

        while verifica_pacote <= qtd_total_pac:
            # RECEBER O HEAD DO PACOTEs
            #com2.limpa_rx()
            #while com2.vazio_rx():
            time.sleep(1)
            tam_payload, num_pacote, qtd_total_pac = com2.recebe_header_dado()
            print("Recebeu o {} header".format(num_pacote))

            
            # VE SE O NUMERO DO PACOTE TA CERTO
            if num_pacote == verifica_pacote:
                tam = tam_payload+4

                print(tam)
                dadoEOP = com2.recebe_pacote(tam) 
                    
                 
                print("recebeu o pacote numero {}".format(num_pacote))
                
                # MANDA MENSAGEM DE QUE TA CERTO
                # PODE MANDAR MAIS UM PACOTE
                if dadoEOP[tam_payload] == 1 and dadoEOP[tam_payload+1] == 1 and dadoEOP[tam_payload+2]==1 and dadoEOP[tam_payload+3] == 1:
                    com2.deu_certo()
                    dado+= dadoEOP[0:tam_payload]          
                    verifica_pacote+=1 
                    print('tamanho certo')
                else:
                    com2.erro_EOP(num_pacote, verifica_pacote)
                    print("ERRO no tamanho!!!")
                print("enviou a verificação do pacote {}".format(num_pacote)) 
                
            else:
                # MANDA MENSAGEM DE ERRO PEDINDO OUTRO PACOTE
                print("Deu ERRO no pacote")
                print("O pacote errado é o {}".format(num_pacote))
                print("O pacote que deve ser enviado é o {}".format(verifica_pacote))
                com2.erro_num_pacote(num_pacote, verifica_pacote) 
                

        
        
        f = open(imageW, "wb")
        f.write(dado)
        
        f.close()

        com2.sucesso()
        print("Enviei mensagem de verificação: FIM DA TRANSMISSÃO")

        
        
        #-----------------------------------
        #TESTE CLASSES
        
        # size = 0
        # while size == 0:
        #     size=com2.pega_tamanho()
        #     time.sleep(0.2)
        # print("tamanho {}".format(size))
        
        # rxBuffer=com2.pega_dado(size)
        
        #-------------------------------------
        
        
        # rxBuffer_t, nRx_t = com2.getData(2)
        # size = int.from_bytes(rxBuffer_t, byteorder='big')
        # print("Recebeu tamanho {}".format(size))   
        
        
        
        # print("size {}".format(size))
        # rxBuffer, nRx = com2.getData(size)
        # print("Recebeu dado")
    
        
        
    
        # size_conf = nRx
        # dado = (int(size_conf)).to_bytes(2, byteorder='big')
        # com2.sendData(dado)
        # print("Enviou tamanho recebido")
      
    
        # # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com2.end()
        
    except Exception as ex:
        print(ex)
        print("ops! :-\\")
        com2.end()
        
    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
