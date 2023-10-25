
function addRow() {
    var table = document.getElementById("mytable");
    var newRow = table.insertRow(table.rows.length);
    var cell = newRow.insertCell(0);
    
    var input1 = document.createElement("input");
      input1.type = "text";
      input1.id = "messages";
      cell.appendChild(input1);
  }

