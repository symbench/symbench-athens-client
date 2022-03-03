CLONE_DESIGN_QUERY = """
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").as('tmp').property('_duptag_','_SRC_').select('tmp').repeat(__.in('inside').as('tmp').property('_duptag_','_SRC_').select('tmp')).times(20)
g.V().has('_duptag_','_SRC_').as('x').select('x').addV(select('x').label()).as('y').property('_duptag_','_DUP_').addE('clone').from('x').to('y').iterate()
g.V().has('_duptag_','_SRC_').as('x').out('clone').where(__.has('_duptag_','_DUP_')).as('y').select('x').properties().as('xps').select('y').property(select('xps').key(),select('xps').value()).select('y').property('_duptag_','_DUP_').iterate()
g.V().has('_duptag_','_SRC_').as('orig').out('clone').where(__.has('_duptag_','_DUP_')).as('cloned').select('orig').inE().where(label().is(neq('clone'))).as('elabel').select('elabel').outV().out('clone').where(__.has('_duptag_','_DUP_')).as('inTarg').select('cloned').addE(select('elabel').label()).from('inTarg').to('cloned').iterate()
g.V().has('_duptag_','_SRC_').as('orig').out('clone').where(__.has('_duptag_','_DUP_')).as('cloned').select('orig').out('component_id').as('linkDest').addE('component_id').from('cloned').to('linkDest').iterate()
g.V().has('_duptag_','_SRC_').as('orig').out('clone').where(__.has('_duptag_','_DUP_')).as('cloned').select('orig').out('id_in_component_model').as('linkDest').addE('id_in_component_model').from('cloned').to('linkDest').iterate()
g.V().has('[]Name',"{src_name}").has('_duptag_','_DUP_').property('[]Name','{dst_name}')
g.V().has('_duptag_','_SRC_').outE('clone').drop().iterate()
g.V().has('_duptag_','_SRC_').property('_duptag_','_cpysrc_')
g.V().has('_duptag_','_DUP_').property('_duptag_','_cpydst_')
"""


CLEAR_DESIGN_QUERY = """
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").in("inside").in("inside").in("inside").in("inside").in("inside").in("inside").in("inside").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").in("inside").in("inside").in("inside").in("inside").in("inside").in("inside").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").in("inside").in("inside").in("inside").in("inside").in("inside").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").in("inside").in("inside").in("inside").in("inside").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").in("inside").in("inside").in("inside").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").in("inside").in("inside").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").in("inside").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").in("inside").in("inside").in("inside").in("inside").in("inside").in("inside").in("inside").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").in("inside").in("inside").in("inside").in("inside").in("inside").in("inside").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").in("inside").in("inside").in("inside").in("inside").in("inside").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").in("inside").in("inside").in("inside").in("inside").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").in("inside").in("inside").in("inside").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").in("inside").in("inside").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").in("inside").drop()
g.V().has("VertexLabel","[avm]Design").has("[]Name","{src_name}").drop()
"""
