import unittest

from pynwb.io.build.builders import GroupBuilder, DatasetBuilder, LinkBuilder, ExternalLinkBuilder
import json


class GroupBuilderSetterTests(unittest.TestCase):
    """Tests for setter functions in GroupBuilder class"""

    def setUp(self):
        setattr(self, 'gb', GroupBuilder('gb'))

    def tearDown(self):
        pass

    def test_setitem_disabled(self):
        """Test __set_item__ is disabled"""
        with self.assertRaises(NotImplementedError):
            self.gb['key'] = 'value'

    def test_add_dataset(self):
        ds = self.gb.add_dataset('my_dataset', list(range(10)))
        self.assertIsInstance(ds, DatasetBuilder)

    def test_add_group(self):
        gp = self.gb.add_group('my_subgroup')
        self.assertIsInstance(gp, GroupBuilder)
        self.assertIs(self.gb['my_subgroup'], gp)

    def test_add_link(self):
        sl = self.gb.add_link('my_link', '/path/to/target')
        self.assertIsInstance(sl, LinkBuilder)
        self.assertIs(self.gb['my_link'], sl)

    def test_add_external_link(self):
        el = self.gb.add_external_link('my_externallink', '/path/to/target', 'external.h5')
        self.assertIsInstance(el, ExternalLinkBuilder)
        self.assertIs(self.gb['my_externallink'], el)

    #@unittest.expectedFailure
    def test_set_attribute(self):
        self.gb.set_attribute('key', 'value')
        self.assertIn('key', self.gb.obj_type)
        #self.assertEqual(dict.__getitem__(self.gb, 'attributes')['key'], 'value')
        self.assertEqual(self.gb['key'], 'value')

class GroupBuilderGetterTests(unittest.TestCase):

    def setUp(self):
        attrs = {
            'subgroup1': GroupBuilder('subgroup1'),
            'dataset1': DatasetBuilder('dataset1', list(range(10))),
            'soft_link1': LinkBuilder('soft_link1', "/soft/path/to/target"),
            'external_link1': ExternalLinkBuilder('external_link1', "/hard/path/to/target",
                                                  "test.h5"),
            'int_attr': 1,
            'str_attr': "my_str",
        }
        for key, value in attrs.items():
            setattr(self, key, value)

        setattr(self, 'group1', GroupBuilder('group1', {'subgroup1':self.subgroup1}))
        setattr(self, 'gb', GroupBuilder('gb', {'group1': self.group1},
                                         {'dataset1': self.dataset1},
                                         {'int_attr': self.int_attr,
                                          'str_attr': self.str_attr},
                                         {'soft_link1': self.soft_link1,
                                          'external_link1': self.external_link1}))

    def tearDown(self):
        pass

    def test_get_item_group(self):
        """Test __get_item__ for groups"""
        self.assertIs(self.gb['group1'], self.group1)

    def test_get_item_group_subgroup1(self):
        """Test __get_item__ for groups deeper in hierarchy"""
        self.assertIs(self.gb['group1/subgroup1'], self.subgroup1)

    def test_get_item_dataset(self):
        """Test __get_item__ for datasets"""
        self.assertIs(self.gb['dataset1'], self.dataset1)

    def test_get_item_attr1(self):
        """Test __get_item__ for attributes"""
        self.assertEqual(self.gb['int_attr'], self.int_attr)

    def test_get_item_attr2(self):
        """Test __get_item__ for attributes"""
        self.assertEqual(self.gb['str_attr'], self.str_attr)

    def test_get_item_invalid_key(self):
        """Test __get_item__ for invalid key"""
        with self.assertRaises(KeyError):
            self.gb['invalid_key']

    def test_get_item_soft_link(self):
        """Test __get_item__ for soft links"""
        self.assertIs(self.gb['soft_link1'], self.soft_link1)

    def test_get_item_external_link(self):
        """Test __get_item__ for external links"""
        self.assertIs(self.gb['external_link1'], self.external_link1)

    def test_get_group(self):
        """Test get() for groups"""
        self.assertIs(self.gb.get('group1'), self.group1)

    def test_get_group_subgroup1(self):
        """Test get() for groups deeper in hierarchy"""
        self.assertIs(self.gb.get('group1/subgroup1'), self.subgroup1)

    def test_get_dataset(self):
        """Test get() for datasets"""
        self.assertIs(self.gb.get('dataset1'), self.dataset1)

    def test_get_attr1(self):
        """Test get() for attributes"""
        self.assertEqual(self.gb.get('int_attr'), self.int_attr)

    def test_get_attr2(self):
        """Test get() for attributes"""
        self.assertEqual(self.gb.get('str_attr'), self.str_attr)

    def test_get_item_soft_link(self):
        """Test get() for soft links"""
        self.assertIs(self.gb.get('soft_link1'), self.soft_link1)

    def test_get_item_external_link(self):
        """Test get() for external links"""
        self.assertIs(self.gb.get('external_link1'), self.external_link1)

    def test_get_invalid_key(self):
        """Test get() for invalid key"""
        self.assertIs(self.gb.get('invalid_key'), None)

    def test_items(self):
        """Test items()"""
        items = (
            ('group1', self.group1),
            ('dataset1', self.dataset1),
            ('int_attr', self.int_attr),
            ('str_attr', self.str_attr),
            ('soft_link1', self.soft_link1),
            ('external_link1', self.external_link1)
        )
        #self.assertSetEqual(items, set(self.gb.items()))
        try:
            self.assertCountEqual(items, self.gb.items())
        except AttributeError:
            self.assertItemsEqual(items, self.gb.items())

    def test_keys(self):
        """Test keys()"""
        keys = (
            'group1',
            'dataset1',
            'int_attr',
            'str_attr',
            'soft_link1',
            'external_link1',
        )
        try:
            self.assertCountEqual(keys, self.gb.keys())
        except AttributeError:
            self.assertItemsEqual(keys, self.gb.keys())

    def test_values(self):
        """Test values()"""
        values = (
            self.group1,
            self.dataset1,
            self.int_attr, self.str_attr,
            self.soft_link1,
            self.external_link1,
        )
        try:
            self.assertCountEqual(values, self.gb.values())
        except AttributeError:
            self.assertItemsEqual(values, self.gb.values())

    @unittest.skip('not necessarily useful')
    def test_write(self):
        """Test for base dictionary functionality preservation"""
        self.maxDiff = None
        builder_json = '''
            {
            "group1": {
                "subgroup1": {

                }
            },
            "dataset1": {
                "attributes": {
                },
                "data": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9
                ]
            },
            "soft_link1": {
                "path": "/soft/path/to/target",
                "hard": false
            },
            "external_link1": {
                "path": "/hard/path/to/target",
                "file_path": "test.h5",
                "hard": false
            },
            "int_attr": 1,
            "str_attr": "my_str"
        }
        '''
        dump = json.dumps(self.gb)

        print (dump)
        self.assertDictEqual(json.loads(builder_json), json.loads(dump))


