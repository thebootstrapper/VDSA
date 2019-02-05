if (session_id_com == null){
  var session_id_com = null
}
if (session_id_mag == null) {
  var session_id_mag = null
}


var filter = [null, session_id_com, session_id_mag, null, null]; // Dans l'ordre: id_client (sans la lettre), id_commercial, id_magasin, id_sousfamille, id_famille
var bool_ca = "True";





// = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
//                      Graph
// = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

var ctx = document.getElementById("myChart");



var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ["Septembre", "Octobre", "Novembre", "Decembre", "Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre"],
    datasets: [{
      label: '# of Votes',
      borderWidth: 3,
      borderColor: 'rgb(0, 27, 205)',
      fill: false
    },
    {
      label: '# of eeee',
      borderWidth: 2,
      borderColor: 'rgb(212, 0, 0)',
      borderDash: [4,8],
      fill: false
  }]
  },
  options: {
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true
        }
      }]
    }
  }
});



function fillBloc(id_bloc, l_num){
  var bloc = document.getElementById(id_bloc);
  var nb_var = bloc.getElementsByClassName("nb_var")[0];
  if (l_num[0]) {
    nb_var.innerHTML = l_num[0].toFixed(2);
  } else {nb_var.innerHTML = "";}
  var l_nb_fix = bloc.getElementsByClassName("nb_fix");
  if (l_num[1]) {
    l_nb_fix[0].innerHTML = l_num[1].toFixed(0);
  }else {l_nb_fix[0].innerHTML = "";}
  if (l_num[2]) {
    l_nb_fix[1].innerHTML = l_num[2].toFixed(0);
  } else {l_nb_fix[1].innerHTML = "";}
}

function applyChanges(data){
  fillBloc("nb_clt", data.nb_clt);
  fillBloc("nb_newclt", data.nb_newclt);
  fillBloc("ca_year", data.ca_year);
  fillBloc("marge_year", data.marge_year);
  myChart.data.datasets[0].label = data.graph_dates[0] + " - " + data.graph_dates[1];
  myChart.data.datasets[0].data = data.graph_data[0];
  myChart.data.datasets[1].label = data.graph_dates[1] + " - " + data.graph_dates[2];
  myChart.data.datasets[1].data = data.graph_data[1];
  myChart.update();
}


$(document).ready(function() {


  // = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
  //                      Formulaire dynamique
  // = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

  function buttonClicked(button) {
    var list_btn = document.getElementsByClassName("button-ca");
    for (var i = 0; i < list_btn.length; i++) {
      list_btn[i].className = "btn button-ca btn-default"
    }
    button.className += " selected";
    bool_ca = button.value;
    updateGraph();
  }

  function readIdCltInput(){
    var input = document.getElementById("input_id_clt");
    var re_id_clt = RegExp('^[vVdD]\\d+$');
    value = input.value;
    if (re_id_clt.test(value)) {
      id_mag = value.slice(0,1).toUpperCase();
      id_clt = value.slice(1);
      input.value = id_mag + id_clt;
      filter[0] = id_clt;
      filter[2] = id_mag;
      document.getElementById("active_id_clt").innerHTML = id_mag + id_clt;
      document.getElementById("search_row").style.display = "inline-block";
      updateGraph();
    }
  }

  function eraseIdClt(){
    filter[0] = null;
    filter[2] = session_id_mag;
    document.getElementById("input_id_clt").value = "";
    document.getElementById("search_row").style.display = "none";
  }


  var list_btn = document.getElementsByClassName("button-ca");
  for (var i = 0; i < list_btn.length; i++) {
    list_btn[i].addEventListener("click", function(){buttonClicked(this)});
  }

  var input_id_clt = document.getElementById("input_id_clt");
  input_id_clt.addEventListener("keydown", function(e){
    if (e.key == "Enter"){readIdCltInput()}
  })
  var btn_submit_id_clt = document.getElementById("btn_submit_id_clt");
  btn_submit_id_clt.addEventListener("click", function(){readIdCltInput()});

  var a_close_id_clt = document.getElementById("a_close_id_clt");
  a_close_id_clt.addEventListener("click", function(){eraseIdClt(); updateGraph();});







  // = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
  //                               AJAX
  // = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


  $('#sel_com').change(function(){
    filter[1]= document.getElementById("sel_com").value;
    updateGraph();
  })

  $('#sel_mag').change(function(){
    eraseIdClt();
    filter[2]=document.getElementById("sel_mag").value;
    updateGraph();
  })



  $("#sel_fam").change(function() {
    id_fam= document.getElementById("sel_fam").value;
    filter[3]= null;
    filter[4]= id_fam;
    updateGraph();


    //charger les sous familles
    $.ajax({
      type:"POST",
      url:"/dashboard/sql_list_sous_fam/",
      data: {
        'id_fam': id_fam
      },
      success: function(json_data){
        var sous_familles = JSON.parse(json_data);

        var select = document.getElementById("sel_sfam");

        var html = '<OPTION value="">Sous famille (toutes par défauts)</OPTION>';

        for( var sous_f in sous_familles){
          html +='<OPTION value="' + sous_familles[sous_f][0]+'"> '
            +  sous_familles[sous_f][1] + '</OPTION>'
        }
        select.innerHTML = html;
      }
    });
  })


  $("#sel_sfam").change( function(){
    filter[3] = document.getElementById("sel_sfam").value;
    updateGraph();
  })

  function updateGraph(){
    console.log(filter);
    console.log(bool_ca);

    $.ajax({
      type:"POST",
      url:"/dashboard/sql_get_table_data/",
      data: {
        'filter[]': filter,
        'bool_ca': bool_ca
      },
      success: function(json_data){
        var data = JSON.parse(json_data);
        applyChanges(data);
      }
    });
  }

  updateGraph();

});
