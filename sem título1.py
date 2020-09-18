# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 16:04:11 2020

@author: Lais Nascimento
"""

def int_byte(n):
    return (int(n)).to_bytes(1, byteorder='big')
z = int_byte(0)
pacote_deu_certo=int_byte(3)+ z+ z+ z+ z+ z+ z+ z+ z+ z 
EOP = int_byte(1) + int_byte(1)+ int_byte(1) +int_byte(1)

print(pacote_deu_certo[0:3]+EOP)

def prepara_dado( dado, numero_do_pacote, byte_dado,qtd_pac, ultimo_payload ):
       
       #qtd_pac, ultimo_payload = self.com.quantos_pacotes(dado)
       
       txBuffer = open(dado, "rb").read()

       # TAMANHO DO PAYLOAD DO PACOTE
       if qtd_pac - numero_do_pacote !=0:
           tamanho_pl = 114
       else: 
           tamanho_pl = ultimo_payload
           
       z = int_byte(0)
       header_pacote = int_byte(2) + int_byte(tamanho_pl) + int_byte(numero_do_pacote) +int_byte(qtd_pac)+ z+ z+ z+ z+ z+ z
       
       
       
       pay_end_pacote = txBuffer[byte_dado:tamanho_pl] + EOP
       
       return (header_pacote, pay_end_pacote)
dado = "C:/Users/Lais Nascimento/Desktop/Projeto3/imgs/imageTeste.png"

n = 1

b = 0

q = 5

p= 26

print(prepara_dado(dado, n, b, q, p))


   
