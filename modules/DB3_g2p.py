from ModulesForW02 import *
import time
import subprocess
import sqlite3
import csv
import os

#Download gene2pubmed from ftp site to the local data directory
download_gene2pubmed()
# gunzip gene2pubmed
time.sleep(1)
source_file = "../csv_gitignore/gene2pubmed.gz"
command = ["gunzip", source_file]
time.sleep(1)
subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
time.sleep(1)
command = ["mv", "../csv_gitignore/gene2pubmed", "../csv_gitignore/gene2pubmed.tsv"]
subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

print("gene2pubmed is downloaded in the local data directory")
exit()


dbname = "../data/gem.db"
target_table_name = "gene2pubmed"
import_table_name = "../csv_gitignore/gene2pubmed.tsv"
is_create_table = True
is_header_skip = True

sql_script = """create table gene2pubmed(tax_id text, GeneID text, PubMed_ID text)"""

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
        ???????????????????????????????????????????????????
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



