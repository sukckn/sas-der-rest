# Databricks notebook source
import os
import uuid

# COMMAND ----------

#get values from jobs
SQLQuery= dbutils.widgets.get("SQLQuery")

# COMMAND ----------

#Get a temp filename for extracted data
dbr_temp_path= str(uuid.uuid1())

#Path on DBR server where temp extracted file should land
DBR_PATH_FOR_FILE= '/tmp/outputcsv'

#CLEAR DATA - empty path
dbutils.fs.rm(DBR_PATH_FOR_FILE,True)

# COMMAND ----------

#run submitted SQLQuery
data= spark.sql(SQLQuery)

# COMMAND ----------

#export data using single node, can be optimised
data.coalesce(1).write.format("com.databricks.spark.csv").option("header", "true").mode("overwrite").save(DBR_PATH_FOR_FILE + "/" + dbr_temp_path)

# COMMAND ----------

#get all exported files
exported_files= dbutils.fs.ls(DBR_PATH_FOR_FILE+"/"+dbr_temp_path)


# COMMAND ----------

#out of all exported file get filename with data
for file in exported_files:
  if (str(file.name).endswith(".csv")):
      exported_file= "/dbfs"+DBR_PATH_FOR_FILE+"/"+dbr_temp_path+"/"+file.name


# COMMAND ----------

# archive exported csv file
os.system("gzip "+exported_file)
