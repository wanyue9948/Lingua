from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI()
@app.route('/translate', methods=['POST'])
def translate():
    # Extracting data from POST request
    data = request.json
    source_text = data['text']
    target_language = data['targetLang']

    # Constructing the message for translation
    # Adjust the prompt as needed for your translation task
    prompt = f"Please ignore all previous instructions. Please respond only in the {target_language} language.\
      Do not explain what you are doing. Do not self reference. You are an expert translator. \
      Translate the following text to the {target_language} using vocabulary \
      and expressions of a native {target_language} speaker.Translate the following text : '{source_text}'"

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



if __name__ == '__main__':
    app.run(debug=True)  # Turn off debug in production
