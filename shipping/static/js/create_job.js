function initMapByType(type, latitude, longitude) {
    const map = new google.maps.Map(document.getElementById(type + "-map"), {
        center: new google.maps.LatLng(latitude || -33.3977345, longitude || -70.770331),
        zoom: 15,
    });


    // [START maps_places_autocomplete_creation]
    const center = new google.maps.LatLng(latitude || -33.3977345, longitude || -70.770331);
    // Create a bounding box with sides ~10km away from the center point
    const defaultBounds = {
        north: center.lat + 0.1,
        south: center.lat - 0.1,
        east: center.lng + 0.1,
        west: center.lng - 0.1,
    };
    const input = document.getElementById("id_" + type + "_address");
    const options = {
        bounds: defaultBounds,
        componentRestrictions: {country: "cl"},
        fields: ["address_components", "geometry", "icon", "name"],
        strictBounds: false,
    };
    const autocomplete = new google.maps.places.Autocomplete(input, options);

    // [END maps_places_autocomplete_creation]
    // Set initial restriction to the greater list of countries.
    // [START maps_places_autocomplete_countries_multiple]
    autocomplete.setComponentRestrictions({
        country: ["cl"],
    });

    // [END maps_places_autocomplete_countries_multiple]
    // [START maps_places_autocomplete_setbounds]
    // const southwest = {lat: 5.6108, lng: 136.589326};
    // const northeast = {lat: 61.179287, lng: 2.64325};
    // const newBounds = new google.maps.LatLngBounds(southwest, northeast);
    //
    // autocomplete.setBounds(newBounds);

    // [END maps_places_autocomplete_setbounds]
    const infowindow = new google.maps.InfoWindow();
    const infowindowContent = document.getElementById(type + "-infowindow-content");

    infowindow.setContent(infowindowContent);

    const marker = new google.maps.Marker({
        map,
        position: new google.maps.LatLng(latitude || -33.3977345, longitude || -70.770331),
    });

    autocomplete.addListener("place_changed", () => {
        infowindow.close();
        marker.setVisible(false);

        const place = autocomplete.getPlace();
        document.querySelector("#" + type + "-lat").value = place.geometry.location.lat();
        document.querySelector("#" + type + "-lng").value = place.geometry.location.lng();

        if (!place.geometry || !place.geometry.location) {
            // User entered the name of a Place that was not suggested and
            // pressed the Enter key, or the Place Details request failed.
            window.alert("No details available for input: '" + place.name + "'");
            return;
        }

        // If the place has a geometry, then present it on a map.
        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(17); // Why 17? Because it looks good.
        }

        marker.setPosition(place.geometry.location);
        marker.setVisible(true);

        let address = "";

        if (place.address_components) {
            address = [
                (place.address_components[0] &&
                    place.address_components[0].short_name) ||
                "",
                (place.address_components[1] &&
                    place.address_components[1].short_name) ||
                "",
                (place.address_components[2] &&
                    place.address_components[2].short_name) ||
                "",
            ].join(" ");
        }

        infowindowContent.children[type + "-place-icon"].src = place.icon;
        infowindowContent.children[type + "-place-name"].textContent = place.name;
        infowindowContent.children[type + "-place-address"].textContent = address;
        infowindow.open(map, marker);
    });
}

function initMap() {
    initMapByType("pickup", pickupLat, pickupLng);
    initMapByType("delivery", deliveryLat, deliveryLng);
}

window.initMap = initMap;