
from concurrent import futures
import logging
import grpc
import chat_pb2_grpc
import chat_pb2


class Chat(chat_pb2_grpc.ChatServicer):

    def __init__(self):
        self.mensagens=[]

    def ConversaChat(self, request_iterator, context):
        index = 0
        while True:
            while len(self.mensagens) > index:
                mensagem = self.mensagens[index]
                index+=1
                yield mensagem
    
    def EnviaMensagem(self, request: chat_pb2.Mensagem, context):
        print('Mensagem recebida! Dono:{}, Conteúdo:{}'.format(request.dono, request.conteudo))
        self.mensagens.append(request)
        return chat_pb2.Retorno()
    
    def EnviaCredencial(self, request, context):
        linhas = []
        try:
            arquivo = open('dicio')
            linhas = arquivo.readlines()
        except:
            print('arquivo nao existe')
        finally:
            arquivo = open('dicio', 'w')
            for l in linhas:
                arquivo.write(l)
            arquivo.write('{}:{}:{}\n'.format(request.nome, request.servidor, request.porta))
            arquivo.close()
        
        return chat_pb2.Retorno()
    



def start_servidor():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(Chat(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig()
    start_servidor()