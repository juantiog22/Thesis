
$( document ).ready(function() {


    $('.show_confirm').click(function(event) {
        var url = $(this).attr('url');
        var form =  $(this).closest("form");
        var context = $(this).attr('name');
        event.preventDefault();
        event.stopPropagation();
        Swal.fire({
          title: `Are you sure you want to delete the Preamble: `,
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

    const rows = document.querySelectorAll("tr[data-href]");
    rows.forEach(row => {
      row.addEventListener('click', () => {
          window.location.href = row.dataset.href;
      });
    });

      
  });
  
  
  
  
  
  


