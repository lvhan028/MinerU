import os
import json
import fire

from loguru import logger

from magic_pdf.pipe.UNIPipe import UNIPipe
from magic_pdf.rw.DiskReaderWriter import DiskReaderWriter

import magic_pdf.model as model_config 
model_config.__use_inside_model__ = True

# try:
#     current_script_dir = os.path.dirname(os.path.abspath(__file__))
#     demo_name = "demo1"
#     pdf_path = os.path.join(current_script_dir, f"{demo_name}.pdf")
#     model_path = os.path.join(current_script_dir, f"{demo_name}.json")
#     pdf_bytes = open(pdf_path, "rb").read()
#     # model_json = json.loads(open(model_path, "r", encoding="utf-8").read())
#     model_json = []  # model_json传空list使用内置模型解析
#     jso_useful_key = {"_pdf_type": "", "model_list": model_json}
#     local_image_dir = os.path.join(current_script_dir, 'images')
#     image_dir = str(os.path.basename(local_image_dir))
#     image_writer = DiskReaderWriter(local_image_dir)
#     pipe = UNIPipe(pdf_bytes, jso_useful_key, image_writer)
#     pipe.pipe_classify()
#     """如果没有传入有效的模型数据，则使用内置model解析"""
#     if len(model_json) == 0:
#         if model_config.__use_inside_model__:
#             pipe.pipe_analyze()
#         else:
#             logger.error("need model list input")
#             exit(1)
#     pipe.pipe_parse()
#     md_content = pipe.pipe_mk_markdown(image_dir, drop_mode="none")
#     with open(f"{demo_name}.md", "w", encoding="utf-8") as f:
#         f.write(md_content)
# except Exception as e:
#     logger.exception(e)

def process(pdf_list):
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    
    for index, pdf_path in enumerate(pdf_list):
        pdf_bytes = open(pdf_path, "rb").read()
   
        model_json = []  # model_json传空list使用内置模型解析
        
        jso_useful_key = {"_pdf_type": "", "model_list": model_json}
        local_image_dir = os.path.join(current_script_dir, 'images')
        image_dir = str(os.path.basename(local_image_dir))
        image_writer = DiskReaderWriter(local_image_dir)
        pipe = UNIPipe(pdf_bytes, jso_useful_key, image_writer)
        pipe.pipe_classify()
        """如果没有传入有效的模型数据，则使用内置model解析"""
        if len(model_json) == 0:
            if model_config.__use_inside_model__:
                pipe.pipe_analyze()
            else:
                logger.error("need model list input")
                exit(1)
        pipe.pipe_parse()
        md_content = pipe.pipe_mk_markdown(image_dir, drop_mode="none")
        with open(f"results/{index}.md", "w", encoding="utf-8") as f:
            f.write(md_content)

def file_ext(file_path):
    return os.path.splitext(file_path)[-1]


def main(file_path: str):
    pdf_list = []
    ext = file_ext(file_path)
    if ext == '.pdf':
        pdf_list.append(file_path)
        pdf_list *= 1
    elif ext == '.txt':
        with open(file_path) as f:
            file_paths = f.readlines()
            pdf_list += [_path for _path in file_paths if file_ext(_path) == '.pdf']
    else:
        print(f'unexpected input file_path: {file_path}')
        exit(-1)
    
    process(pdf_list)

if __name__ == '__main__':
    fire.Fire(main)