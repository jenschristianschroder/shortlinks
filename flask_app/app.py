import os
from flask import Flask, request, redirect
from azure.storage import CloudStorageAccount
from azure.storage.table import TableService, Entity
app = Flask(__name__)


@app.route('/<shortlink>', methods=['GET'])
def shortlinkredirect(shortlink):
    table_service = TableService(account_name=os.environ["StorageAccount"], account_key=os.environ["StorageKey"])

    tablename = 'links'
    target = os.environ["Hostname"]
    try:
        partitionkey = shortlink[:1]
        rowkey = shortlink
        shortlinkentity = table_service.get_entity(table_name=tablename, partition_key=partitionkey, row_key=rowkey)
        target = shortlinkentity.target
    except Exception as e:
        print('Error occurred.', e)
    finally:
        if request.query_string != b'':
            target = target + "?" + request.query_string.decode('utf-8')
        return redirect(target)


if __name__ == "__main__":
    app.run(debug=True)