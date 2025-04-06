import streamlit as st
import sqlite3
import pandas as pd

# Conexión a base de datos (en la raíz, no en subcarpeta)
conn = sqlite3.connect("vocabulario.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS palabras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ingles TEXT NOT NULL,
        espanol TEXT NOT NULL,
        tipo TEXT NOT NULL
    )
""")
conn.commit()

# Guardar palabra
def guardar_palabra(ingles, espanol, tipo):
    cursor.execute("INSERT INTO palabras (ingles, espanol, tipo) VALUES (?, ?, ?)", (ingles, espanol, tipo))
    conn.commit()

# Eliminar palabra
def borrar_palabra(id_palabra):
    cursor.execute("DELETE FROM palabras WHERE id = ?", (id_palabra,))
    conn.commit()

# Interfaz web con Streamlit
st.set_page_config(page_title="Vocabulario Inglés", layout="wide")
st.title("📘 Mi Vocabulario de Inglés")

with st.form("formulario"):
    col1, col2, col3 = st.columns([3, 3, 2])
    with col1:
        ingles = st.text_input("Palabra en inglés")
    with col2:
        espanol = st.text_input("Traducción en español")
    with col3:
        tipo = st.selectbox("Tipo de palabra", [
            "Sustantivo", "Verbo - Presente", "Verbo - Pasado", "Verbo - Participio", "Verbo - Gerundio",
            "Adjetivo", "Adverbio", "Contracción", "Artículo definido", "Artículo indefinido",
            "Pronombre", "Preposición", "Conjunción", "Interjección", "Expresión", "Otro"
        ])

    guardar = st.form_submit_button("Guardar")
    if guardar:
        if ingles.strip() == "" or espanol.strip() == "":
            st.warning("⚠️ Completa todos los campos antes de guardar.")
        else:
            guardar_palabra(ingles.strip(), espanol.strip(), tipo)
            st.success("✅ Palabra guardada correctamente.")

st.divider()

# Mostrar lista
st.subheader("📋 Palabras guardadas")

df = pd.read_sql_query("SELECT * FROM palabras ORDER BY ingles", conn)
if df.empty:
    st.info("No hay palabras guardadas aún.")
else:
    st.dataframe(df, use_container_width=True)

    # Eliminar palabra
    st.write("Selecciona el ID de una palabra para eliminar:")
    id_a_borrar = st.number_input("ID", min_value=1, step=1)
    if st.button("🗑️ Borrar palabra"):
        borrar_palabra(id_a_borrar)
        st.success("✅ Palabra eliminada.")
        st.experimental_rerun()