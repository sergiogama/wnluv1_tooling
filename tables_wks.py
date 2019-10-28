from flask import url_for
from flask_table import Table, Col, NestedTableCol
import operator

class TableEntities(Table):
    type = Col('Tipo')
    text = Col('Texto')
    relevance = Col('Confiança')
    count = Col('Contagem')

class TableEntitiesCustom(Table):
    type = Col('Tipo')
    text = Col('Texto')
    confidence = Col('Confiança')
    count = Col('Contagem')

class TableRelations(Table):
    entity1 = Col('1ª Entidade')
    type = Col('Relação')
    entity2 = Col('2ª Entidade')
    relevance = Col('Relevância')

def gen_entities_table(records):
    table = TableEntities(records)
    return(table)

def gen_entities_table_custom(records):
    table = TableEntitiesCustom(records)
    return(table)


def gen_relations_table(records):
    organized = []
    for relation in records:
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
