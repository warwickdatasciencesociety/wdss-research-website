"""Script to convert source notebooks to markdown and format correctly."""

import re
import os
import platform
import shutil
import subprocess

if not os.path.exists('source/_posts'):
    os.mkdir('source/_posts')

for post in os.listdir('content'):
    # check notebook exists
    notebook_path = f"content/{post}/{post}.ipynb"
    if not os.path.exists(notebook_path):
        raise RuntimeError(f"could not find notebook for post {post}")

    # convert to markdown
    system = platform.system()
    if system == 'Windows':
        process = subprocess.Popen([
            'jupyter', 'nbconvert',
            notebook_path,
            '--to', 'markdown', '--template=build/markdown_with_captions.tpl',
            '--TagRemovePreprocessor.enabled=True',
            "--TagRemovePreprocessor.remove_cell_tags=['remove_cell']",
            "--TagRemovePreprocessor.remove_input_tags=['remove_input']",
            "--TagRemovePreprocessor.remove_single_output_tags=['remove_single_output']",
            "--TagRemovePreprocessor.remove_all_outputs_tags=['remove_all_output']",
        ], shell=True)
    elif system == 'Linux':
        process = subprocess.Popen(' '.join([
            'jupyter nbconvert',
            notebook_path,
            '--to markdown',
            '--template=build/markdown_with_captions.tpl',
            '--TagRemovePreprocessor.enabled=True',
            "--TagRemovePreprocessor.remove_cell_tags=\"['remove_cell']\"",
            "--TagRemovePreprocessor.remove_input_tags=\"['remove_input']\"",
            "--TagRemovePreprocessor.remove_single_output_tags=\"['remove_single_output']\"",
            "--TagRemovePreprocessor.remove_all_outputs_tags=\"['remove_all_output']\"",
        ]), shell=True)
    else:
        raise NotImplementedError("build does currently not support system")
    process.wait()
    
    markdown_path = f'content/{post}/{post}.md'
    image_dir_path = f'content/{post}/{post}_files/'

    with open(markdown_path, 'r', encoding='utf8') as file:
        file_data = file.read()

    # correct image paths
    file_data = re.sub(f'{post}_files/', f'/images/{post}/', file_data)

    # remove captions
    # file_data = re.sub(r'!\[\w+\]', '![]', file_data)

    # remove additional table formatting
    file_data = re.sub('table border="1" class="dataframe"', 'table', file_data)
    file_data = re.sub('tr style="text-align: right;"', 'tr', file_data)
    file_data = re.sub(r'</table>[\r\n]{1,2}</div>', '</table>', file_data)
    file_data = re.sub(r'<div>.*?</style>', '', file_data, flags=re.DOTALL)

    with open(markdown_path, 'w', encoding='utf8') as file:
        file.write(file_data)

    # move files
    shutil.move(markdown_path, f'source/_posts/{post}.md')
    target_image_dir_path = f'source/images/{post}/'
    if not os.path.exists(target_image_dir_path):
        os.mkdir(target_image_dir_path)
    else:
        for image in os.listdir(target_image_dir_path):
            if re.match(post, image):
                os.remove(f'{target_image_dir_path}{image}')
    for image in os.listdir(image_dir_path):
        shutil.move(f'{image_dir_path}{image}', f'{target_image_dir_path}')
    os.rmdir(image_dir_path)
