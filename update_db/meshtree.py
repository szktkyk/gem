import sqlite3
import csv
import os
import pandas as pd


# create csv from the binary mtree file
with open('../data/csv_gitignore/mtrees2024.bin','rb') as f:
    data = f.readlines()

mesh_name = []
mesh_number = []
for a_line in data:
    a_line = a_line.decode()
    new_line = a_line.split(';')
    mesh_name.append(new_line[0])
    mesh_number.append(new_line[1].replace('\n',''))

df = pd.DataFrame(list(zip(mesh_name,mesh_number)), columns =['mesh_term','mesh_number'])
df.to_csv('../data/csv_gitignore/mtrees2024.csv')

# import data to sqlite
dbname = "../data/gem.db"
target_table_name = "mtree"
import_table_name = "../data/csv_gitignore/mtrees2024.csv"
is_create_table = True
is_header_skip = True

sql_script = """create table mtree( Integer, mesh_term text, mesh_number text)"""

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


