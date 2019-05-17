$(document).ready(function () {
    // configurations for initial map rendering
    var center = L.bounds([1.3446314,103.6769616], [1.3524204,103.6874623]).getCenter();
    var map = L.map('mapdiv').setView([center.x, center.y], 15);
    var basemap = L.tileLayer('https://maps-{s}.onemap.sg/v3/Default/{z}/{x}/{y}.png', {
        detectRetina: true,
        maxZoom: 18,
        minZoom: 15
    });
    
    basemap.addTo(map);

    // variables to store all marker objects & marker states
    var markerList = [];
    var defaultState = L.AwesomeMarkers.icon({icon : 'utensils', prefix : 'fa', markerColor : 'red', iconColor : 'white'});
    var clickedState = L.AwesomeMarkers.icon({icon : 'utensils', prefix : 'fa', markerColor : 'cadetblue', iconColor : 'white'});

    /**
     * renders markers on a given latitude & longitude
     */
    function showPosition(position) {      
        marker = new L.Marker([position.coords.latitude, position.coords.longitude], {bounceOnAdd: false, icon: defaultState, places: position.coords.subarea}).addTo(map);                 
        markerList.push(marker);
        marker.addEventListener('click', showDetails);
    }

    /**
     * renders dining areas in a given marker
     */
    function showDetails(marker){
        resetMarkers();
        marker.target.setIcon(clickedState);
        displayPlaces(marker.target.options.places);
    }

    /**
     * reset all markers to default icon
     */
    function resetMarkers(){
        for (var i = 0; i < markerList.length; i++){
            markerList[i].setIcon(defaultState);
        }
    }

    /**
     * render the initial state of the map
     */
    function showInitialRender(marker){
        marker.setIcon(clickedState);
        displayPlaces(marker.options.places);
    }

    /**
     * display nearby places of a marker
     */
    function displayPlaces(placeList){
        $('#map-result-list').children().remove();
        for (var i = 0; i < placeList.length; i++){
            var url = "/webapp/search?q=" + placeList[i];
            var encodeURL = encodeURI(url);
            $('#map-result-list').append("<a href='"+ encodeURL +"'><li>" + placeList[i] + "</li></a>");
        }
    }

    // list of coordinates
    var position = [];
    var placeList = JSON.parse(document.getElementById('nearby_places-data').textContent);

    for (place in placeList){
        position.push({coords : 
                        {latitude : placeList[place].latitude, 
                        longitude : placeList[place].longitude, 
                        subarea : placeList[place].subarea}
                    });
    }

    for (var i = 0; i < position.length; i++){
        showPosition(position[i]);
    }

    if (markerList.length != 0){
        showInitialRender(markerList[0]);
    }
});