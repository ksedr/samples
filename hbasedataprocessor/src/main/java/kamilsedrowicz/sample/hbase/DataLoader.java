package kamilsedrowicz.sample.hbase;

import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.logging.log4j.LogManager;

import java.io.BufferedReader;
import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Contains methods for reading data from files and loading it to a HBase table.
 */
public class DataLoader {
    /**
     * Reads data from a file.
     * Assumes that the input file is a text file with two columns (row key and column value)
     * delimited by the file column delimiter.
     *
     * @param fileName the name of the file containing the data to read
     * @return a map of {row key : column value}
     */
    public static Map<String, String> readDataFromFile(String fileName, String columnDelimiter) {

        Map<String, String> map = new HashMap<>();
        try {
            BufferedReader br = Files.newBufferedReader(Paths.get(ClassLoader.getSystemResource(fileName).toURI()));
            map = br.lines()
                    .map(s -> s.split(columnDelimiter, 2))
                    .collect(Collectors.toMap(e -> e[0], e -> e[1]));
            LogManager.getRootLogger().trace(fileName + ": " + map.size() + " lines read");
        } catch (IOException e) {
            LogManager.getRootLogger().error("reading file error:" + fileName);
            throw new RuntimeException(e);
        } catch (URISyntaxException e) {
            LogManager.getRootLogger().error("uri syntax error:" + fileName);
            throw new RuntimeException(e);
        }

        return map;
    }

    /**
     * Loads (batch) the data to the table column specified by the column family and the column qualifier.
     *
     * @param table an opened HBase table
     * @param data a map of {row key : column value} with the input data
     * @return a results object
     */
    public static Object[] loadData(Table table, byte[] columnFamily, byte[] columnQualifier, Map<String, String> data) {

        List<Put> batch = data.entrySet().stream().map(e -> {
            Put put = new Put(Bytes.toBytes(e.getKey()));
            put.addColumn(columnFamily, columnQualifier,
                    Bytes.toBytes(e.getValue()));
            return put;
        }).collect(Collectors.toList());

        Object[] results = new Object[batch.size()];
        try {
            table.batch(batch, results);
            LogManager.getRootLogger().trace("data loaded to: " + table.getName());
        } catch (IOException e) {
            LogManager.getRootLogger().error("table batch IO error");
            throw new RuntimeException(e);
        } catch (InterruptedException e) {
            LogManager.getRootLogger().error("table batch interrupted error");
            throw new RuntimeException(e);
        }
        return results;
    }

}
