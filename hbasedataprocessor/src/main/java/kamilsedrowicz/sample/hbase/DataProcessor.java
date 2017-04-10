package kamilsedrowicz.sample.hbase;

import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.ResultScanner;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.logging.log4j.LogManager;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Contains methods for reading and transforming data from an HBase table.
 */
public class DataProcessor {

    /**
     * Reads data specified by the column family and the column qualifier from the HBase table.
     *
     * @param table an opened HBase table
     * @param columnFamily a column family
     * @param columnQualifier a column qualifier
     * @return a map of {row key : column value} containing the data read from the table
     */
    public static Map<String, String> scanTable(Table table, byte[] columnFamily, byte[] columnQualifier) {
        Scan scan = new Scan();
        scan.addColumn(columnFamily, columnQualifier);
        Map<String, String> map = new HashMap<>();
        try (ResultScanner rs = table.getScanner(scan)) {
            for (Result r : rs) {
                map.put(Bytes.toString(r.getRow()), Bytes.toString(r.getValue(columnFamily, columnQualifier)));
            }
        } catch (IOException e) {
            LogManager.getRootLogger().error("table scan error");
            throw new RuntimeException(e);
        }
        return map;
    }

    /**
     * Creates a map with transformed (changed to uppercase) values of the input map.
     *
     * @param data a map
     * @return a map with transformed values
     */
    public static Map<String, String> transformData(Map<String, String> data) {
        return data.entrySet().stream().collect(
                Collectors.toMap(Map.Entry::getKey, e -> e.getValue().toUpperCase())
        );
    }
}
