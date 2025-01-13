// Basic DataTable
$(function(){
	$('#basicExample').DataTable({
		"lengthMenu": [[50, 100, 150, 200,], [50, 100, 150, 200, "All"]],
		"language": {
			"lengthMenu": "Відображати _MENU_ Записів на сторінці",
			"info": "Показувати _PAGE_ з _PAGES_",
		}
	});
});



// Vertical Scroll
$(function(){
	$('#scrollVertical').DataTable({
		"scrollY": "207px",
		"scrollCollapse": true,
		"paging": false,
		"bInfo" : false,
	});
});
// rolly
$(function(){
	$('#rolly').DataTable({
		"scrollCollapse": false,
		"paging": false,
		"bInfo" : false,
		"searching": false
	});
});



// Highlighting rows and columns
$(function(){
	$('#highlightRowColumn').DataTable({
		"lengthMenu": [[50, 100, 150, 200,], [50, 100, 150, 200, "All"]],
		"language": {
			"lengthMenu": "Відображати _MENU_ Записів на сторінці",
		}
	});
	var table = $('#highlightRowColumn').DataTable();  
	$('#highlightRowColumn tbody').on('mouseenter', 'td', function (){
		var colIdx = table.cell(this).index().column;
		$(table.cells().nodes()).removeClass('highlight');
		$(table.column(colIdx).nodes()).addClass('highlight');
	});
});



// Using API in callbacks
$(function(){
	$('#apiCallbacks').DataTable({
		"lengthMenu": [[50, 100, 150, 200,], [50, 100, 150, 200, "All"]],
		"language": {
			"lengthMenu": "Відображати _MENU_ Записів на сторінці",
		},
		"initComplete": function(){
			var api = this.api();
			api.$('td').on('click', function(){
			api.search(this.innerHTML).draw();
		});
		}
	});
});


// Hiding Search and Show entries
$(function(){
	$('#hideSearchExample').DataTable({
		"lengthMenu": [[50, 100, 150, 200,], [50, 100, 150, 200, "All"]],
		"language": {
			"lengthMenu": "Відображати _MENU_ Записів на сторінці",
			"info": "Показувати _PAGE_ з _PAGES_",
		}
	});
});