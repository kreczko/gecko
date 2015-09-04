from gecko.utils.ntuple import FileInfo

file_name = '/storage/TopQuarkGroup/TTJets_Madgraph_PU20bx25_001.root'
f = FileInfo(file_name)
f.toJSON('test.json')