class GroupBuilderIsEmptyTests(unittest.TestCase):

    def test_is_empty_true(self):
        """Test empty when group has nothing in it"""
        gb = GroupBuilder('gb')
        self.assertEqual(gb.is_empty(), True)

    def test_is_empty_true_group(self):
        """Test is_empty() when group has an empty subgroup"""
        gb = GroupBuilder('gb', {'my_subgroup': GroupBuilder('my_subgroup')})
        self.assertEqual(gb.is_empty(), True)

    def test_is_empty_false_dataset(self):
        """Test is_empty() when group has a dataset"""
        gb = GroupBuilder('gb', datasets={'my_dataset': DatasetBuilder('my_dataset')})
        self.assertEqual(gb.is_empty(), False)

    def test_is_empty_false_group_dataset(self):
        """Test is_empty() when group has a subgroup with a dataset"""
        gb = GroupBuilder('gb', {'my_subgroup': GroupBuilder('my_subgroup', datasets={'my_dataset': DatasetBuilder('my_dataset')})})
        self.assertEqual(gb.is_empty(), False)

    def test_is_empty_false_attribute(self):
        """Test is_empty() when group has an attribute"""
        gb = GroupBuilder('gb', attributes={'my_attr': 'attr_value'})
        self.assertEqual(gb.is_empty(), False)

    def test_is_empty_false_group_attribute(self):
        """Test is_empty() when group has subgroup with an attribute"""
        gb = GroupBuilder('gb', {'my_subgroup': GroupBuilder('my_subgroup', attributes={'my_attr': 'attr_value'})})
        self.assertEqual(gb.is_empty(), False)

