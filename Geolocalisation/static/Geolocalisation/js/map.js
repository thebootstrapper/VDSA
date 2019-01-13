

/*

je n ai pas la bonne valeur sur les cercles */
function getCouleur(value){
  if ( value < 0)
    return "red"
  else
    return "blue"
}


function min(data){
  var min = Number.MIN_SAFE_INTEGER

    for ( client in data){
      if ( $.isNumeric(data[client].value) == true &&  data[client].value <min)
          min = data[client].value;
    }

    return min;
}

function max(data){
  var max = Number.MAX_SAFE_INTEGER;

  for ( client in data){
    if ( $.isNumeric(data[client].value) == true &&  data[client].value  > max)
        min = data[client].value;
  }

  return max;
}

function getScale(data){
   var echelle = new Array();
  var min_echelle = 10;
  var max_echelle = 50;
  var client_echelle;

  var min_value = min(data);
  var max_value = max(data);



  for ( client in data){
    echelle[client]= (data[client].value - min_value )*(max_echelle -  min_echelle)/(max_value - min_value);
  }
  return echelle;
}


/*
Ce json contient pour chaque adrese les données suivantes :
id: l'identifiant de l'adresse dans la base de donnée
cp: code postale
ville: la ville
chiffre: le choffre d 'affaire ou la marge
*/



