import originpro as op

op.attach()
print(op.graph_list())
for graph in op.graph_list():
    print(graph.lname)
    graph.save_fig(path='C:\\Users\\18637\\Desktop\\%s.png'%(graph.lname),width=2479,ratio=300)
