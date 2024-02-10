import streamlit as st
import random
import pandas as pd
import sys

class ObjetoVotacao:
  def __init__(self, nome, votos):
    self.nome = nome
    self.votos = votos

st.set_page_config(
  page_title="Top List",
  page_icon="👌",
  layout="centered"
)

def carregarDados(uploaded_file):
  dataframe = pd.read_csv(uploaded_file)
  st.write(dataframe)

  lista_objetos = [
      ObjetoVotacao(nome=row['Nome'], votos=0)
      for index, row in dataframe.iterrows()
  ]

  return lista_objetos


placeholder = st.empty()
placeholderTable = st.empty()

def dar_voto(opcao, lista):
  opcao.votos += 1
  draw(lista)

def draw(lista):
    with placeholder.container():
      st.markdown("<h1 style='text-align: center;'>Top List👌</h1>", unsafe_allow_html=True)
      st.write("---")
      for i in range(len(lista)):
        valores = [obj for obj in lista if obj.votos == i]
        
        if (len(valores) > st.session_state.grupos):
          break

      if len(valores) > 1:
          col1, col2, col3 = st.columns(3, gap="large")
          opcoes = random.sample(valores, 2)

          with col1:
            st.button(opcoes[0].nome, on_click=lambda: dar_voto(opcoes[0], lista), key=random.randint(1, sys.maxsize))

          with col2:
            st.button(opcoes[1].nome, on_click=lambda: dar_voto(opcoes[1], lista), key=random.randint(1, sys.maxsize))
          
          with col3:
            st.button("🤔", on_click=lambda: dar_voto(opcoes[random.randint(0,1)], lista), key=random.randint(1, sys.maxsize))
      else:
        df = pd.DataFrame([{'nome': obj.nome, 'votos': obj.votos} for obj in st.session_state.lista])
        df = df.sort_values(by='votos', ascending=False)
        
        st.dataframe(data=df, hide_index=True)

def main():
  if ("lista" not in st.session_state):
    st.markdown("<h1 style='text-align: center;'>Top List👌</h1>", unsafe_allow_html=True)
    st.write("---")
    number = st.number_input('Inserir grupos', step=1, value=1, min_value=1)
    
    uploaded_file = st.file_uploader("Selecione o arquivo", type=["csv"])
  
    if uploaded_file is not None:
      st.session_state.lista = carregarDados(uploaded_file)
      st.session_state.grupos = number
      st.rerun()
  else:
    draw(st.session_state.lista)

if __name__ == "__main__":
  main()