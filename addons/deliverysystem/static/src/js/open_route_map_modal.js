/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { DeliveryRouteMap } from "./delivery_route_map";
export class OpenRouteMapModal extends Component {
    static template = "deliverysystem.OpenRouteMapModal";
    static components = { Dialog: Dialog, DeliveryRouteMap: DeliveryRouteMap }; // Correct the components object

    setup() {
        this.state = useState({
            routeId: this.props.routeId,
            stops: this.props.stops,
            apiKey: this.props.apiKey,
            polyline: this.props.polyline,
        });
    }
    closeModal() {
        this.props.close();
    }
}