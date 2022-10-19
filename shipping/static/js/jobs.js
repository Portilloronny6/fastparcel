document.querySelector('#cancel-job').addEventListener('click', (e) => {
    e.preventDefault();
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            document.querySelector('#cancel-job-form').submit();
        }
    })
});

function initMap() {
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    const map = new google.maps.Map(
        document.getElementById("map"),
        {
            zoom: 7,
            center: new google.maps.LatLng(-33.3977345, -70.770331),
        }
    );

    directionsRenderer.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsRenderer);
}

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    directionsService
        .route({
            origin: new google.maps.LatLng(pickupLat, pickupLng),
            destination: new google.maps.LatLng(deliveryLat, deliveryLng),
            travelMode: google.maps.TravelMode.DRIVING,
        })
        .then((response) => {
            directionsRenderer.setDirections(response);
        })
        .catch((e) => window.alert("Directions request failed due to " + e));
}

window.initMap = initMap;
