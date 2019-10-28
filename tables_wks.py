from flask import url_for
from flask_table import Table, Col, NestedTableCol
import operator

class TableEntities(Table):
    type = Col('Tipo')
    text = Col('Texto')
    relevance = Col('Relevância')
    count = Col('Contagem')
    ''' For custom html styles 
    def get_tr_attrs(self, item):
        if (dt.datetime.strptime(item['tempo_envio'], "%d/%m/%Y %H:%M:%S") > dt.datetime(2019, 10, 17, 23, 59)):
            return {'class': 'atrasado'}
        else:
            return {}
    '''

'''
class SubTable(Table):
    text = Col('Text')
    location = Col('Position')
    entities = Col('Entities')

class TableRelations(Table):
    type = Col('Type')
    arguments = NestedTableCol('Arguments', SubTable)
    score = Col('Relevance')
'''

class TableRelations(Table):
    entity1 = Col('1ª Entidade')
    type = Col('Relação')
    entity2 = Col('2ª Entidade')
    relevance = Col('Relevância')

def gen_entities_table(records):
    table = TableEntities(records)
    return(table)

def gen_relations_table(records):
    organized = []
    #print("Testing")
    #print(records)
    for relation in records:
        print(relation['arguments'][0]['entities'])
        print(relation['arguments'][0]['entities'])
        print("test done")
        organized.append(
            {
                'entity1': "{}: {}".format(relation['arguments'][0]['entities'][0]['type'], relation['arguments'][0]['entities'][0]['text']),
                'type': relation['type'],
                'entity2': "{}: {}".format(relation['arguments'][1]['entities'][0]['type'], relation['arguments'][1]['entities'][0]['text']),
                'relevance': relation['score']
            }
        )
    table = TableRelations(organized)
    return(table)
