WP-PLUGIN-BUILDER

README v1.0

Author  Zorko <contact@zorko.co>
Year    2016
License GPL 3.0

Wordpress Plugin Builder

This script was created as a Python practice with a real use case: Ease the creation of Wordpress plugins.
By removing the tedious task of creating the file structure and actually connecting the main class to the main plugin file,
this script does just what is what meant for.

Simply start writing code in the class file located under the includes/classes directory in the generated plugin root directory.
Don't forget to add your hooks in the main plugin file located in the plugin root dir :-)

EXAMPLE OF USE

Method inside class file:
    public function hello_world() {
        echo "Hello World!";
        return;
    }


Add hook in the bottom of the main plugin file:
    add_action('init', array($object, 'hello_world'));