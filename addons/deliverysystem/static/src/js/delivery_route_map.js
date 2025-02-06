import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
class DeliveryRouteMap extends Component {
    setup() {
        this.action = useService("action");
        this.orm = useService("orm");
        this.routeId = this.props.routeId;
        this.stops = this.props.stops;
    }
    async mounted() {
        // Get API key from system parameters
        const apiKey = await this.orm.call('google.maps.helper', '_get_api_key', []);
        await this.loadGoogleMaps(apiKey);
        await this._initMap();
    }
    loadGoogleMaps(apiKey) {
        return new Promise((resolve, reject) => {
            if (window.google && window.google.maps) {
                resolve();
                return;
            }

            const script = document.createElement('script');
            script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}`;
            script.async = true;
            script.defer = true;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }
    async _initMap() {
        const mapElement = this.el.querySelector('#route_map');
        const map = new google.maps.Map(mapElement, {
            zoom: 12,
            center: { lat: 0, lng: 0 }
        });

        // Add markers for each stop
        this.stops.forEach((stop) => {
            const geocoder = new google.maps.Geocoder();
            geocoder.geocode({ 'address': stop.address }, (results, status) => {
                if (status === 'OK') {
                    new google.maps.Marker({
                        map: map,
                        position: results[0].geometry.location,
                        title: stop.address,
                        label: stop.sequence.toString()
                    });
                }
            });
        });
    }
}
DeliveryRouteMap.template = 'deliverysystem.RouteMap';
DeliveryRouteMap.components = {};
export const deliveryRouteMap = {
    component: DeliveryRouteMap,
};
registry.category("actions").add("delivery_route_map", deliveryRouteMap);