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



    def split(self, split_time):
        """Utiliza o metodo record para criar dois videos
        um do inicio ao split_time e o outro do split_time ateh o final

        args:
            split_time - inteiro contendo o tempo de split em milissegundo"""

        # primeira parte do split
        try:
            self.record(self.video_name + 'a.' + self.video_format,0 , split_time)
        except Exception as ex:
            print(ex)

        # segunda parte do split
        try:
            self.record(self.video_name + 'b.' + self.video_format, split_time)
        except Exception as ex:
            print(ex)

        return
        

    def record(self, name, begin_time, end_time=0):
        """Dado um valor inicial e um final, salva um trecho do video com o nome especificado

        args:
            name - string contendo o nome do arquivo a ser criado
            begin_time - inteiro contendo o inicio em milissegundos do seguimento
            end_time - inteiro contendo o final em milissegundos do seguimento"""

        # formato do video
        fourcc = cv.VideoWriter_fourcc(*'XVID')

        # calcula endtime real do video caso 0 seja especificado
        if end_time == 0:
            end_time = self.video_cap.get(cv.CAP_PROP_FRAME_COUNT)* self.video_cap.get(cv.CAP_PROP_FPS)


        # cria objeto de escrita utilizando os parametros do video de origem
        a_out = cv.VideoWriter(name, fourcc,
                               self.video_cap.get(cv.CAP_PROP_FPS),
                               (int(self.video_cap.get(cv.CAP_PROP_FRAME_WIDTH ))
                                ,int(self.video_cap.get(cv.CAP_PROP_FRAME_HEIGHT))))


        # enquanto a captura estiver sobre o tempo delimitado escreve os frames no novo arquvo
        while self.video_cap.get(cv.CAP_PROP_POS_MSEC) < end_time:
            ret, frame = self.video_cap.read()
            if not ret:
                raise Exception("Can't receive frame (stream end?). Exiting ...")

            a_out.write(frame) # escrita

        #libera objeto de escrita
        a_out.release()

        return
        

    def release(self):
        self.video_cap.release()
        
