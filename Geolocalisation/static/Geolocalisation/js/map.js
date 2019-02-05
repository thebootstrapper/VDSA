

/*

parametre en entrée: un réel qui correspont au du chiffre d'affaire ( ou marge)
cette fonction retourne une chaine de caractère: "blue" ou "red", qui correspond à la couleur du cercle sur la carte.
 Si le chiffre d'affaire est négatif, la couleur retournée est "red",si non c'est "blue".
*/
function getCouleur(value){
  if ( value < 0)
    return "red"
  else
    return "blue"
}

/*

cette fonction retourne le minimum des chiffres d'affaire( ou marge).
*/
function min(data){
  var min = Number.MAX_SAFE_INTEGER

    for ( client in data){
      if ( $.isNumeric(data[client].value) == true &&  data[client].value <min)
          min = data[client].value;
    }

    return min;
}

/*
cette fonction retourne le maximum des chiffres d'affaire( ou marge).
*/
function max(data){
  var max = Number.MIN_SAFE_INTEGER;

  for ( client in data){
    if ( $.isNumeric(data[client].value) == true &&  data[client].value  > max)
        max = data[client].value;
  }

  return max;
}


/*

parametres en entrés:
clients: tableaux de listes, tel que chaque liste contient l'identifiant de la localisation, le code  postale, le nom de la ville et le chiffre d'affire ou la marge

retour:
cette fonction retourne un tableau de réels. Chaque réel correspond au diamettre du cercle qui s'affichera pour chaque chiffre d'affaire(ou marge).
Nous avons à ce que ce diametre démonde du chiffre d'afffaire (ou des marges) afin que les différences soient facilement visible. Mais sachant que le chiffre d'affaire et les marges sont des nombres très variables, à partir de cette fonction, nous avons réussit à avoir un tableau de diametres à partir d'un tableau de de chiffre d'affaire(ou marge).

*/
function getScale(data){

  var echelle = new Array();
  var min_echelle = 20;
  var max_echelle = 70;
  var client_echelle;

  var min_value = min(data);
  var max_value = max(data);

  for ( client in data){
    echelle[client]= ((data[client].value - min_value )/(max_value - min_value))*(max_echelle -  min_echelle) + min_echelle;
  }
  return echelle;
}


/* Cette fonction me à jour la map à en fonction du contenu du formulaire */

function updateMap(){


  bool_cal= $("#ca_label").hasClass("active");
  console.log( "bool_ca: "+bool_cal);


  var is_admin=document.forms["sous_famille_form"].elements[1].value
  console.log(is_admin)
  if (is_admin == 0){
        id_commercial=null;
        id_magasin=null;

  }
  else{

  id_commercial= document.forms["representant_form"].elements[0].value;
  if(id_commercial=="null")// car il recupère la valeur du champs en chaine de caractere
      id_commercial=null;

  id_magasin = document.forms["representant_form"].elements[1].value;
  if(id_magasin=="null")// car il recupère la valeur du champs en chaine de caractere
      id_magasin=null;
  console.log("id_magasin: "+id_magasin);

  }
  id_famille = document.forms["famille_form"].elements[0].value;
  if(id_famille=="null")// car il recupère la valeur du champs en chaine de caractere
      id_famille=null;
  console.log("id_famille: "+id_famille);

  id_sousfamille = document.forms["sous_famille_form"].elements[0].value;
  if(id_sousfamille=="null")// car il recupère la valeur du champs en chaine de caractere
      id_sousfamille=null;
  console.log("id_sousfamille : "+id_sousfamille);



  $.ajax({
    type:"POST",
    url:"/dashboard/sql_get_geoloc_data/",
    data: {
      'filter[]': [null,  id_commercial, id_magasin, id_sousfamille, id_famille ],
      // bool_cal : bool_cal,
    //  'filter[]': [null, null, null, null, null],
      'bool_ca': true
    },
    success: function(json_data){
      var clients = JSON.parse(json_data);


      // Create the map.
      var map = new google.maps.Map(document.getElementById('map_canvas'), {
        zoom: 6,

        center: {lat: 47.090, lng: 0},
      });


      console.log("liste des clients:")
      console.log(clients)
      var echelle = getScale(clients);
      var geocoder = new google.maps.Geocoder();

      for (var client in clients){
      geocodeAddress(geocoder, clients[client],echelle[client],map);
      }
    }

  })

  }




