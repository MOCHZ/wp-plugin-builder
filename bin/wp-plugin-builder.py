#!/usr/bin/env python
import re
import os
import sys
import errno
import datetime


def main():
    plugin_name = raw_input('Plugin Name: ')
    target_dir = raw_input('Plugin Target Directory: ')

    try:
        target_dir
    except NameError:
        target_dir = 'tmp'

    # CREATE PLUGIN DIRECTORIES
    try:
        _create_directories(plugin_name, target_dir)
    except RuntimeWarning:
        _warn('Unexpected error occurred while creating plugin directories')

    # GENERATE PLUGIN FILES
    try:
        _populate_directories(plugin_name, target_dir)
    except RuntimeWarning:
        _warn('Unexpected error occurred while populating plugin directories')

    return


def _create_directories(plugin_name, target_dir):
    plugin_name = re.sub(r'[ ._]', '-', plugin_name.lower())

    root = os.path.join(target_dir, plugin_name)
    includes = os.path.join(root, 'includes')
    css = os.path.join(includes, 'css')
    templates = os.path.join(includes, 'templates')
    classes = os.path.join(includes, 'classes')

    if not os.path.exists(root):
        try:
            os.makedirs(root)
            os.makedirs(includes)
            os.makedirs(css)
            os.makedirs(templates)
            os.makedirs(classes)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
    else:
        _warn('The root directory: ' + root + ' already exists')

    return


def _populate_directories(plugin_name, target_dir):
    ps = os.path.sep
    plugin_name = re.sub(r'[ ._]', '-', plugin_name.lower())

    script_root = os.path.dirname(os.path.realpath(__file__))
    template_files = script_root + ps + '..' + ps + 'templates' + ps

    # DIRECTORIES
    root = os.path.join(target_dir, plugin_name, 'includes')
    css = os.path.join(root, 'css')
    classes = os.path.join(root, 'classes')

    # USER INPUT
    author = raw_input('Author Name: ')
    email = raw_input('Authors Email: ')
    plugin_uri = raw_input('Plugin URI: ')
    package = raw_input('Package Name: ')
    desc = raw_input('Plugin Description: ')

    # REGEX PATTERNS
    regex = [{'plugin_name': plugin_name},
             {'plugin_var': _create_plugin_var(plugin_name)},
             {'plugin_name_upper': _create_presentation(plugin_name).upper()},
             {'plugin_name_presentation': _create_presentation(plugin_name)},
             {'copyright': author + ' (c) ' + str(datetime.datetime.now().year)},
             {'plugin_uri': plugin_uri},
             {'package': package},
             {'author': author},
             {'email': '<' + email + '>'},
             {'description': desc},
             {'class_name': _create_class(plugin_name)},
             {'class_file': _create_class_filename(plugin_name)}]

    # CREATE CSS FILE FROM TEMPLATE
    css_file = css + ps + 'styles.css'
    css_template = template_files + 'css.tmpl'
    _create_file_from_template(css_file, css_template, regex, 'CSS file already exists, this should not be possible!')

    # CREATE PHP CLASS FROM TEMPLATE
    class_file = classes + ps + _create_class_filename(plugin_name)
    class_template = template_files + 'class.tmpl'
    _create_file_from_template(class_file, class_template, regex, 'PHP class file already exists, this should not be possible!')

    # CREATE MAIN PLUGIN FILE
    plugin_file = target_dir + ps + plugin_name + ps + plugin_name + '.php'
    plugin_template = template_files + 'plugin.tmpl'
    _create_file_from_template(plugin_file, plugin_template, regex, 'Plugin file already exists, this should not be possible!')

    # CREATE INDEX FILE
    index_file = target_dir + ps + plugin_name + ps + 'index.php'
    index_template = template_files + 'index.tmpl'
    _create_file_from_template(index_file, index_template, regex, 'Index file already exists, this should not be possible!')

    # CREATE README
    readme_file = target_dir + ps + plugin_name + ps + 'README.txt'
    readme_template = template_files + 'readme.tmpl'
    _create_file_from_template(readme_file, readme_template, regex, 'Plugin file already exists, this should not be possible!')

    # CREATE CHANGES FILE
    open(target_dir + ps + plugin_name + ps + 'CHANGES.md', 'a').close()
    return


def _create_file_from_template(file_to_create, template, regex_list, error_msg):
    if os.path.isfile(file_to_create):
        _warn(error_msg)
    else:
        template = open(template, 'r')
        content = template.read()

        new_file = open(file_to_create, 'a')
        new_file.write(_fix_content(content, regex_list))
        new_file.close()
    return


def _fix_content(content, regex):
    for reg in regex:
        for key, val in reg.items():
            content = re.sub(r'<' + key + '>', val, content)
    return content


def _create_presentation(plugin_name):
    presentation_name = re.sub(r'[_.-]', ' ', plugin_name)
    return presentation_name.title()


def _create_class(plugin_name):
    class_name = re.sub(r'[_.-]', ' ', plugin_name)
    class_name = class_name.title()
    class_name = re.sub(r'\s', '', class_name)
    return class_name


def _create_class_filename(plugin_name):
    filename = re.sub(r'[ ]', '-', plugin_name)
    filename = 'class-' + filename + '.php'
    return filename


def _create_plugin_var(plugin_name):
    plugin_var = re.sub(r'[ .-]', '_', plugin_name)
    return plugin_var


def _warn(message):
    print 'Warning: ' + message
    print 'Quitting'

    sys.exit(2)


def _help(message=None):
    self = sys.argv[0]
    help_message = self + ' -n plugin-name [ -t target/path/ ]'

    if message is not None:
        print message
        print help_message
    else:
        print help_message

    sys.exit(2)


if __name__ == '__main__':
    main()
