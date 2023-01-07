from ModulesForW02 import *
import time
import subprocess
import sqlite3
import csv
import os


dbname = "../data/gem.db"
target_table_name = "taxidlineage"
# target_table_name = "metadata"
# import_table_name = "../20220917_ge_metadata.csv"
import_table_name = "../csv_gitignore/taxidlineage3.csv"
is_create_table = True
is_header_skip = True

# sql_script = """create table gene_info(tax_id text, GeneID text, Symbol text, LocusTag text, Synonyms text, dbXrefs text, chromosome text, map_location text, description text, type_of_gene text, Symbol_from_nomenclature_authority text, Full_name_from_nomenclature_authority text, Nomenclature_status text, Other_designations text, Modification_date text, Feature_type text);"""
sql_script = """create table taxidlineage(id text, taxids text)"""
# sql_script = """create table metadata(getool Text, pmid Text, pubtitle Text, pubdate Text, organism_name Text, genesymbol Text,  editing_type Text, gene_counts Integer, biopro_id Text, RNA_seq Text, vector Text, cellline Text, tissue Text, Mutation_type Text)"""

class ImportSQLite():
    def __init__(self, dbname, target_table_name, import_data_name, is_create_table, is_header_skip=False, sql_create_table=None):
        """
        Import tsv or csv into DB
        :param dbname: text Name of the connecting DB
        :param target_table_name: text Table Name
        :param import_data_name: text Data to import
        :param is_create_table: boolean If you create a table or not
        :param is_header_skip: boolean If you skip a header or not
        :param sql_create_table: text 
        """
        self.dbname = dbname
        self.target_table_name = target_table_name
        self.import_data_name = import_data_name
        self.is_create_table = is_create_table
        self.is_header_skip = is_header_skip
        _, raw_delimiter = os.path.splitext(import_data_name)
        if raw_delimiter == '.csv':
            self.delimiter = ','
        elif raw_delimiter == '.tsv':
            self.delimiter = '\t'
        else:
            raise ValueError('Import file should be csv or tsv.')

        if is_create_table:
            if not sql_create_table:
                raise ValueError('It\'s necessary of sql to create table')
            else:
                self.sql_create_table = sql_create_table


    def read_import_file(self):
        with open(self.import_data_name, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            if self.is_header_skip:
                header = next(reader)

            return [i for i in reader]


    def pick_column_num(self, import_data):
        """
        インポートファイルの列数を算出する
        :param import_data: array(two-dimensional)
        :return: int
        """
        columns = []
        for raw in import_data:
            columns.append(len(raw))
        if len(set(columns)) == 1:
            return columns[0]
        else:
            raise ValueError('this import files has diffrenect column numbers.')


    def insert_csv_file(self):
        input_file = self.read_import_file()
        column = self.pick_column_num(input_file)
        val_questions = ['?' for i in range(column)]
        cur.executemany("insert into {0} values ({1})".format(self.target_table_name, ','.join(val_questions)), input_file)


if __name__ == '__main__':

    sql = ImportSQLite(
        dbname=dbname,
        target_table_name=target_table_name,
        import_data_name=import_table_name,
        is_create_table=is_create_table,
        is_header_skip= is_header_skip,
        sql_create_table=sql_script
    )

    conn = sqlite3.connect(sql.dbname)
    cur = conn.cursor()

    if sql.is_create_table:
        cur.execute('drop table if exists {};'.format(target_table_name))
        cur.execute(sql.sql_create_table)

    sql.insert_csv_file()

    conn.commit()
    conn.close()




# time.sleep(1)
# command_format = "cat gene_info | awk '{ print $1, $2, $3}' > ../data/geneinfo.csv"
# subprocess.call(command_format.split())

# df_geneinfo = pd.read_csv("../data/geneinfo.csv", sep=" ")

# df_dict = {}
# for name, group in df_geneinfo.groupby("#tax_id"):
#     df_dict[name] = group
#     df_dict[name].to_csv(f"./gene_ref_test/{name}_genes.csv", sep="\t")

# time.sleep(1)
# command_remove1 = "rm ../data/gene_info"
# command_remove2 = "rm ../data/geneinfo.csv"
# subprocess.call(command_remove1.split())
# time.sleep(1)
# subprocess.call(command_remove2.split())