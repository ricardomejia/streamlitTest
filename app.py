import streamlit as st
import whisper
import os

# Función para transcribir el audio
def transcribe_audio(audio_file_path, model_name, progress_bar):
    # Cargar el modelo de Whisper según la elección del usuario
    model = whisper.load_model(model_name)
    # Procesar el archivo de audio
    result = model.transcribe(audio_file_path)
    # Completar la barra de progreso
    progress_bar.progress(100)
    return result["text"]

# Título de la aplicación
st.title('Transcripción de Audio con Whisper')

# Selector de modelo
model_option = st.selectbox(
    'Elige el modelo de Whisper',
    ('tiny', 'base', 'small', 'medium', 'large')  # Lista de modelos disponibles
)

# Carga de archivos
audio_file = st.file_uploader("Sube aquí tu archivo de audio", type=['mp3', 'wav', 'ogg', 'flac', 'mp4'])

if audio_file is not None:
    # Crea la carpeta tempDir si no existe
    if not os.path.exists('tempDir'):
        os.makedirs('tempDir')

    # Guardar el archivo de audio en el sistema de archivos
    audio_file_path = os.path.join('tempDir', audio_file.name)
    with open(audio_file_path, "wb") as f:
        f.write(audio_file.getbuffer())

    # Muestra el reproductor de audio
    st.audio(audio_file, format='audio/mp3', start_time=0)

    # Botón de transcripción
    if st.button('Transcribir'):
        # Inicializar la barra de progreso
        progress_bar = st.progress(0)
        with st.spinner('Transcribiendo...'):
            # Llamada a la función de transcripción con el modelo seleccionado
            transcription = transcribe_audio(audio_file_path, model_option, progress_bar)
            st.text_area('Transcripción', transcription, height=250)
