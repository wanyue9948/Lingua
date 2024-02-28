from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Mapping of language codes to voice names
voice_names = {
    'cn': 'zh-CN-YunyangNeural',
    'fi': 'fi-FI-HarriNeural',
    'en': 'en-US-RyanMultilingualNeural'
}

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("The OPENAI_API_KEY environment variable must be set.")
client = OpenAI(api_key=api_key)
# speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
# audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

def synthesize_speech(text, language):
    # Azure Speech Service credentials from environment variables
    speech_key = os.environ.get('SPEECH_KEY')
    speech_region = os.environ.get('SPEECH_REGION')
    if not speech_key or not speech_region:
        raise ValueError("Azure Speech Service credentials are not set in environment variables.")

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    if language == 'en':
        voice_name = voice_names['en']
    elif language == 'cn':
        voice_name = voice_names['cn']
    elif language == 'fi':
        voice_name = voice_names['fi']
    speech_config.speech_synthesis_voice_name = voice_name
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return "Speech synthesized successfully."
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        return f"Speech synthesis canceled: {cancellation_details.reason}"

@app.route('/translate', methods=['POST'])
def translate():
    # Extracting data from POST request
    data = request.json
    source_text = data['text']
    source_language = data['sourceLang']
    target_language = data['targetLang']

    # Constructing the message for translation
    # Adjust the prompt as needed for your translation task
    prompt = f"Please ignore all previous instructions. Please respond only in the {target_language} language.\
      Do not explain what you are doing. Do not self reference. You are an expert translator. \
      Just give me the answer of the translation, no other words\
      Translate the following text from {source_language} to the {target_language} using vocabulary \
      and expressions of a native {target_language} speaker.Translate the following text : '{source_text}'."


    # Make an API call to OpenAI's Chat Completions
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a native translator."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extracting the assistant's message from the response
        translated_text = response.choices[0].message.content
        translated_text = translated_text.replace('"', '')
        # print(response.choices[0].message.content)
        return jsonify(translated_text=translated_text)

    except Exception as e:
        # Handling exceptions and errors
        print(f"An error occurred: {e}")
        return jsonify(error=str(e)), 500

@app.route('/explain', methods=['POST'])
def explain():
    # 获取 POST 请求中的数据
    data = request.json
    text_to_explain = data['to_explain']
    source_language = data['sourceLang']
    explain_language = data['exLang']


    prompt = f"Explain the following {source_language} sentence: '{text_to_explain}' with grammar and vocubularies in {explain_language}, \
        your audience can only understand {explain_language} and a native {explain_language} speaker, \
                so make sure to expain everything only in {explain_language}."
    
    # 调用 ChatGPT API 进行解释
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are a language teacher."},
                {"role": "user", "content": prompt}
            ]
        )

        explanation = response.choices[0].message.content
        return jsonify(explanation=explanation)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify(error=str(e)), 500

@app.route('/speech', methods=['POST'])
def speak():
    try:
        data = request.json
        text = data['text']
        language = data.get('language')  # Default to English if language is not provided
        speech_result = synthesize_speech(text, language)
        return speech_result
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
