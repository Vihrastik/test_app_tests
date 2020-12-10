from src.common.consts import YamlTemplateData
from src.common.template_api import (
    upload_template,
    get_templates_list,
    delete_template,
    install_template,
)
from src.common.utils import (
    extract_name,
    extract_templates_list,
)


def set_template(name, data):
    upload_template(file_name=name, file=data)
    short_name = extract_name(name)
    install_template(short_name)


def create_templ_with_one_button_not_clickable():
    params = {
        'file_name': YamlTemplateData.file_right_short.value.name,
        'data': YamlTemplateData.file_right_short.value.data,
    }
    set_template(params['file_name'], params['data'])


def create_templ_with_one_button_clickable():
    params = {
        'file_name': YamlTemplateData.file_right_one_full.value.name,
        'data': YamlTemplateData.file_right_one_full.value.data,
    }
    set_template(params['file_name'], params['data'])


def create_templ_with_hundred_button_clickable():
    params = {
        'file_name': YamlTemplateData.file_right_hundred_items.value.name,
        'data': YamlTemplateData.file_right_hundred_items.value.data,
    }
    set_template(params['file_name'], params['data'])


def delete_all_templates():
    templates = extract_templates_list(get_templates_list().content)
    for template in templates:
        delete_template(template)


def create_templ_with_large_button_clickable():
    params = {
        'file_name': YamlTemplateData.file_right_some_full.value.name,
        'data': YamlTemplateData.file_right_some_full.value.data,
    }
    set_template(params['file_name'], params['data'])
