/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useRef, useState, onMounted } from "@odoo/owl";
import { OpenRouteMapModal } from "./open_route_map_modal";

class OpenRouteMapDialog extends Component {
    static template = "deliverysystem.OpenRouteMapDialog";
    setup() {
        this.dialogService = useService("dialog");
        this.action = useService("action");
        this.orm = useService("orm");
        this.routeId = this.props.action.params.route_id;
        this.state = useState({
            routeId: null,
            stops: [],
            apiKey: null,
            polyline: null,
        });

        onMounted(async () => {
            await this.loadData();
            this.renderModal();
        });
    }

    async loadData() {
        if (!this.routeId) return;
        const route = await this.orm.read("delivery.route", [this.routeId], ["stops", "polyline"]);
        const stopIds = route[0].stops;
        const stops = await this.orm.read("delivery.stop", stopIds, ["address", "sequence","latitude","longitude"]);
        const apiKey = await this.orm.call('google.maps.helper', 'get_api_key', [[]]);
        this.state.routeId = this.routeId;
        this.state.stops = stops;
        this.state.apiKey = apiKey;
        this.state.polyline = route[0].polyline;
    }

    renderModal() {
        this.dialogService.add(OpenRouteMapModal, {
            routeId: this.state.routeId,
            stops: this.state.stops,
            apiKey: this.state.apiKey,
            polyline: this.state.polyline,
            action: this.props.action,
        });
    }
}

OpenRouteMapDialog.components = { OpenRouteMapModal };
OpenRouteMapDialog.props = {
    action: { type: Object },
};

registry.category("actions").add("open_delivery_route_map_modal", OpenRouteMapDialog);