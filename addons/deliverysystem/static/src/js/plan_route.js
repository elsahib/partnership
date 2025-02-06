import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
class DeliveryRoutePlannerView extends Component {
    setup() {
        this.action = useService("action");
        this.orm = useService("orm");
        this.selectedStops = [];
        this.stops = [];
    }
    async mounted() {
        await this._loadStops();
    }
    async _loadStops() {
        this.stops = await this.orm.searchRead('delivery.stop', [['status', '=', 'open']], ['address', 'type', 'status', 'associated_parcels']);
    }
    async _onCreateRouteButtonClick() {
        if (this.selectedStops.length < 2) {
            this.env.services.notification.alert({
                title: this.env._t("Error"),
                body: this.env._t("Please select at least two stops."),
            });
            return;
        }

        try {
            const result = await this.orm.call('delivery.controller', 'create_route', [this.selectedStops]);
            if (result.error) {
                this.env.services.notification.alert({
                    title: this.env._t("Error"),
                    body: result.error,
                });
            } else if (result.route_id) {
                await this.action.doAction({
                    type: 'ir.actions.act_window',
                    res_model: 'delivery.route',
                    res_id: result.route_id,
                    view_mode: 'form',
                });
            }
        } catch (error) {
            console.error("Error creating route:", error);
            this.env.services.notification.alert({
                title: this.env._t("Error"),
                body: this.env._t("An error occurred while creating the route. Please check the console for details."),
            });
        }
    }
    _onStopSelect(stopId) {
        if (this.selectedStops.includes(stopId)) {
            this.selectedStops = this.selectedStops.filter(id => id !== stopId);
        } else {
            this.selectedStops.push(stopId);
        }
    }
}
DeliveryRoutePlannerView.template = 'deliverysystem.RoutePlannerView';
DeliveryRoutePlannerView.components = {};
export const deliveryRoutePlannerView = {
    component: DeliveryRoutePlannerView,
};
registry.category("actions").add("delivery_route_planner_view", deliveryRoutePlannerView);