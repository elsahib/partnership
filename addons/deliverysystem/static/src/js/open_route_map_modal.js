/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { DeliveryRouteMap } from "./delivery_route_map";

export class OpenRouteMapModal extends Component {
    static template = "deliverysystem.OpenRouteMapModal";
    static components = { Dialog: Dialog, DeliveryRouteMap: DeliveryRouteMap }; // Correct the components object
    // static props = {
    //     close: { type: Function },
    //     action: { type: Object },
    //     routeId: { type: Number },
    //     stops: { type: Array },
    //     apiKey: { type: String },
    // };

    setup() {
        // this.actionService = useService("action");
        // this.dialogService = useService("dialog");
        // this.orm = useService("orm");
        this.state = useState({
            routeId: this.props.routeId,
            stops: this.props.stops,
            apiKey: this.props.apiKey,
        });
        console.log('Modal Props:', this.props);
    }

    // async willStart() {
    //     // await this.loadData(); //No need to load data here, it's passed from the dialog
    // }

    // async loadData() {
    //     // if (!this.state.routeId) return;
    //     // const route = await this.orm.read("delivery.route", [this.state.routeId], ["stops"]);
    //     // const stopIds = route[0].stops;
    //     // const stops = await this.orm.read("delivery.stop", stopIds, ["address", "sequence"]);
    //     // this.state.stops = stops;
    //     // this.state.apiKey = await this.orm.call('google.maps.helper', '_get_api_key', []);
    // }

    closeModal() {
        this.props.close();
    }
}