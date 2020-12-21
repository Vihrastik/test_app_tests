import ast
import random

import pytest

from src.common.consts import YamlTemplateData
from src.common.funcs import delete_all_templates
from src.common.template_api import (
    upload_template,
    get_templates_list,
    delete_template,
    install_template,
)
from src.common.utils import (
    generate_random_string,
    extract_name,
    extract_templates_list,
)


class TestUploadTemplates:
    def test_success_put_with_file_and_id(self):
        response = upload_template(file_name=YamlTemplateData.file_yaml.value.name,
                                   file=YamlTemplateData.file_yaml.value.data,
                                   data={'tmpl_id': str(random.randint(1, 10000000))})
        assert response.status_code == 201

    def test_success_put_without_id(self):
        response = upload_template(file_name=YamlTemplateData.file_yaml.value.name,
                                   file=YamlTemplateData.file_yaml.value.data)
        assert response.status_code == 201

    @pytest.mark.parametrize('file, data',
                             [(YamlTemplateData.file_docx.value.name, YamlTemplateData.file_docx.value.data),
                              (YamlTemplateData.file_exe.value.name, YamlTemplateData.file_exe.value.data),
                              ],
                             ids=['docx', 'exe'])
    def test_put_with_file_another_format(self, file, data):
        response = upload_template(file_name=file, file=data)
        assert response.status_code == 400

    def test_put_with_empty_file(self):
        response = upload_template(file_name=YamlTemplateData.file_yaml.value.name, file='')
        assert response.status_code == 400

    def test_put_with_empty_name_file(self):
        response = upload_template(file_name='', file=YamlTemplateData.file_yaml.value.data)
        assert response.status_code == 400

    def test_put_with_big_file(self):
        response = upload_template(file_name=YamlTemplateData.file_right_big.value.name,
                                   file=YamlTemplateData.file_right_big.value.data)
        assert response.status_code == 413

    def test_put_with_big_name_file(self):
        response = upload_template(file_name=generate_random_string(1000), file=YamlTemplateData.file_yaml.value.data)
        assert response.status_code == 400


class TestListTemplates:
    def test_success_get_list(self):
        response = get_templates_list()
        assert response.status_code == 200
        assert response.content


class TestDeleteTemplates:
    def test_success_delete_template(self):
        params = {
            'file_name': YamlTemplateData.file_yaml.value.name,
            'data': YamlTemplateData.file_yaml.value.data,
        }
        upload_template(file_name=params['file_name'], file=params['data'])
        short_name = extract_name(params['file_name'])
        response = delete_template(short_name)
        assert response.status_code == 200
        assert ast.literal_eval(response.text)['message'] == f'Template with tmpl_id={short_name} successfully deleted!'

    @pytest.mark.parametrize('file_name', [' ',
                                           generate_random_string(10),
                                           ],
                             ids=['empty_name', 'non_existent'])
    def test_delete_incorrect_template(self, file_name):
        response = delete_template(file_name)
        assert response.status_code == 404
        assert ast.literal_eval(response.text)['message'] == f'No template with tmpl_id={file_name} found!'


class TestInstallTemplates:
    @pytest.mark.parametrize('file, data',
                             [(YamlTemplateData.file_right_short.value.name,
                               YamlTemplateData.file_right_short.value.data),
                              (YamlTemplateData.file_right_one_full.value.name,
                               YamlTemplateData.file_right_one_full.value.data),
                              (YamlTemplateData.file_right_some_full.value.name,
                               YamlTemplateData.file_right_some_full.value.data),
                              (YamlTemplateData.file_reversible_depend.value.name,
                               YamlTemplateData.file_reversible_depend.value.data),
                              ],
                             ids=['right_short', 'right_one_full', 'right_some_full', 'reversible_dependency'])
    def test_success_install_template(self, file, data):
        upload_template(file_name=file, file=data)
        short_name = extract_name(file)
        response = install_template(short_name)
        assert response.status_code == 200

    @pytest.mark.parametrize('file_name', [' ',
                                           generate_random_string(10),
                                           ],
                             ids=['empty_name', 'non_existent'])
    def test_install_incorrect_template_name(self, file_name):
        response = install_template(file_name)
        assert response.status_code == 404
        assert ast.literal_eval(response.text)['message'] == f'No template with tmpl_id={file_name} found!'

        
class TestE2E:
    def test_create_and_check_template_list(self):
        params = {
            'file_name': YamlTemplateData.file_yaml.value.name,
            'data': YamlTemplateData.file_yaml.value.data,
        }
        upload_template(file_name=params['file_name'], file=params['data'])
        short_name = extract_name(params['file_name'])
        response = get_templates_list()
        assert short_name.encode() in response.content

    def test_create_and_delete_template(self):
        params = {
            'file_name': YamlTemplateData.file_yaml.value.name,
            'data': YamlTemplateData.file_yaml.value.data,
        }
        upload_template(file_name=params['file_name'], file=params['data'])
        short_name = extract_name(params['file_name'])
        delete_template(short_name)
        response = get_templates_list()
        assert short_name.encode() not in response.content

    def test_create_install_and_check_template_list(self):
        params = {
            'file_name': YamlTemplateData.file_right_short.value.name,
            'data': YamlTemplateData.file_right_short.value.data,
        }
        upload_template(file_name=params['file_name'], file=params['data'])
        short_name = extract_name(params['file_name'])
        install_template(short_name)
        response = get_templates_list()
        assert short_name.encode() in response.content

    def test_create_install_and_delete_template_without_data(self):
        params = {
            'file_name': YamlTemplateData.file_right_short.value.name,
            'data': YamlTemplateData.file_right_short.value.data,
        }
        upload_template(file_name=params['file_name'], file=params['data'])
        short_name = extract_name(params['file_name'])
        install_template(short_name)
        delete_template(short_name)
        response = get_templates_list()
        assert short_name.encode() not in response.content

    def test_create_install_and_delete_template_with_data(self):
        params = {
            'file_name': YamlTemplateData.file_right_short.value.name,
            'data': YamlTemplateData.file_right_short.value.data,
            'tmpl_id': str(random.randint(1, 10000000)),
        }
        upload_template(file_name=params['file_name'],
                        file=params['data'],
                        data={'tmpl_id': params['tmpl_id']})
        short_name = extract_name(params['file_name'])
        install_template(short_name)
        delete_template(short_name)
        response = get_templates_list()
        assert short_name.encode() not in response.content

    def test_delete_all_templates(self):
        params = {
            'file_name_1': YamlTemplateData.file_yaml.value.name,
            'data_1': YamlTemplateData.file_yaml.value.data,
            'file_name_2': YamlTemplateData.file_right_short.value.name,
            'data_2': YamlTemplateData.file_right_short.value.data,
        }
        upload_template(file_name=params['file_name_1'], file=params['data_1'])
        upload_template(file_name=params['file_name_2'], file=params['data_2'])
        delete_all_templates()
        response = get_templates_list()
        assert not extract_templates_list(response.content)
