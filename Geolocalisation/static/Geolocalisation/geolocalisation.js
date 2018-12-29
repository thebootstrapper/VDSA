
var clients = {
        client1: {
          center: {lat: 41.878, lng: -87.629},
          CA: 2714856,
          nom: "mboussa"
        },
        newyork: {
          center: {lat: 40.714, lng: -74.005},
          CA: 9405837,
          nom: "mboussa"
        },
        losangeles: {
          center: {lat: 34.052, lng: -118.243},
          CA: 5857799,
          nom: "mboussa"
        },
        vancouver: {
          center: {lat: 49.25, lng: -123.1},
          CA: 1502,
          nom: "mboussa"
        }
      };

      function initMap() {
        // Create the map.
        var map = new google.maps.Map(document.getElementById('map_canvas'), {
          zoom: 4,

          center: {lat: 37.090, lng: -95.712},
        });

        // Construct the circle for each value in citymap.
        // Note: We scale the area of the circle based on the population.
        for (var client in clients) {

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
               position: clients[client].center,
               title: "Client: "+clients[client].nom,
               icon: mIcon,
               label: {color: 'white', fontSize: '12px', fontWeight: '600',
                 text: clients[client].CA+""}
             });
  /*
          // Add the circle for this city to the map.
          var cityCircle = new google.maps.Circle({
            strokeColor: '#FF0000',
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: '#FF0000',
            fillOpacity: 0.35,
            label: "essaie",
            map: map,
            center: citymap[city].center,
            radius: Math.sqrt(citymap[city].CA) * 100
          });

          */
        }
      }



initMap();
