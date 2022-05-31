import yaml
dict_file=[{"names":["person" ,"cat"]}]
with open("/home/pc-visualisation/Bureau/database_training/data.yaml", 'w') as file:
    documents = yaml.dump(dict_file, file,default_flow_style=None)