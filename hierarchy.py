'''
dimensions.py
@author: todd
'''
import logging
import csv

class HierarchyItem:
    """
    This class holds each item of the hierarchy.  There are five fields:
        + code (a unique identifier used as the key)
        + name
        + parent code, the code of the parent in the hierarchy.
        + level name (defined by the hierarchy key)
        + level number (also defined by the hierarchy key)
    The top level hierarchy items should have 'root' as the parent code (no quotes)
    """

    def __init__(self, code, name, parent_code, level_name, level_number):
        self.code = code
        self.name = name
        self.parent_code = parent_code
        self.level_name = level_name
        self.level_number = level_number

class Hierarchy:
    """
    This data structure holds a square hierarchy stored in a CSV file and defined by a hierarchy key file (also a CSV).

    The hierarchy key file should have the following attributes:
         + It lists the three elements needed for each level of the hierarchy.
         + Each level in the hierarchy is defined by three columns, a code, a name and the parent code.
         + The top level should have 'root' as a parent (no quotes).
         + The first row should be the top level of the hierarchy, second row = second level, etc.
         + The first row in the CSV (row titles) should be:  code,name,parent_code
         + Repeat the code and name of these items in the regular hierarchy CSV vile for each level in the hierarchy
    
    The regular hierarchy file should have the following attributes:
         + The lowest level has unique codes and is the first column.
         + Each bottom level node is listed with its parent nodes on one line
         + Higher level codes (parents) are repeated over rows, showing how the lower levels roll up to the higher, e.g.:
            11186,Product 11186,1118,Desk 1118,111,Team 111,11,Business Line 11,1,Asset Class 1
            11389,Product 11389,1138,Desk 1138,113,Team 113,11,Business Line 11,1,Asset Class 1
            11497,Product 11497,1149,Desk 1149,114,Team 114,11,Business Line 11,1,Asset Class 1
                
    """

    def __init__(self, file, keyfile):
        self.log = logging.getLogger(__name__)
        item_keys = []
        rows = []
        columns = []
        self.items = {}     # class level variable
        self.levels = []    # class level variable
        self.children = []  # used by 'get_all_children'
        rowcount = 0


        self.log.info(f"reading hierarchy key file... {keyfile}")

        try:
            # get hierarchy key -> map of csv columns to item definitions
            with open(keyfile, newline='') as f:
                reader = csv.DictReader(f)
                levelnum = 0
                # use keys in first row as master set
                for row in reader:
                    self.log.debug(str(row))
                    levelnum += 1
                    row['level_number'] = levelnum
                    item_keys.append(row) 
            self.log.debug(('/' * 20) + ' hierarchy key  ' + ('/' * 20))
            
            # output hierarchy key to log
            for item_key in item_keys:
                self.log.debug(('-' * 20) + ' item key ' + ('-' * 20))
                self.log.debug(str(item_key))
                self.log.debug('item_key[\'code\']=' + str(item_key['code']))
                self.log.debug('item_key[\'name\']=' + str(item_key['name']))
                self.log.debug('item_key[\'parent_code\']=' + str(item_key['parent_code']))

            # process regular hierarchy file
            self.log.debug(('/' * 20) + ' hierarchy file ' + ('/' * 20))
            self.log.info(f"reading {file}")

            # get hierarchy map of columns to fields
            with open(file, newline='') as f:
                reader = csv.DictReader(f)
                # use keys in first row as master set
                for row in reader:
                    if rowcount == 0:
                        columns = list(row.keys())
                    # log.debug(row)
                    rows.append(row)
                    rowcount += 1
            
            self.log.info(f"Read {rowcount} rows")

            # create hierarchy items
            # ['product_code', 'product', 'desk_code', 'desk', 'team_code', 'team', 'business_line_code', 'business_line', 'asset_class_code', 'asset_class'] 
            # ['code', 'name', 'parent_code']
            for row in rows:
                for item_key in item_keys:
                    # log.debug(item_key)
                    # log.debug(row)
                    if item_key['parent_code'] != 'root':
                        i = HierarchyItem(
                            row[item_key['code']], 
                            row[item_key['name']], 
                            row[item_key['parent_code']], 
                            item_key['name'], 
                            item_key['level_number'])
                    else:
                        i = HierarchyItem(
                            row[item_key['code']], 
                            row[item_key['name']], 
                            None, 
                            item_key['name'], 
                            item_key['level_number'])
                    # add to master dictionary
                    self.items[row[item_key['code']]] = i
           

        except:
            self.log.exception("*** Caught exception trying to create hierarchy ***")
            raise

    def get_item(self, code):
        '''
        Just let it fail if there is no item?
        '''
        try:
            i = self.items[code]
        except:
            self.log.exception("*** Caught exception trying to get item ***")
            raise
        return i
                
    def get_parent(self, code):
        '''
        Return parent code of requested node or None if it's top level or doesn't exist
        '''
        i = self.get_item(code)
        if i.parent_code is not None and i.parent_code != 'root':
            return i.parent_code
        else:
            return None


    def get_children(self, code):
        '''
        Get a list of child node codes at the first level below the requested node
        '''
        i = self.get_item(code)
        # find items where this code is the parent (use local children variable)
        children = []
        for c in self.items.keys():
            if self.items[c].parent_code == i.code:
                children.append(self.items[c].code)
        return children

    def get_child_count(self, code):
        return len(self.get_children(code))

    def get_all_children(self, code, children=[]):
        '''
        Get child codes at all levels underneath the requested node (use class level children variable)
        '''
        self.__get_all_children(code)

        # reset children variable
        cs = self.children
        self.children = []
        return cs

    def __get_all_children(self, code):
        '''
        Recursive part 
        TODO: This could probably be more efficient
        '''
        added = 0
        self.log.debug('length of children coming into __get_all_children: ' + str(len(self.children)))
        if self.children is None:
            self.log.debug("Children is None.  Creating an empty list.")
            self.children = []

        #  add all children of the requested code
        if code is not None: 
            i = self.get_item(code)

            self.log.debug('Adding first children for code: ' + i.code)
            self.log.debug('Children size: ' + str(len(self.children)))
            cs = self.get_children(i.code)
            for c in cs:
                if c not in self.children:
                    self.log.debug('appending: ' + c)
                    self.children.append(c)
                    added += 1
        else:
            self.log.debug('Calling private function with code=None')

        # loop through the existing children and add child node codes not already in the list
        for c in self.children:
            self.log.debug('Checking child: ' + c)
            cs = self.get_children(c)
            for n in cs:
                if n not in self.children:
                    self.log.debug('Adding new child: ' + n)
                    self.children.append(n)
                    added += 1

        # call the function recursively with no code but a populated list of children (class level variable)
        # if the number of added nodes is zero then stop calling the function recursively
        if added > 0:
            self.log.debug("Calling function recursively.  added=" + str(added))
            self.__get_all_children(None)
        else:
            self.log.debug("Returning to caller, added=" + str(added))
            self.log.debug("Length of children: " + str(len(self.children)))
            # self.log.debug("children: " + str(self.children))
            return


    def get_leaf_nodes(self, code):
        '''
        Get the lowest level child codes (e.g. have no children) under the requested code
        '''
        leaves = []
        i = self.get_item(code)
        all_children = self.get_all_children(i.code)
        self.log.debug("Pruning non-leaf nodes:" + str(all_children))
        for c in all_children:
            child_count = self.get_child_count(c)
            self.log.debug(f"Child count for {c} is {child_count}")
            if child_count == 0:
                leaves.append(c)
        self.log.debug("Remaining leaves: " + str(leaves))
        return leaves