class GroupBuilderDeepUpdateTests(unittest.TestCase):

    def test_mutually_exclusive_subgroups(self):
        gb1 = GroupBuilder('gb1', {'subgroup1': GroupBuilder('subgroup1')})
        gb2 = GroupBuilder('gb2', {'subgroup2': GroupBuilder('subgroup2')})
        gb1.deep_update(gb2)
        self.assertIn('subgroup2', gb1)
        gb1sg = gb1['subgroup2']
        gb2sg = gb2['subgroup2']
        self.assertIs(gb1sg, gb2sg)

    def test_mutually_exclusive_datasets(self):
        gb1 = GroupBuilder('gb1', datasets={'dataset1': DatasetBuilder('dataset1', [1,2,3])})
        gb2 = GroupBuilder('gb2', datasets={'dataset2': DatasetBuilder('dataset2', [4,5,6])})
        gb1.deep_update(gb2)
        self.assertIn('dataset2', gb1)
        #self.assertIs(gb1['dataset2'], gb2['dataset2'])
        self.assertListEqual(gb1['dataset2'].data, gb2['dataset2'].data)

    def test_mutually_exclusive_attributes(self):
        gb1 = GroupBuilder('gb1', attributes={'attr1': 'my_attribute1'})
        gb2 = GroupBuilder('gb2', attributes={'attr2': 'my_attribute2'})
        gb1.deep_update(gb2)
        self.assertIn('attr2', gb2)
        self.assertEqual(gb2['attr2'], 'my_attribute2')

    def test_mutually_exclusive_links(self):
        gb1 = GroupBuilder('gb1', links={'link1': LinkBuilder('link1', '/path/to/link1')})
        gb2 = GroupBuilder('gb2', links={'link2': LinkBuilder('link2', '/path/to/link2')})
        gb1.deep_update(gb2)
        self.assertIn('link2', gb2)
        self.assertEqual(gb1['link2'], gb2['link2'])

    def test_intersecting_subgroups(self):
        subgroup2 = GroupBuilder('subgroup2')
        gb1 = GroupBuilder('gb1', {'subgroup1': GroupBuilder('subgroup1'), 'subgroup2': subgroup2})
        gb2 = GroupBuilder('gb2', {'subgroup2': GroupBuilder('subgroup2'), 'subgroup3': GroupBuilder('subgroup3')})
        gb1.deep_update(gb2)
        self.assertIn('subgroup3', gb1)
        self.assertIs(gb1['subgroup3'], gb2['subgroup3'])
        self.assertIs(gb1['subgroup2'], subgroup2)

    def test_intersecting_datasets(self):
        gb1 = GroupBuilder('gb1', datasets={'dataset2': DatasetBuilder('dataset2', [1,2,3])})
        gb2 = GroupBuilder('gb2', datasets={'dataset2': DatasetBuilder('dataset2', [4,5,6])})
        gb1.deep_update(gb2)
        self.assertIn('dataset2', gb1)
        self.assertListEqual(gb1['dataset2'].data, gb2['dataset2'].data)

    def test_intersecting_attributes(self):
        gb1 = GroupBuilder('gb1', attributes={'attr2':'my_attribute1'})
        gb2 = GroupBuilder('gb2', attributes={'attr2':'my_attribute2'})
        gb1.deep_update(gb2)
        self.assertIn('attr2', gb2)
        self.assertEqual(gb2['attr2'], 'my_attribute2')

    def test_intersecting_links(self):
        gb1 = GroupBuilder('gb1', links={'link2': LinkBuilder('link2', '/path/to/link1')})
        gb2 = GroupBuilder('gb2', links={'link2': LinkBuilder('link2', '/path/to/link2')})
        gb1.deep_update(gb2)
        self.assertIn('link2', gb2)
        self.assertEqual(gb1['link2'], gb2['link2'])

class DatasetBuilderDeepUpdateTests(unittest.TestCase):

    def test_overwrite(self):
        db1 = DatasetBuilder('db1', [1,2,3])
        db2 = DatasetBuilder('db2', [4,5,6])
        db1.deep_update(db2)
        self.assertListEqual(db1.data, db2.data)

    def test_no_overwrite(self):
        db1 = DatasetBuilder('db1', [1,2,3])
        db2 = DatasetBuilder('db2', [4,5,6], attributes={'attr1': 'va1'})
        db1.deep_update(db2)
        self.assertListEqual(db1.data, db2.data)
        self.assertIn('attr1', db1.attributes)


if __name__ == '__main__':
    unittest.main()
