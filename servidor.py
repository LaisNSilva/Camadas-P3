# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 13:52:25 2020

@author: Lais Nascimento
"""


from enlace import *

def int_byte(n):
    return (int(n)).to_bytes(1, byteorder='big') 

EOP = int_byte(1) + int_byte(1)+ int_byte(1) +int_byte(1)

def byte_int(n):
    return (int.from_bytes(n, byteorder='big'))



class Servidor(object):
    
    def __init__(self, name):
        self.name        = name
        self.com         = None
        
        
    def start(self):
        self.com = enlace(self.name)
        self.com.enable()
        
    def end(self):
        self.com.disable()

    
    def pega_handshake(self):
        rxBuffer = self.com.rx.getNData(14)
        return(rxBuffer)
    
    def re_handshake(self, hdsk):
        # pacote = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
        
        #rxBuffer, nRx = self.com.getData(14)
        if hdsk == 0:
            # Mensagem de handshake
            # Tem que enviar a resposta
            z =  (int(0)).to_bytes(1, byteorder='big')
            um = (int(1)).to_bytes(1, byteorder='big')
            sete = (int(7)).to_bytes(1, byteorder='big')
            
            pacote = um+ z+ z+ z+ z+ z+ z+ z+ z+ z+ um+ um+ um+ um
            self.com.sendData(pacote)
        else:
            pacote = sete + z+ z+ z+ z+ z+ z+ z+ z+ z+ um+ um+ um+ um
            self.com.sendData(pacote)

            
    def erro_num_pacote(self, qual_pacote_errou, reenvio):
        #pacote=[2, 0, 0, 0, qual_pacote_errou, reenvio, 0, 0, 0, 0 ]
        z = int_byte(0)
        pac_npacote = int_byte(4)+ z+ z+ z+ int_byte(qual_pacote_errou)+ int_byte(reenvio)+z + z+ z+ z +EOP
        self.com.sendData(pac_npacote)

    def erro_EOP(self, qual_pacote_errou, reenvio):
        #pacote=[5, 0, 0, 0, qual_pacote_errou, reenvio, 0, 0, 0, 0 ]
        z = int_byte(0)
        pac_npacote = int_byte(5)+ z+ z+ z+ int_byte(qual_pacote_errou) + int_byte(reenvio)+z + z+ z+ z +EOP
        self.com.sendData(pac_npacote)
        
            
    def recebe_header_dado(self):
        header = self.com.rx.getNData(10)
        #tam_payload = 0
        #num_pacote = 0
        #qtd_total_pac = 0 
        print("header: {}".format(header[0]))
        if header[0] == 2:
            tam_payload = header[1]
            
            num_pacote = header[2]
             
            qtd_total_pac = header[3]
        
        return (tam_payload, num_pacote, qtd_total_pac)

    def deu_certo(self):
        z = int_byte(0)
        pacote_deu_certo=int_byte(3)+ z+ z+ z+ z+ z+ z+ z+ z+ z +EOP
        self.com.sendData(pacote_deu_certo)

    def sucesso(self):
        #pacote[8, 0,0,0,0,0,0,0,0,0 +eop]
        z = int_byte(0)
        sucesso_tras=int_byte(8)+ z+ z+ z+ z+ z+ z+ z+ z+ z +EOP
        self.com.sendData(sucesso_tras)



    
    def recebe_pacote(self, tam):
        print("entrei")
        pacote= self.com.rx.getNData(tam)
        print("peguei")
        return (pacote)
        
        
    def envia_pacote(self, pacote):
        self.com.sendData(pacote)
        
    def limpa_rx(self):
        self.com.rx.clearBuffer()
            
    def vazio_rx(self):
        return self.com.rx.getIsEmpty()
             
    
    # def verifica_pacote():
    #     for byte 
            
        
        
     # TESTES -----------------------------------
    
    # def pega_tamanho(self):
    #     rxBuffer_t, nRx_t = self.com.getData(2)
    #     size = int.from_bytes(rxBuffer_t, byteorder='big')
    #     print("Recebeu tamanho {}".format(size))  
    #     return size
        
        
    # def pega_dado(self, size):
    #     rxBuffer, nRx = self.com.getData(size)
    #     return rxBuffer
        
        
        
        
        
        
        
        
        
        
        
        