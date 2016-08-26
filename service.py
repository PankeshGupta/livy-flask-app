from livy.client import HttpClient
import csv
import pathlib2
import time

global client
client = None

def set_client(http_client):
    global client
    client = http_client

def upload_jar_files():
    time.sleep(10)
    add_spark_csv_uri = str(pathlib2.Path("/Users/manikandan.nagarajan/jars/spark-csv_2.10-1.4.0"
                                          ".jar").as_uri())
    add_commons_csv_uri = str(pathlib2.Path("/Users/manikandan.nagarajan/jars/commons-csv-1.4.jar").as_uri())
    add_spark_csv_future = client.add_jar(add_spark_csv_uri)
    add_commons_csv_future = client.add_jar(add_commons_csv_uri)
    print add_spark_csv_future.result()
    print add_commons_csv_future.result()

def process_kdensity_request(column, bandwidth, points):
    bandwidth = float(bandwidth)
    points_list = [float(value) for value in points.strip().split(',')]
    print "column::", column
    print "_bandwidth::", bandwidth
    print "_points::", points_list
    result = process_kdensity_job(column, bandwidth, points_list)
    print "result::", result
    import ast

    #testarray = ast.literal_eval(result)
    print "reslt-list::", result[0]
    result_list = []
    for item in result:
        print "reslt-list-item::", item
        result_list.append(item)
    response = (points_list, result_list)
    return response

def process_kdensity_job(column, bandwidth, points_list):
    def kdensity_job(context):
        from pyspark.sql import Row
        from pyspark.mllib.stat import KernelDensity
        sql_ctx = context.sql_ctx
        df = sql_ctx.read.format('com.databricks.spark.csv') \
            .option('header', 'true').option('inferSchema', 'true') \
            .load('/Users/manikandan.nagarajan/Desktop/datasets/demo/forestfires.csv')
        rdd_column_data = df.rdd.map(lambda row_data: row_data[column])

        kd = KernelDensity()
        kd.setSample(rdd_column_data)
        kd.setBandwidth(bandwidth)
        densities = kd.estimate(points_list)
        return densities

    # def spark_job_call_back(spark_job_future):
    #     print "result in spark job callback:", spark_job_future.result()
    #
    # add_spark_job_future = client.submit(kdensity_job)
    # add_spark_job_future.add_done_callback(spark_job_call_back)
    # time.sleep(60)

    kdensity_job_future = client.submit(kdensity_job)
    result = kdensity_job_future.result(timeout=30)
    return result

    #return None
