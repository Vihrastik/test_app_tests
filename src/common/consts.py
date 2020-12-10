from enum import Enum

from src.common.utils import generate_random_string


class TemplException(AssertionError):
    pass


class YamlTemplate:
    """
    Моделька Yaml файла.
    """
    def __init__(self, name, data):
        self.name = name
        self.data = data


class YamlTemplateData(Enum):
    file_right_short = YamlTemplate('file_right_short.yaml', ' -  id: 1\n    label: test')
    file_right_one_full = YamlTemplate('file_r_one_f.yaml', ' -  id: 1\n    label: test\n    link: test_link\n    '
                                                           'depends: 1')
    file_right_some_full = YamlTemplate('file_r_some_f.yaml',
                                       ''.join(f' -  id: {i}\n    '
                                               f'label: {generate_random_string(500)}\n    '
                                               f'link: {generate_random_string(500)}\n    '
                                               f'depends: 1\n'
                                               for i in range(100)))
    file_right_big = YamlTemplate('file_right_big.yaml',
                                 ''.join(f' -  id: {generate_random_string(100)}\n    '
                                         f'label: {generate_random_string(100)}\n    '
                                         f'link: {generate_random_string(100)}\n    '
                                         f'depends: {generate_random_string(100)}\n'
                                         for i in range(1000)))
    file_right_hundred_items = YamlTemplate('file_right_hundred.yaml',
                                           ''.join(f' -  id: {i}\n    '
                                                   f'label: test_label{i}\n    '
                                                   f'link: test_link{i}\n    '
                                                   f'depends: {i}\n' for i in range(100)))
    file_yaml = YamlTemplate('usual_file.yaml', 'id: 1')
    file_docx = YamlTemplate('test_doc.docx', ' ')
    file_exe = YamlTemplate('test_doc.exe', ' ')
    file_invalid = YamlTemplate('file_invalid.yaml', 'a=3')
    file_invalid_depend = YamlTemplate('file_invalid_depend.yaml', ' -  id: 1\n    label: 1\n    depends: a')
    file_wrong_depend = YamlTemplate('file_wrong_depend.yaml', ' -  id: 1\n    label: 1\n    depends: 2\n -  id: 2'
                                                              '\n    label: 2\n    depends: 3')
    file_reversible_depend = YamlTemplate('file_reversible_depend.yaml', ' -  id: 1\n    label: 1\n    depends: 2\n -  '
                                                                        'id: 2\n    label: 2\n    depends: 1')
    file_no_label_value = YamlTemplate('file_no_lab_value.yaml', ' -  id: 1\n    label:\n    depends: 1')
    file_no_id_value = YamlTemplate('file_no_id_value.yaml', ' -  id:\n    label:\n    depends: 1')
    file_no_label = YamlTemplate('file_no_lab.yaml', ' -  id: 1')
    file_no_id = YamlTemplate('file_no_id.yaml', ' -  label: 1')

    file_two_similar_id = YamlTemplate('file_two_similar_id.yaml', ' -  id: 1\n -  id: 1\n')
