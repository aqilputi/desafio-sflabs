import videotransf as vt
import json

class VideoTransfRoutines():
    """
    Classe para realizao de lista de tarefas de transformacoes
    armazenada em formato JSON
    """

    data = None # objeto json com as rotinas

    def __init__(self, filepath):
        try:
            with open('mensagens.json') as json_file:
                self.tasks = json.load(json_file)
        except Exception as ex:
            print(ex)



    def run(self):
        """ Executa todas as tarefas do objeto json"""

        for t in self.tasks:
            print(f'Video: {t["video"]}')
            print(f'Task: {t["task"]}')
            print(f'Parametros: {t["params"]}')

            # Tenta criar objeto de leitura
            # Caso nao exista, a tarefa eh ignorada
            try:
                transf = vt.VideoTransf(t['video'])
            except Exception as ex:
                print(ex)
                print("\nA tarefa foi ignorada...")
                continue


            transf.video_format = 'avi' # declara formato de escrita do arquivo como avi

            # Seleciona tipo de task
            if t['task'] == 'split':
                transf.split(self.tstamp_to_milisseconds(t['params']['timestamp']))

            if t['task'] == 'slice':
                transf.slice(self.tstamp_to_milisseconds(t['params']['timestamps'][0]),
                self.tstamp_to_milisseconds(t['params']['timestamps'][1]))

            if t['task'] == 'append':
                transf.append(t['params']['to_append'])

            print("pronto!\n\n")


    def tstamp_to_milisseconds(self, timestamp):
        """Transforma string de timestamp em milissegundos

        args:
            timestamp - string de tempo
        """
        
        ftr = [3600, 60, 1] # lista de segundos para transformar hrs, min, seg

        # separa horas, minutos e segundos, convert todos para segundos e soma
        return 1000*sum([a*b for a, b in
                         zip (ftr, [int(i) for i in
                                    timestamp.split(":")])])
