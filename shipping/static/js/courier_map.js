function initMap() {
    new google.maps.Map(
        document.getElementById("map"),
        {
            zoom: 13,
            center: new google.maps.LatLng(-33.3977345, -70.770331),
        }
    );
}

window.initMap = initMap;
