from ute_infomodel import ute_infomodel
filename = '/home/work/temp/meta_T7027384.zip'
btsid = '225'
i1 = ute_infomodel()
i1.setup_infomodel(address='10.69.64.120', port=12345, definitions_file_path=filename, alias=btsid)
i1.connect_infomodel(alias=btsid)
print 'OK'
i1.teardown_infomodel(alias=btsid)

