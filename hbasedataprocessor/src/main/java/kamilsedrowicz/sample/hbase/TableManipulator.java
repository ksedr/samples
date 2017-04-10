package kamilsedrowicz.sample.hbase;

import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;
import org.apache.hadoop.hbase.TableExistsException;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.logging.log4j.LogManager;

import java.io.IOException;

/**
 * Contains methods for manipulating an HBase table:
 * - creating
 * - dropping
 */
public class TableManipulator {
    /**
     * Creates an HBase table with the specifies name and column family.
     * The new table is not created if a table with the specified name already exists.
     *
     * @param admin an HBase admin
     * @param tableName the name of the table to create
     * @param columnFamily the name of the column family that the table should contain
     * @return a table descriptor
     * @throws IOException IO exception while creating the table
     */
    public static HTableDescriptor createTable(Admin admin, String tableName, byte[] columnFamily)
            throws IOException {
        HTableDescriptor td = new HTableDescriptor(TableName.valueOf(tableName));
        td.addFamily(new HColumnDescriptor(columnFamily));try {
            admin.createTable(td);
            LogManager.getRootLogger().trace("table created: " + td.getNameAsString());
        } catch (TableExistsException e) {
            LogManager.getRootLogger().info("table " + td.getNameAsString() + " already exists");
        }
        return td;
    }

    /**
     * Drops an HBase table.
     *
     * @param admin an HBase admin
     * @param tableName the name of the table to drop
      @throws IOException IO exception while dropping the table
     */
    public static void dropTable(Admin admin, String tableName) throws IOException {
        admin.disableTable(TableName.valueOf(tableName));
        admin.deleteTable(TableName.valueOf(tableName));
    }
}
