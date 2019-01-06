
/*
<body>
  <div id="floating-panel">
    <input id="address" type="textbox" value="Sydney, NSW">
    <input id="submit" type="button" value="Geocode">
  </div>
  <div id="map"></div>
  <script>
    function initMap() {
      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: {lat: -34.397, lng: 150.644}
      });
      var geocoder = new google.maps.Geocoder();

      document.getElementById('submit').addEventListener('click', function() {
        geocodeAddress(geocoder, map);
      });
    }

    function geocodeAddress(geocoder, resultsMap) {
      var address = document.getElementById('address').value;
      geocoder.geocode({'address': address}, function(results, status) {
      // how to get a geolocalisation data from a normal adress in "results"
        if (status === 'OK') {
          resultsMap.setCenter(results[0].geometry.location);
          var marker = new google.maps.Marker({
            map: resultsMap,
            position: results[0].geometry.location
          });
        } else {
          alert('Geocode was not successful for the following reason: ' + status);
        }
      });
    }
  </script>
  <script async defer
  src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap">
  </script>
</body>
</html>
*/


var clients = {
        client1: {
          center: {lat: 48.878, lng: 0},
          CA: 2714856,
          nom: "mboussa"
        },
        newyork: {
          center: {lat: 43.714, lng: 0},
          CA: 9405837,
          nom: "mboussa"
        },
        losangeles: {
          center: {lat: 44.052, lng: 5.1}, // lat = y, lng=x
          CA: 5857799,
          nom: "mboussa"
        },
        vancouver: {
          center: {lat: 49.25, lng: 0},
          CA: 1502,
          nom: "mboussa"
        }
      };

      function initMap() {
        // Create the map.
        var map = new google.maps.Map(document.getElementById('map_canvas'), {
          zoom: 6,

          center: {lat: 47.090, lng: 0},
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
