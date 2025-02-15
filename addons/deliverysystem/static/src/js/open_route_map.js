/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";
import { DeliveryRouteMap } from "./delivery_route_map";
import { useService } from "@web/core/utils/hooks";

class DeliveryRouteMapAction extends Component {
    static template = "deliverysystem.DeliveryRouteMapAction";
    static components = { Dialog, DeliveryRouteMap };

    setup() {
        this.orm = useService("orm");
        this.routeId = this.props.action.params.route_id;
        this.state = useState({
            routeId: this.props.action.params.route_id,
            stops: [],
            apiKey: "",
            polyline: "",
            mapId:""
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        const orm = this.env.services.orm;
        const [route] = await orm.read("delivery.route", [this.routeId], ["stops", "polyline"]);
        const stops = await orm.read("delivery.stop", route.stops, ["address", "sequence", "latitude", "longitude"]);
        const apiKey = await orm.call('google.maps.helper', 'get_api_key', [[]]);
        const mapId = await orm.call('google.maps.helper', 'get_map_id', [[]]);

        this.state.mapId = mapId
        this.state.stops = stops;
        this.state.apiKey = apiKey;
        this.state.polyline = route.polyline;
    }
}

// Remove old registry entry
registry.category("actions").add("delivery_route_map_action", DeliveryRouteMapAction);