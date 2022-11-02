function initMap() {
    const map = new google.maps.Map(
        document.getElementById("map"),
        {
            zoom: 13,
            center: new google.maps.LatLng(-33.3977345, -70.770331),
        }
    );

//    Get available jobs via API
    fetch(apiUrl)
        .then(response => response.json())
        .then(json => {
                for (let job of json) {
                    const position = {lat: job.pickup_lat, lng: job.pickup_lng};
                    const market = new google.maps.Marker({
                        position: position,
                        map,
                        title: job.id
                    });

                    new google.maps.InfoWindow({
                        content: `<small><b>${job.name}</b></small><br><small>${job.distance} Km</small>`
                    }).open(map, market);
                }
            }
        )
}

window.initMap = initMap;
