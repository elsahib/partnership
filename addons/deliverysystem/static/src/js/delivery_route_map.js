/** @odoo-module **/

import { Component, useRef, onMounted } from "@odoo/owl";

export class DeliveryRouteMap extends Component {
    static template = "deliverysystem.DeliveryRouteMap";
    static props = {
        routeId: { type: Number },
        stops: { type: Array },
        apiKey: { type: String },
        polyline: { type: String },
    };
    
    setup() {
        this.map_ids = '25bca46518f5ae1c';
        this.routeId = this.props.routeId;
        this.stops = this.props.stops;
        this.apiKey = this.props.apiKey;
        this.polyline = this.props.polyline;
        this.mapRef = useRef("route_map");

        onMounted(() => {
            console.log('DeliveryRouteMap mounted');
            this.initializeMap();
        });
    }

    loadGoogleMaps() {
        return new Promise((resolve, reject) => {
            if (window.google && window.google.maps && window.google.maps.marker) {
                console.log('Google Maps API already loaded');
                resolve(window.google.maps);
                return;
            }

            window.initMap = () => {
                console.log('Google Maps API initialized');
                resolve(window.google.maps);
            };

            const script = document.createElement('script');
            script.src = `https://maps.googleapis.com/maps/api/js?key=${this.apiKey}&callback=initMap&loading=async&v=weekly&libraries=marker,places,geometry&map_ids=${this.map_ids}`;
            script.async = true;
            script.defer = true;
            script.onerror = (e) => {
                console.error('Failed to load Google Maps API:', e);
                reject(e);
            };
            document.head.appendChild(script);
        });
    }

    async initializeMap() {
        try {
            const googleMaps = await this.loadGoogleMaps();
            await this._initMap(googleMaps);
        } catch (error) {
            console.error('Error initializing map:', error);
        }
    }

    async _initMap(googleMaps) {
        if (!this.mapRef.el) {
            console.error('Map element not found');
            return;
        }
        console.log('Map element found:', this.mapRef.el);
        
        const map = new googleMaps.Map(this.mapRef.el, {
            zoom: 12,
            center: { lat: 51.5074, lng: -0.1278 },
            mapId: this.map_ids,
        });
        const bounds = new googleMaps.LatLngBounds();
        
        if (this.polyline && this.polyline.length > 0) {
            try {
                const decodedPath = googleMaps.geometry.encoding.decodePath(this.polyline);
                const polyline = new googleMaps.Polyline({
                    path: decodedPath,
                    geodesic: true,
                    strokeColor: '#2980b9',
                    strokeOpacity: 1.0,
                    strokeWeight: 4
                });
        
                polyline.setMap(map);
            } catch (error) {
                console.error('Error decoding or displaying polyline:', error);
            }
        } else {
            console.warn('No polyline data available or polyline is empty.');
        }

        for (const stop of this.stops) {
            const geocoder = new googleMaps.Geocoder();
            try {
                const results = await new Promise((resolve, reject) => {
                    geocoder.geocode({ 'address': stop.address }, (results, status) => {
                        if (status === 'OK') {
                            resolve(results);
                        } else {
                            reject(status);
                        }
                    });
                });
                
                const marker = new googleMaps.marker.AdvancedMarkerElement({
                    map,
                    position: results[0].geometry.location,
                    title: stop.address,
                    content: this.createMarkerContent(stop.sequence)
                });

                bounds.extend(results[0].geometry.location);
            } catch (error) {
                console.error(`Error geocoding address ${stop.address}:`, error);
            }
        }
        map.fitBounds(bounds);
    }

    createMarkerContent(sequence) {
        const content = document.createElement('div');
        content.innerHTML = sequence.toString();
        content.style.background = '#4285f4';
        content.style.color = 'white';
        content.style.padding = '8px';
        content.style.borderRadius = '50%';
        return content;
    }
}