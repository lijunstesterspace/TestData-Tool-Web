import os
import uuid
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB


def process_file(filepath, insert_str, position_mode, custom_pos):
    """文件处理核心逻辑"""
    filename = secure_filename(os.path.basename(filepath))
    name_part, ext = os.path.splitext(filename)

    if position_mode == 'prefix':
        new_name = f"{insert_str}{filename}"
    elif position_mode == 'suffix':
        new_name = f"{name_part}{insert_str}{ext}"
    elif position_mode == 'custom':
        pos = min(max(int(custom_pos), 0), len(name_part))
        new_name = f"{name_part[:pos]}{insert_str}{name_part[pos:]}{ext}"

    new_path = os.path.join(os.path.dirname(filepath), new_name)
    os.rename(filepath, new_path)
    return new_path


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        insert_str = request.form.get('insert_str', '')
        position_mode = request.form.get('position_mode', 'prefix')
        custom_pos = request.form.get('custom_pos', 0)

        # 创建临时目录
        session_id = str(uuid.uuid4())
        temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
        os.makedirs(temp_dir, exist_ok=True)

        # 处理文件
        processed_files = []
        for f in uploaded_files:
            if f.filename == '':
                continue
            temp_path = os.path.join(temp_dir, secure_filename(f.filename))
            f.save(temp_path)
            new_path = process_file(
                temp_path, insert_str, position_mode, custom_pos)
            processed_files.append(new_path)

        # 打包成ZIP
        zip_path = os.path.join(temp_dir, 'processed_files.zip')
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in processed_files:
                zipf.write(file, os.path.basename(file))

        return send_file(zip_path, as_attachment=True)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
