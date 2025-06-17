import streamlit as st
import speech_recognition as sr
import wave
import tempfile
from collections import Counter

# Transcription vocale
def transcribe_and_save():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Parlez maintenant...")
        audio = r.listen(source)
        st.info("⏳ Transcription en cours...")

        # Sauvegarde audio temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            with wave.open(f.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(44100)
                wf.writeframes(audio.get_raw_data())
            audio_file_path = f.name

        try:
            text = r.recognize_google(audio, language="fr-FR")
            return text, audio_file_path
        except sr.UnknownValueError:
            return "❌ Je n'ai pas compris.", None
        except sr.RequestError:
            return "❌ Problème de connexion à l'API.", None

# Analyse simple du texte
def analyze_text(text):
    words = text.lower().split()
    count = len(words)
    most_common = Counter(words).most_common(5)
    return count, most_common

# Interface principale
def main():
    st.title("🗣️ Application de Reconnaissance Vocale Améliorée")
    st.write("Clique sur le bouton ci-dessous, parle, et découvre la transcription avec analyse.")

    if st.button("🎙️ Démarrer l'enregistrement"):
        transcription, audio_path = transcribe_and_save()
        st.subheader("📝 Transcription :")
        st.success(transcription)

        if audio_path:
            st.audio(audio_path, format="audio/wav")
            with open(audio_path, "rb") as file:
                st.download_button(label="⬇️ Télécharger l'audio", data=file, file_name="enregistrement.wav", mime="audio/wav")

        if transcription and "❌" not in transcription:
            word_count, top_words = analyze_text(transcription)
            st.subheader("📊 Analyse du texte :")
            st.write(f"Nombre de mots : {word_count}")
            st.write("Mots les plus fréquents :")
            for word, freq in top_words:
                st.write(f"- {word} : {freq} fois")

if __name__ == "__main__":
    main()
