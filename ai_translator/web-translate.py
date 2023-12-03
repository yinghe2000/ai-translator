from flask import Flask, render_template, request, redirect, url_for, flash
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_pdf():
    source_pdf = request.form.get('source_pdf')
    dest_pdf = request.form.get('dest_pdf')
    target_lang = request.form.get('target_lang')

    if not all([source_pdf, dest_pdf, target_lang]):
        flash('All fields are required!', 'error')
        return redirect(url_for('index'))

    # Here you should add your actual PDF translation logic
    flash(f'Translation of {source_pdf} to {target_lang} started. Output will be saved as {dest_pdf}', 'success')
    translator.translate_pdf(source_pdf,"pdf",target_lang,dest_pdf)

    return redirect(url_for('index'))

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

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    app.run(debug=True)

