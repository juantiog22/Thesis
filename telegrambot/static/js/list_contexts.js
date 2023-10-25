
function addRow() {
  var table = document.getElementById("mytable");
  var newRow = table.insertRow(table.rows.length);
  var cell = newRow.insertCell(0);
  
  var input1 = document.createElement("input");
    input1.type = "text";
    input1.name = "messages"; 
    cell.appendChild(input1);
}

function deleteRow() {
  var table = document.getElementById("mytable");
  if (table.rows.length > 1) {
    table.deleteRow(table.rows.length - 1);
  } else {
    alert("Cannot delete the last row.");
  }
}


$( document ).ready(function() {


    $('.show_confirm').click(function(event) {
        var url = $(this).attr('url');
        var form =  $(this).closest("form");
        var context = $(this).attr('name');
        event.preventDefault();
        event.stopPropagation();
        Swal.fire({
          title: `Are you sure you want to delete the Context: `,
          text: context,
          icon: "warning",
          showCancelButton: true,
          confirmButtonText: 'Delete',
          cancelButtonText: 'Cancel',
        })
        .then(function(result) {
          if (result.isConfirmed) {
            form.submit();
          }
        });
      });

    $('.add').click(function(event) {
      event.preventDefault();
      event.stopPropagation();
    });

    
    $('.del').click(function(event) {
      event.preventDefault();
      event.stopPropagation();
    });
  
    const rows = document.querySelectorAll("tr[data-href]");
    rows.forEach(row => {
      row.addEventListener('click', () => {
          window.location.href = row.dataset.href;
      });
    });

      
  });
  
  
  
  
  
  


