# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 13:52:23 2020

@author: Lais Nascimento
"""

from enlace import *

def int_byte(n):
    return (int(n)).to_bytes(1, byteorder='big')


EOP = int_byte(1) + int_byte(1)+ int_byte(1) +int_byte(1)

# def byte_int(n):
#     return int.from_bytes(n, byteorder='big')   

class Cliente(object):
    
    def __init__(self, name):
        self.name        = name
        self.com         = None
        
    
    global pode_enviar
    
    def start(self):
        self.com = enlace(self.name)
        self.com.enable()
        
    def end(self):
        self.com.disable()
        
     
        
    def handshake(self):
        # pacote = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
        
        zero = int_byte(0)
        pacoteh = zero +zero+ zero+ zero+ zero+ zero+ zero+ zero+ zero+ zero+  EOP
        
        self.com.sendData(pacoteh)
        
    
    def verifica_re_handshake(self):
        rxBuffer = self.com.rx.getNData_h(14)
        if rxBuffer == b'\x00':
            return False
        else:
            if rxBuffer[0] == 7:
                print ("Não pode mandar dado")
                return False
            else:
                if rxBuffer[0] == 1:
                    print("Pode mandar dado!")
                    return  True
             
                
      #def gera_erro_numpac(self):


 
        
    def verifica_envia(self, verifica):
        if  verifica[0] == 3:
            return (True, 0, 0)
        else:
            if verifica[0] == 4 or verifica[0]==5: # ERRO NO NUMERO DO PACOTE
                qual_pacote_erro = verifica[4]
                print("deu erro no pacote{}".format(qual_pacote_erro))
                qual_pacote_errou = verifica[4]
                qual_pacote_enviar = verifica[5]
            return (False, qual_pacote_errou, qual_pacote_enviar)

                
    def quantos_pacotes(self, txBuffer):
        #txBuffer = open(dado, "rb").read()
        
        # TAMANHO TOTAL DO DADO
        txLen = len(txBuffer)
        
        # QUANTOS PACOTES VOU PRECISAR
        div_int = int(txLen/114)
        if txLen % 114 == 0 :
            qtd_pac = div_int
            ultimo_payload = 114
        else:
            qtd_pac = div_int + 1
            # PAYLOAD COM MENOS DE 114 BYTES
            # tamanhos - menos o que já foi envidado
            ultimo_payload = txLen - (114*div_int)

        return(qtd_pac, ultimo_payload)
        
        
    def prepara_dado(self, txBuffer, numero_do_pacote, byte_dado,qtd_pac, ultimo_payload, fim ):
        
        #qtd_pac, ultimo_payload = self.com.quantos_pacotes(dado)
        
        

        # TAMANHO DO PAYLOAD DO PACOTE
        if qtd_pac - numero_do_pacote !=0:
            tamanho_pl = 114
        else: 
            tamanho_pl = ultimo_payload
            
        z = int_byte(0)
        header_pacote = int_byte(2) + int_byte(tamanho_pl) + int_byte(numero_do_pacote) +int_byte(qtd_pac)+ z+ z+ z+ z+ z+ z
        
        
        
        pay_end_pacote = txBuffer[byte_dado:(tamanho_pl+byte_dado)] + fim
        
        return (header_pacote, pay_end_pacote)
    
    def envia_pacote(self, pacote):
        self.com.sendData(pacote)
        
    def recebe_pacote(self, tamanho):
        pacote = self.com.rx.getNData(tamanho)
        return pacote
                
                
            
                
                
                
                
    # TESTES -----------------------------------
    
    # def manda_tamanho(self, dado):
    #     txBuffer = open(dado, "rb").read()
    #     txLen  = len(txBuffer)
    #     tamanho= (int(txLen)).to_bytes(2, byteorder='big')
    #     self.com.sendData(tamanho)
        
    # def envia_dado(self, dado):
    #     txBuffer = open(dado, "rb").read()
    #     self.com.sendData(txBuffer)
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
            
        