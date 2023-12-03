from flask import Flask, request, jsonify
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator

app = Flask(__name__)

@app.route('/api/translate', methods=['POST'])
def translate_pdf():
    # Extracting data from the request
    source_pdf = request.form.get('source_pdf')
    dest_pdf = request.form.get('dest_pdf')
    target_lang = request.form.get('target_lang')

    if not all([source_pdf, dest_pdf, target_lang]):
        return jsonify({'error': 'Missing parameters'}), 400

    # Here, you would add the logic to handle the PDF translation
    # For instance, calling a function like:
    # translate_pdf_file(source_pdf, dest_pdf, target_lang)
    translator.translate_pdf(source_pdf,"pdf",target_lang,dest_pdf)

    # Placeholder response
    response = {
        'source_pdf': source_pdf,
        'dest_pdf': dest_pdf,
        'target_lang': target_lang,
        'status': 'Translation started'
    }

    return jsonify(response)

if __name__ == '__main__':
    argument_parser = ArgumentParser()
    args = argument_parser.parse_arguments()
    config_loader = ConfigLoader(args.config)

    config = config_loader.load_config()

    if args.model_type == "OpenAIModel":
        model_name = args.openai_model if args.openai_model else config['OpenAIModel']['model']
        api_key = args.openai_api_key if args.openai_api_key else config['OpenAIModel']['api_key']
        model = OpenAIModel(model=model_name, api_key=api_key)
    elif args.model_type == "GLMModel":
        timeout = args.timeout if args.timeout else config['GLMModel']['timeout']
        model_url = args.model_url if args.model_url else config['GLMModel']['model_url']
        model = GLMModel(model_url=model_url, timeout=timeout)
    else:
        raise ValueError("Invalid model_type specified. Please choose either 'GLMModel' or 'OpenAIModel'.")


    pdf_file_path = args.book if args.book else config['common']['book']
    file_format = args.file_format if args.file_format else config['common']['file_format']

    # 实例化 PDFTranslator 类，接受API请求时调用 translate_pdf() 方法
    translator = PDFTranslator(model)

    app.run(debug=True)

