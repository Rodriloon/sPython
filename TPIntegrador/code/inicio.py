import streamlit as st
def main():
    # Título de la aplicación
    st.sidebar.title("CensAR")
    st.title("CensAR")
    st.markdown("---")
    st.write("La Encuesta Permanente de Hogares (EPH) es un relevamiento estadístico que recoge información sobre las características socioeconómicas de la población en hogares de Argentina. Contiene datos como edad, sexo, nivel educativo, situación laboral, tipo de ocupación, entre otros.")
    st.markdown("---")


if __name__ == "__main__":
    main()