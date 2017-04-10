package kamilsedrowicz.sample.hbase;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.logging.log4j.LogManager;

import java.io.IOException;
import java.util.Map;

/**
 * An example application that that processes HBase data:
 * - creates two HBase tables
 * - loads the data from input files to the first table
 * - reads the data form the first table
 * - transforms the data
 * - loads the data to the second table
 */
public class DataProcessApp {

    private final static byte[] COLUMN_FAMILY = Bytes.toBytes("cf");
    private final static byte[] COLUMN_QUALIFIER = Bytes.toBytes("q");
    private final static String FILE_COLUMN_DELIMITER = ",";

    public static void main(String[] args) throws IOException {
        LogManager.getRootLogger().trace("entering application");
        Configuration conf = HBaseConfiguration.create();
        Connection connection = ConnectionFactory.createConnection(conf);
        Admin admin = connection.getAdmin();

        String tableName1 = "t1";
        String tableName2 = "t2";

        TableManipulator.createTable(admin, tableName1, COLUMN_FAMILY);
        Table table1 = connection.getTable(TableName.valueOf(tableName1));

        Map<String, String> data;
        for (int i = 1; i < 6; i++) {
            data = DataLoader.readDataFromFile("db_in_" + i + ".csv", FILE_COLUMN_DELIMITER);
            DataLoader.loadData(table1, COLUMN_FAMILY, COLUMN_QUALIFIER, data);
        }

        data = DataProcessor.scanTable(table1, COLUMN_FAMILY, COLUMN_QUALIFIER);
        data = DataProcessor.transformData(data);

        TableManipulator.createTable(admin, tableName2, COLUMN_FAMILY);
        Table table2 = connection.getTable(TableName.valueOf(tableName2));
        DataLoader.loadData(table2, COLUMN_FAMILY, COLUMN_QUALIFIER, data);

        table1.close();
        table2.close();
        connection.close();
    }
}