/* cette foinction recherche la latitude et la longitude d'une addresse et l'affiche sur la carte
parametre en trées:
-geocoder: un objet fournis par google map qui permet d'avoir la latitude et la longitude du l'adresse
-client: une liste d'information sur la localisation d'un client conteneant l'identifiant de la localisation, le code  postale, le nom de la ville et le chiffre d'affire ou la marge.
- echelle_valeur: qui est le diametre du cercle à afficher sur la catre.
-map: qui représente la carte
*/

      function geocodeAddress(geocoder, client,echelle_valeur,map) {

                // si le Chiffre d'affaire ou la marge est un numérique
              if ( $.isNumeric(client.value) == true){

                  var address = client.ville + " "+ client.cp  ;
                  // recherche de la latitude et de la longitude du client
                  geocoder.geocode({'address': address}, function(results, status) {

                  //couleur du cercle sur la map
                  var couleur = getCouleur(client.value)
                      //on affiche les résultats sur la carte que si les coordonnées ont été trouvées
                        if (status === 'OK') {

                            // creation du cercle à afficher
                          var mIcon = {
                               path: google.maps.SymbolPath.CIRCLE,
                               fillOpacity: 0.4,
                               fillColor: couleur,
                               strokeOpacity: 1,
                               strokeWeight: 1,
                               strokeColor: '#333',
                               scale:   echelle_valeur
                             };

                              // ajout du cercle dans sur la carte
                             var gMarker = new google.maps.Marker({
                               map: map,
                               position: results[0].geometry.location,
                               title: address,
                               icon: mIcon,
                               label: {color: 'white', fontSize: '12px', fontWeight: '600',
                               text: client.value+" "}
                             });
                        }
                        else // si l'adresse n 'est pas retrouvée, on l'affiche dans la console pour débeugé
                        {

                          var address = client.ville + " "+ client.cp  ;
                          console.log("erreur :"+status + "\n l'addresse introuvable est :"+address)
                        }

                      });
                }
          }



/*
Cette fonction initialise la carte fau chargement de la page
*/

      function initMap() {

        var bool_cal=true;
        var id_commercial= null;
        var id_magasin = null;
        var id_sousfamille = null;
        var id_famille = null;

        // initialisation des des champs à partir du contenu de formulaire
          bool_cal= $("#ca_label").hasClass("active");
          console.log( "bool_ca: "+bool_cal);


          var is_admin=document.forms["sous_famille_form"].elements[1].value
          console.log(is_admin)
          if (is_admin == 0){
                id_commercial=null;
                id_magasin=null;

          }
          else{

          id_commercial= document.forms["representant_form"].elements[0].value;
          if(id_commercial=="null")// car il recupère la valeur du champs en chaine de caractere
              id_commercial=null;

          id_magasin = document.forms["representant_form"].elements[1].value;
          if(id_magasin=="null")// car il recupère la valeur du champs en chaine de caractere
              id_magasin=null;
          console.log("id_magasin: "+id_magasin);

          }

          id_famille = document.forms["famille_form"].elements[0].value;
          if(id_famille=="null")// car il recupère la valeur du champs en chaine de caractere
              id_famille=null;
          console.log("id_famille: "+id_famille);

          id_sousfamille = document.forms["sous_famille_form"].elements[0].value;
          if(id_sousfamille=="null")// car il recupère la valeur du champs en chaine de caractere
              id_sousfamille=null;
          console.log("id_sousfamille : "+id_sousfamille);



          $(document).ready(function() {

              // exécution de la fonction updateMap() quand on change de représentant
              $(".representant").change(function() {
                  updateMap();
              });

              // exécution de la fonction updateMap() quand on change de magasin
              $(".magasin").change(function() {
                  updateMap();
                });

              $(".famille").change(function() {
                    id_famille = document.forms["famille_form"].elements[0].value;
                  //charger les sous famille
                    console.log(id_famille);

                  if(id_famille=="null"){
                    console.log("toutes les familles")
                  }
                  else {
                        $.ajax({
                          type:"POST",
                          url:"/dashboard/sql_list_sous_fam/",
                          data: {
                            'id_fam': id_famille
                          },
                          success: function(json_data){
                            var sous_familles = JSON.parse(json_data);
                            // rajouter les sous familles en jquery
                            console.log("sous famille: "+sous_familles)
                            var select = $(" .sous_famille");
                            var html = '<OPTION value="null"> Toutes les sous familles </OPTION>';

                            for( var sous_f in sous_familles){
                              html +='<OPTION value="' + sous_familles[sous_f][0]+'"> '
                                      +  sous_familles[sous_f][1] + '</OPTION>'
                            }
                            select.children().remove();
                            select.append(html);

                          }
                        });
                      }

                   updateMap();
                });


              $(".sous_famille").change(function() {
                  updateMap();
                });

          });

        $.ajax({
          type:"POST",
          url:"/dashboard/sql_get_geoloc_data/",
          data: {
            'filter[]': [null, id_commercial, id_magasin, id_sousfamille, id_famille],
            'bool_ca': bool_cal
          },
          success: function(json_data){
            var clients = JSON.parse(json_data);


            // Create the map.
            var map = new google.maps.Map(document.getElementById('map_canvas'), {
              zoom: 6,

              center: {lat: 47.090, lng: 0},
            });

            var echelle = getScale(clients);
            console.log("echelle :"+echelle);


            console.log("liste des clients:")
            console.log(clients)
            var geocoder = new google.maps.Geocoder();
          //  geocodeAddress(geocoder, clients,echelle,map)
            for (var client in clients){
            geocodeAddress(geocoder, clients[client],echelle[client],map);
            }
          }
        });


      }
