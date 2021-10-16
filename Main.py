'''
Main.py
@author: todd
https://stackoverflow.com/questions/15727420/using-logging-in-multiple-modules
'''
import logging
from logging.config import fileConfig
from hierarchy import Hierarchy

def main():
    log.debug('Starting')

    try:

        h = Hierarchy('Hierarchy.csv', 'hierarchy_key.csv')
        
        # Get one item code=217
        log.info(('/' * 40) + ' Get one item ' + ('/' * 40))
        i = h.get_item('217')
        log.info('\tcode: ' + i.code)
        log.info('\tname: ' + i.name)
        log.info('\tlevel_name: ' + i.level_name)
        log.info('\tlevel_number: ' + str(i.level_number))

        
        # Get parent of code=9241
        log.info(('/' * 40) + ' Get a parent ' + ('/' * 40))
        log.info('Parent of 9241 is: ' + h.get_parent('9241'))
        
        # Get children of code=29
        log.info(('/' * 40) + ' Get children of a code ' + ('/' * 40))
        log.info('Getting children for code: 29')
        for c in h.get_children('29'):
            ch = h.get_item(c)
            log.info('\tcode: ' + ch.code)
            log.info('\tname: ' + ch.name)
            log.info('\tlevel_name: ' + ch.level_name)
            log.info('\tlevel_number: ' + str(ch.level_number))
            log.info('-' * 20)

        # get *all* children of code=22
        log.info(('/' * 40) + ' Get *all* children of code 22 ' + ('/' * 40))
        all_children = h.get_all_children('22')

        for c in all_children:
            ch = h.get_item(c)
            log.info('\tcode: ' + ch.code)
            log.info('\tname: ' + ch.name)
            log.info('\tlevel_name: ' + ch.level_name)
            log.info('\tlevel_number: ' + str(ch.level_number))
            log.info('-' * 20)

        # get leaf nodes of code=42
        log.info(('/' * 40) + ' Get leaf nodes under a code ' + ('/' * 40))
        leaves = h.get_leaf_nodes('42')
        for leaf in leaves:
            l = h.get_item(leaf)
            log.info('\tcode: ' + l.code)
            log.info('\tname: ' + l.name)
            log.info('\tlevel_name: ' + l.level_name)
            log.info('\tlevel_number: ' + str(l.level_number))
            log.info('\tnumber of children: ' + str(h.get_child_count(l.code)))
            log.info('-' * 20)

    except:
        log.exception("ERROR IN MAIN SCRIPT:")

if __name__ == '__main__':
    fileConfig('logging_config.ini')
    log = logging.getLogger(__name__)
    main()

