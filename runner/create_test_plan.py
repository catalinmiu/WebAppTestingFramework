import argparse
import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append('{}/..'.format(current_dir))
# sys.path.append('{}/../../..'.format(current_dir))


def get_class(module_name, class_name):
    """
    Get a class object from a given module

    :type module_name: str
    :type class_name: str
    :param module_name: The name of an existing module that can be imported from the current working directory
    :param class_name: The name of a class defined in the module
    :rtype: type
    :return: An object of type <class_name> if found in <module_name>; otherwise None
    """

    try:
        module = __import__(module_name)
    except ImportError:
        raise ImportError('Failed to import module: {module_name}'.format(module_name=module_name))

    module_dict = module.__dict__
    class_list = [module_dict[key] for key in module_dict
                  if isinstance(module_dict[key], type)
                  and module_dict[key].__module__ == module.__name__]

    for clazz in class_list:
        if clazz.__name__ == class_name:
            return clazz

    return None


def get_class_names(module_name):
    """
    Get a list of str containing all the classes in a given module

    :type module_name: str
    :param module_name: The name of an existing module that can be imported from the current working directory
    :rtype: list
    :return: Contains str corresponding to the name of each class in a given module (does not go up inheritance ladder)
    """

    try:
        module = __import__(module_name)
    except ImportError:
        raise ImportError('Failed to import module: {module_name}'.format(module_name=module_name))

    module_dict = module.__dict__
    return [
        module_dict[key].__name__
        for key in module_dict
        if isinstance(module_dict[key], type)
           and module_dict[key].__module__ == module.__name__
    ]


def get_classes(module_name):
    """
    Get a list of class objects housed within a given module

    :type module_name: str
    :param module_name: The name of an existing module that can be imported from the current working directory
    :rtype: list
    :return: Contains class/type objects: One for each class in the module (does not go up inheritance ladder)
    """

    try:
        module = __import__(module_name)
    except ImportError:
        raise ImportError('Failed to import module: {module_name}'.format(module_name=module_name))

    module_dict = module.__dict__
    return [
        module_dict[key]
        for key in module_dict if isinstance(module_dict[key], type) and module_dict[key].__module__ == module.__name__]


class TestPlanKeys(object):
    FEATURES = 'features'
    TEST_PLAN_NAME = 'test_plan'
    TAGS = 'tags'
    MODULES_LIST = 'modules'
    MODULE_NAME = 'module_name'
    CLASSES_LIST = 'classes'
    CLASS_NAME = 'class_name'
    TESTS_LIST = 'tests'
    TEST_NAME = 'test_name'
    TEST_DOCSTRING = 'test_docstring'


class TestPlanGenerator(object):
    """
    Generates an HTML-based test plan document
    """
    #
    def __init__(self,
                 # name,
                 # description,
                 modules_list,
                 # required_tags_list,
                 # any_tags_list,
                 # excluded_tags_list,
                 # required_features_list,
                 # any_features_list,
                 # excluded_features_list
                 ):

        # self.name = name
        # self.description = description
        self.modules_list = modules_list

        # self.required_tags_list = required_tags_list
        # self.any_tags_list = any_tags_list
        # self.excluded_tags_list = excluded_tags_list
        #
        # self.required_features_list = required_features_list
        # self.any_features_list = any_features_list
        # self.excluded_features_list = excluded_features_list

    def generate_test_plan_json(self):
        """
        Generate the test plan JSON

        Format:
        {
            'test_plan': '<test plan name>',
            'modules': [
               {
                    'module_name': '<module name>',
                    'classes': [
                        {
                            'class_name': '<class name>',
                             'tests': [
                                {
                                    'test_tags': ['TAG_NAME_1', ..., 'TAG_NAME_N'],
                                    'test_features': ['TEST_FEATURE_1', ..., 'TEST_FEATURE_N'],
                                    'test_name': '<test name>',
                                    'test_docstring': '<test docstring>'
                                },
                                {...}  # more test methods
                            ]
                        },
                        {...}  # more classes
                    ]
                }
                {...}  # more modules
            ]
        }

        :rtype: dict
        :return: Dict that is compliant with JSON format
        """

        test_plan_json = {
            # TestPlanKeys.TEST_PLAN_NAME: self.name,
            TestPlanKeys.MODULES_LIST: []
        }
        import pdb; pdb.set_trace()
        for module_name in self.modules_list:
            module_dict = {
                TestPlanKeys.MODULE_NAME: module_name,
                TestPlanKeys.CLASSES_LIST: []
            }
            test_plan_json[TestPlanKeys.MODULES_LIST].append(module_dict)

            for class_object in get_classes(module_name):
                class_dict = {
                    TestPlanKeys.CLASS_NAME: class_object.__name__,
                    TestPlanKeys.TESTS_LIST: []
                }
                module_dict[TestPlanKeys.CLASSES_LIST].append(class_dict)

                for test_method_name, test_method_object in inspect.getmembers(class_object):
                    if test_method_name.startswith('test_') is False or test_method_name == 'test_config_network_types':
                        continue

                    tags = []
                    if TestPlanKeys.TAGS in dir(test_method_object):
                        tags = test_method_object.tags

                    test_dict = {
                        TestPlanKeys.TEST_NAME: test_method_name,
                        TestPlanKeys.TEST_DOCSTRING: test_method_object.__doc__,
                        TestPlanKeys.TAGS: [tag.name for tag in tags],
                    }
                    class_dict[TestPlanKeys.TESTS_LIST].append(test_dict)

        return test_plan_json


if __name__ == '__main__':
    TestPlanGenerator(['projects']).generate_test_plan_json()