/* cette foinction recherche la latitude et la longitude d'une addresse et l'affiche sur la carte */
      function geocodeAddress(geocoder, data,map) {

              var echelle = getScale(data)
          //    console.log(echelle)
console.log(data)
              for (var client in data) {
                // si le Chiffre d'affaire ou la marge est un numérique
                  if ( $.isNumeric(data[client].value) == true){

                      var address = data[client].ville + " "+ data[client].cp  ;
                      // recherche de la latitude et de la longitude
                      geocoder.geocode({'address': address}, function(results, status) {
                  //      console.log(address);

                  var couleur = getCouleur(data[client].value)
                      // si les coordonnées ont été trouvées
                        if (status === 'OK') {

                            console.log(data[client])
                          var mIcon = {
                               path: google.maps.SymbolPath.CIRCLE,
                               fillOpacity: 0.4,
                               fillColor: couleur,
                               strokeOpacity: 1,
                               strokeWeight: 1,
                               strokeColor: '#333',
                               // echelle[client]
                               scale:  65// trouver une formaule en fonction du CA pour qu'il s''affiche dans le cercle .ex:(Math.sqrt(clients[client].CA) / 100)
                             };

                             var gMarker = new google.maps.Marker({
                               map: map,
                               position: results[0].geometry.location,
                               title: address,
                               icon: mIcon,
                               label: {color: 'white', fontSize: '12px', fontWeight: '600',
                               text: data[client].value+" "}
                             });
                        }
                        else{

                          var address = data[client].ville + " "+ data[client].cp  ;
                          console.log("erreur :"+status + "\n l'addresse introuvable est :"+address)
                        }
                      });

                    }
              }
          }





      function initMap() {

        var bool_cal=false;
        var id_commercial= null;
        var id_magasin = null;
        var id_sousfamille = null;
        var id_famille = null;
/*
          $(document).ready(function() {


            $(".chiffre").change(function() {

              bool_cal = $(this).value;
              id_commercial= $(".representant").value;
              id_magasin =   $(".magasin").value;
              id_sousfamille = $(".sous_famille").value;
              id_famille = $(".falille").value;

              $.ajax({
                type:"POST",
                url:"/dashboard/sql_get_geoloc_data/",
                data: {
                  //'filter[]': [null,  id_commercial, id_magasin, id_sousfamille, id_famille ]
                  // bool_cal : bool_cal
                  'filter[]': [null, null, null, null, null],
                  'bool_ca': true
                },
                success: function(json_data){
                  var clients = JSON.parse(json_data);


                  // Create the map.
                  var map = new google.maps.Map(document.getElementById('map_canvas'), {
                    zoom: 6,

                    center: {lat: 47.090, lng: 0},
                  });

                  var geocoder = new google.maps.Geocoder();
                  geocodeAddress(geocoder, clients,map)
                }
              });

            });

          $(".representant").change(function() {
            id_commercial = $(this).value;bool_cal = $(this).value;
            id_commercial= $(".representant").value;
            id_magasin =   $(".magasin").value;
            id_sousfamille = $(".sous_famille").value;
            id_famille = $(".falille").value;

            $.ajax({
              type:"POST",
              url:"/dashboard/sql_get_geoloc_data/",
              data: {
                //'filter[]': [null,  id_commercial, id_magasin, id_sousfamille, id_famille ]
                // bool_cal : bool_cal
                'filter[]': [null, null, null, null, null],
                'bool_ca': true
              },
              success: function(json_data){
                var clients = JSON.parse(json_data);


                // Create the map.
                var map = new google.maps.Map(document.getElementById('map_canvas'), {
                  zoom: 6,

                  center: {lat: 47.090, lng: 0},
                });

                var geocoder = new google.maps.Geocoder();
                geocodeAddress(geocoder, clients,map)
              }
            });

          });

          $(".magasin").change(function() {
            id_magasin = $(this).value;bool_cal = $(this).value;
            id_commercial= $(".representant").value;
            id_magasin =   $(".magasin").value;
            id_sousfamille = $(".sous_famille").value;
            id_famille = $(".falille").value;

            $.ajax({
              type:"POST",
              url:"/dashboard/sql_get_geoloc_data/",
              data: {
                //'filter[]': [null,  id_commercial, id_magasin, id_sousfamille, id_famille ]
                // bool_cal : bool_cal
                'filter[]': [null, null, null, null, null],
                'bool_ca': true
              },
              success: function(json_data){
                var clients = JSON.parse(json_data);


                // Create the map.
                var map = new google.maps.Map(document.getElementById('map_canvas'), {
                  zoom: 6,

                  center: {lat: 47.090, lng: 0},
                });

                var geocoder = new google.maps.Geocoder();
                geocodeAddress(geocoder, clients,map)
              }
            });

            });

*/
          $(".famille").change(function() {
            id_famille = document.forms["famille_form"].elements[0].value;
console.log(id_famille)
//charger les sous familles
                $.ajax({
                  type:"POST",
                  url:"/Geolocalisation/sql_list_sous_fam/",
                  data: {
                    'famille': id_famille
                  },
                  success: function(json_data){
                    var sous_familles = JSON.parse(json_data);
                    // rajouter les sous familles en jquery
                    console.log(sous_familles)

                  }
                });

            });

/*
          $(".sous_famille").change(function() {
            var id_famille = $(".famille").value;bool_cal = $(this).value;
            id_commercial= $(".representant").value;
            id_magasin =   $(".magasin").value;
            id_sousfamille = $(".sous_famille").value;
            id_famille = $(".falille").value;

            $.ajax({
              type:"POST",
              url:"/dashboard/sql_get_geoloc_data/",
              data: {
                //'filter[]': [null,  id_commercial, id_magasin, id_sousfamille, id_famille ]
                // bool_cal : bool_cal
                'filter[]': [null, null, null, null, null],
                'bool_ca': true
              },
              success: function(json_data){
                var clients = JSON.parse(json_data);


                // Create the map.
                var map = new google.maps.Map(document.getElementById('map_canvas'), {
                  zoom: 6,

                  center: {lat: 47.090, lng: 0},
                });

                var geocoder = new google.maps.Geocoder();
                geocodeAddress(geocoder, clients,map)
              }
            });

            });

          });
*/
        $.ajax({
          type:"POST",
          url:"/dashboard/sql_get_geoloc_data/",
          data: {
            //'filter[]': [null,  id_commercial, id_magasin, id_sousfamille, id_famille ]
            // bool_cal : bool_cal
            'filter[]': [null, null, null, null, null],
            'bool_ca': true
          },
          success: function(json_data){
            var clients = JSON.parse(json_data);


            // Create the map.
            var map = new google.maps.Map(document.getElementById('map_canvas'), {
              zoom: 6,

              center: {lat: 47.090, lng: 0},
            });

            var geocoder = new google.maps.Geocoder();
            geocodeAddress(geocoder, clients,map)
          }
        });


      }
