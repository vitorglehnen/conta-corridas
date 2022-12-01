import tkinter.messagebox
from tkcalendar import DateEntry
from tkinter import *
import pandas as pd
from pyodbc import connect

janela1 = Tk()
janela1.title("Gerenciador de Corridas")


def cria_botao(janela, texto, comando, coluna, linha, x, y, sticky):
    Button(janela, text=texto, command=comando).grid(column=coluna, row=linha, padx=x, pady=y, sticky=sticky)


def cria_texto(janela, texto, coluna, linha, padx, pady, sticky):
    Label(janela, text=texto).grid(column=coluna, row=linha, padx=padx, pady=pady, sticky=sticky)


class Janela1:
    def __init__(self):
        self.banco_de_dados()
        self.contador_de_corridas()
        self.soma_km()
        self.layout_1()
        self.mostra_dados()

    def captura_dados(self):
        self.km_capturado = self.entrada_km.get()
        self.dia_capturado = self.entrada_dia.get()
        self.pace_capturado = self.entrada_pace.get()

        self.insere_dados(self.dia_capturado, self.km_capturado, self.pace_capturado)

        self.entrada_pace.delete(0, 90)
        self.entrada_km.delete(0, 90)

        self.soma_km()
        self.contador_de_corridas()
        self.layout_1()

    def layout_1(self):
        cria_texto(janela1, 'Quilômetros', 0, 0, 0, 5, W)
        cria_texto(janela1, 'Pace', 0, 1, 0, 5, E)

        self.entrada_km = Entry(janela1, width=10)
        self.entrada_km.focus()
        self.entrada_km.grid(column=1, row=0)

        self.entrada_pace = Entry(janela1, width=10)
        self.entrada_pace.grid(column=1, row=1)

        self.entrada_dia = DateEntry(janela1)
        self.entrada_dia.grid(column=1, row=2)

        cria_botao(janela1, 'Adicionar corrida!', self.captura_dados, 1, 3, 0, (20, 0), None)
        cria_botao(janela1, 'Estatísticas', Janela2, 2, 0, (50, 0), 0, None)

    def banco_de_dados(self):
        dados_conexao = (
            "Driver={SQL Server};" "Server=VITOR;" "Database=corridas_vitor;")
        conexao = connect(dados_conexao)
        self.cursor = conexao.cursor()

    def insere_dados(self, data, km, pace):
        self.comando = f"""INSERT INTO Quilometragem(data_corrida, km, pace)
VALUES
    ('{data}', {km}, '{pace}')"""

        self.cursor.execute(self.comando)
        self.cursor.commit()

    def contador_de_corridas(self):
        self.cursor.execute(f'SELECT * FROM Quilometragem')
        self.linhas = len(self.cursor.fetchall())
        self.cursor.commit()

    def soma_km(self):
        self.cursor.execute(f'select sum(km) from Quilometragem')
        self.total_km = self.cursor.fetchval()
        self.cursor.commit()

    def apaga_dados(self):
        self.cursor.execute('TRUNCATE TABLE QUILOMETRAGEM')
        self.cursor.commit()
        self.contador_de_corridas()
        self.soma_km()
        self.layout_1()
        self.janela2.destroy()

    def mostra_dados(self):
        self.cursor.execute("""SELECT * FROM Quilometragem""")

        self.lista_db = []
        self.mostra_o_banco = self.cursor.fetchall()
        for linha in self.mostra_o_banco:
            linha = list(linha)
            self.lista_db.append(linha)

        self.columns = ['Data', 'KM', 'Pace']
        self.df = str(pd.DataFrame(self.lista_db, columns=self.columns))

class Janela2(Janela1):
    def __init__(self):
        super().__init__()
        self.janela2 = Tk()
        self.janela2.title("ESTATÍSTICAS DAS CORRIDAS")
        self.mostra_dados()
        self.mostra_meta()
        self.layout_2()

    def layout_2(self):
        cria_botao(self.janela2, 'Apagar todas as corridas', self.cria_aviso, 0, 0, 0, 0, N)
        cria_botao(self.janela2, 'Definir meta', self.altera_meta, 0, 6, 0, 0, W)

        cria_texto(self.janela2, self.df, 1, 0, (100, 10), 0, N)
        cria_texto(self.janela2, f'Total de corridas: {self.linhas}', 0, 2, 0, 0, W)
        cria_texto(self.janela2, f'Meta: {self.meta}', 0, 3, 0, 0, W)

        if self.total_km == None:
            cria_texto(self.janela2, f'Total de KM: 0', 0, 4, 0, 0, W)
        else:
            cria_texto(self.janela2, f'Total de KM: {self.total_km}', 0, 4, 0, 0, W)

        self.entrada_meta = Entry(self.janela2, width=5, bd=3)
        self.entrada_meta.grid(column=0, row=5, pady=(20, 0), sticky=W)

    def cria_aviso(self):
        self.aviso = tkinter.messagebox.askquestion(title='Apagar corridas', message='Deseja apagar todas as corridas?')
        if self.aviso == 'yes':
            self.apaga_dados()

    def altera_meta(self):
        self.valor_meta_capturado = int(self.entrada_meta.get())
        self.cursor.execute(f"""UPDATE Metas SET meta = {self.valor_meta_capturado}""")
        self.entrada_meta.delete(0, 90)
        self.mostra_meta()
        self.layout_2()
        self.cursor.commit()

    def mostra_meta(self):
        self.cursor.execute('SELECT * FROM Metas')
        self.meta = self.cursor.fetchval()
        self.cursor.commit()


Janela1()
janela1.mainloop()
