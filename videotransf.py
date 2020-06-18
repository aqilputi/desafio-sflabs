import cv2 as cv
import numpy as np
import ntpath

class VideoTransf():
    """Classe para para algumas transformacoes em video"""

    """split: quebra o video em duas partes e as salva em arquivos separados
       slice: retira um trecho do video a o salva em um arquivo separado
       append: junta o video selecionado a um terceiro video e salva em um arquivo separado"""

    video_path = None    # caminho relativo do video selecionado
    video_name = None    # nome do video
    video_format = None  # extensao do arquivo

    video_cap = None     # Objeto cv.VideoCaptura para tratar o video

    def __init__(self, path):
        # Manipula o path do arquivo para resgatar o nomee extensao
        self.video_path = path
        self.video_name = ntpath.basename(path)[:-4]
        self.video_format = path[-3:]

        # cria objeto de video
        try:
            self.video_cap = cv.VideoCapture(path)
        except Exception as ex:
            print(f'An Error occurred while opening the video file:\n{ex}')

        if not self.video_cap.isOpened():
            raise FileNotFoundError("Wrong file or file path")


    def slice(self, begin_time, end_time):
        """Utiliza o metodo record para criar um segmento de video
        com nome nome_do_arquivo + 'c'

        args:
            begin_time - inteiro identificando o tempo inicial do seguimento em milissegundos
            end_time - inteiro identificando o tempo final do seguimento em milissegundo

        """

        # cria arquivo com seguimento
        try:
            self.record(self.video_name + 'c.' + self.video_format, begin_time, end_time)
        except Exception as ex:
            print(ex)

        return
    
    def append(self, video_toappend):
        """Junta o video com um outro arquivo de video terceiro passado por argumento

        args:
            video_toappend - caminho do segundo video a ser unido com o primeiro
"""

        try:
            rec = self.record(self.video_name + 'd.' + self.video_format, release=False)
        except Exception as ex:
            print(f'An error occurred during the first video recording:\n{ex}')


        try:
            othervideo = VideoTransf(video_toappend)
            othervideo.record(video_writer=rec, release=True)
        except Exception as ex:
            print(f'An error occurred during the second video appending:\n{ex}')
        else:
            othervideo.release()




    def split(self, split_time):
        """Divide o video em dois e cria dois novos arquivos de video,
        um do inicio ao split_time e o outro do split_time ateh o final,
        com nomes nome_do_arquivo + 'a' e nome_do_arquiv + 'b' respectivamente

        args:
            split_time - inteiro identificando o tempo de split em milissegundo"""

        # primeira parte do split
        try:
            self.record(self.video_name + 'a.' + self.video_format, 0, split_time)
        except Exception as ex:
            print(ex)

        # segunda parte do split
        try:
            self.record(self.video_name + 'b.' + self.video_format, split_time)
        except Exception as ex:
            print(ex)

        return
        

    def record(self, name=None, begin_time=0, end_time=0, video_writer=None, release=True):
        """Dado um valor inicial e um final, salva um trecho do video com o nome especificado

        args:
            name - string identificando o nome do arquivo a ser criado
            begin_time - inteiro identificando o inicio em milissegundos do seguimento
            end_time - inteiro identificando o final em milissegundos do seguimento"""

        if not video_writer:
            # formato do video
            fourcc = cv.VideoWriter_fourcc(*'XVID')

            # cria objeto de escrita utilizando os parametros do video de origem
            video_writer = cv.VideoWriter(name, fourcc,
                                   self.video_cap.get(cv.CAP_PROP_FPS),
                                   (int(self.video_cap.get(cv.CAP_PROP_FRAME_WIDTH ))
                                    ,int(self.video_cap.get(cv.CAP_PROP_FRAME_HEIGHT))))

        # calcula endtime real do video caso 0 seja especificado
        if end_time == 0:
            end_time = self.video_cap.get(cv.CAP_PROP_FRAME_COUNT)* self.video_cap.get(cv.CAP_PROP_FPS)



        # enquanto a captura estiver sobre o tempo delimitado escreve os frames no novo arquivo
        while self.video_cap.get(cv.CAP_PROP_POS_MSEC) < end_time:
            ret, frame = self.video_cap.read()
            if not ret:
                raise Exception("Can't receive frame (stream end?). Exiting ...")

            video_writer.write(frame) # escrita

        if release == True:
            #libera objeto de escrita
            video_writer.release()
            return
        else:
            return video_writer
        
        

    def release(self):
        """Libera objeto de leitura"""
        self.video_cap.release()
        
