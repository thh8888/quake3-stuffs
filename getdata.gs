function Get_Data() { 
// Replace the variables in this block with real values.
var address = 'dbinstance-endpoint.something.somewhere'; //End point provided by the RDS Instance
// var rootPwd = 'root_password'; //Root password given while configuring DB instance
var user = 'dbuser'; //Username given while configuring DB instance
var userPwd = 'dbpassword'; //User password given while configuring DB instance
var db = 'dbname'; //Database name to which you want to connect
 
var dbUrl  = 'jdbc:mysql://' + address + '/' + db; //Generates the database url to which you can connect to
var conn = Jdbc.getConnection(dbUrl, user, userPwd);

var ss = SpreadsheetApp.getActiveSpreadsheet(); /* This represents the whole data */
var sheet = ss.getSheetByName("sheetname in your Spreadsheet"); /* Replace with your own spreadsheet name */

var stmt = conn.createStatement();
var store_results = stmt.executeQuery('SELECT * FROM players');
var numCols = store_results.getMetaData().getColumnCount();

// Put data starting in row 2 to allow you to put header line in the first row.
var row = 2;
  
while (store_results.next()) {
 var rowString = ' ';
 var cellString = '';
 for (var column = 0; column < numCols; column++) {
     cellString = store_results.getString(column + 1);
     rowString += store_results.getString(column + 1) + '\t';
     sheet.getRange(row,column +1).setValue(cellString);
     }
 row += 1;
 Logger.log(rowString);
 }
 store_results.close();
 stmt.close();
  
}

