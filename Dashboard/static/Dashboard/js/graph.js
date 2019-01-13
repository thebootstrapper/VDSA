$(document).ready(function() {
  // JQuery code to be added in here.

  $('#id_sql_clt_search').click(function(event){
    $.ajax({
      type:"POST",
      url:"/dashboard/sql_clt_search/",
      data: {'id_input[]': ["lol", "lil", "lolu"]},
      success: function(x){
        console.log(x);
      }
    });
    return false;
  });


  $('#id_sql_get_table_data').click(function(event){
    $.ajax({
      type:"POST",
      url:"/dashboard/sql_get_table_data/",
      data: {
        'filter[]': [666, 12, 'V', null, null],
        'bool_ca': true
      },
      success: function(json_data){
        var data = JSON.parse(json_data);
        console.log(data);
      }
    });
    return false;
  });


});
