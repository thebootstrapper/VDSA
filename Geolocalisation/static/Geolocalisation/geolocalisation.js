
/*
Ce json contient pour chaque adrese les données suivantes :
id: l'identifiant de l'adresse dans la base de donnée
cp: code postale
ville: la ville
chiffre: le choffre d 'affaire ou la marge
*/
var clients = {

        client1: {
            id: 5,
            cp: 75000,
            ville: "lyon",
            chiffre: 400,
        },
        newyork: {
            id: 5,
            cp: 95000,
            ville: "Cergy",
            chiffre: 4000,
        },
      };



/* cette foinction recherche la latitude et la longitude d'une addresse et l'affiche sur la carte */
      function geocodeAddress(geocoder, data,map) {
              for (var client in data) {
                // si le Chiffre d'affaire ou la marge est un numérique
                  if ( $.isNumeric(data[client].chiffre) == true){

                      var address = data[client].ville + " "+ data[client].cp  ;

                      // recherche de la latitude et de la longitude
                      geocoder.geocode({'address': address}, function(results, status) {
                        console.log(status);

                      // si les coordonnées ont été trouvées
                        if (status === 'OK') {

                          var mIcon = {
                               path: google.maps.SymbolPath.CIRCLE,
                               fillOpacity: 0.4,
                               fillColor: 'blue',
                               strokeOpacity: 1,
                               strokeWeight: 1,
                               strokeColor: '#333',
                               scale:  50// trouver une formaule en fonction du CA pour qu'il s''affiche dans le cercle .ex:(Math.sqrt(clients[client].CA) / 100)
                             };

                             var gMarker = new google.maps.Marker({
                               map: map,
                               position: results[0].geometry.location,
                               title: address,
                               icon: mIcon,
                               label: {color: 'white', fontSize: '12px', fontWeight: '600',
                               text: data[client].chiffre+""}
                             });
                        }
                      });

                    }
              }
          }



      function initMap() {
        // Create the map.
        var map = new google.maps.Map(document.getElementById('map_canvas'), {
          zoom: 6,

          center: {lat: 47.090, lng: 0},
        });


        var geocoder = new google.maps.Geocoder();
        geocodeAddress(geocoder, clients,map)

      }
