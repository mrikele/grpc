from __future__ import print_function

import logging
import threading
import grpc
import chat_pb2_grpc
import chat_pb2

class Credencial:
    def __init__(self, nome, servidor, porta):
        self.nome = nome
        self.servidor = servidor
        self.porta = porta
        self.monta_credencial(self.nome, self.servidor, self.porta)
    
    def monta_credencial(self, nome, servidor, porta):
        credencial = '{}:{}:{}'.format(nome, servidor, porta)
        return credencial


class Cliente:
    def __init__(self):
        channel = grpc.insecure_channel('localhost:50051')
        self.stub = chat_pb2_grpc.ChatStub(channel)
        threading.Thread(target=self.recebe_mensagens).start()
        self.enviar_credencial()
        #self.envia_mensagem()
    
    def recebe_mensagens(self):
        for resposta in self.stub.ConversaChat(chat_pb2.Retorno()):  
                print("[{}]: {}".format(resposta.dono, resposta.conteudo))  

    def envia_mensagem(self):
        name = input('Digite seu nome:')
        mensagem_digitada = 'Teste'
        if name != '':
            mensagem_enviada = chat_pb2.Mensagem()
            mensagem_enviada.dono = name
            mensagem_enviada.conteudo = mensagem_digitada
            print('Enviando mensagem. Dono:{}, Conteúdo:{}'.format(mensagem_enviada.dono, mensagem_enviada.conteudo))
            self.stub.EnviaMensagem(mensagem_enviada)   


    def enviar_credencial(self):
        servidor_cliente = 'localhost'
        porta_cliente = '50051'
        nome = input('Informe o nome:')

        #credencial = Credencial(nome.strip(), servidor_cliente.strip(), porta_cliente.strip())
        
        credencial = chat_pb2.Credencial()
        credencial.nome = nome.strip()
        credencial.servidor = servidor_cliente.strip()
        credencial.porta = porta_cliente.strip()
        
        self.stub.EnviaCredencial(credencial)
        

    

if __name__ == '__main__':
    logging.basicConfig()
    cliente = Cliente()