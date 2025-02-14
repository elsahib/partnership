# Delivery System Module

This Odoo module extends Odoo's functionality to provide a comprehensive delivery management system. It allows you to manage delivery routes, stops, parcels, and delivery personnel efficiently.

## Features

*   **Delivery Route Management:** Create and manage delivery routes, optimize routes using Google Maps API, and track delivery progress.
*   **Delivery Stop Management:** Define delivery stops with addresses and types (pickup/drop-off).
*   **Parcel Management:** Track parcels, assign them to routes and delivery personnel, and manage their status.
*   **Delivery Personnel Management:** Manage delivery partners, their availability, and assigned routes.
*   **Block Scheduling:** Schedule delivery blocks and manage driver registrations.
*   **Google Maps Integration:** Utilize Google Maps API for route optimization, distance calculation, and map visualization.

## Dependencies

*   Odoo (version 18.0)
*   PostgreSQL
*   Google Maps API key (for route optimization and location tracking)
*   Python libraries: `pypeg2`, `jwt`, `googlemaps`

## Installation

1.  Clone this repository into your Odoo addons path (e.g., `/mnt/extra-addons`).
2.  Ensure the dependencies are installed. The `docker-compose.yml` file provides an example of how to install the python dependencies:

    ```sh
    apt-get update && apt-get install -y python3-pypeg2 python3-jwt gosu
    ```
3.  Configure the environment variables in a `.env` file (see example below).
4.  Configure the Odoo configuration file (`odoo.conf`) to connect to the database and specify the addons path (see example below).
5.  Restart the Odoo server.
6.  Update the modules list in Odoo.
7.  Install the "Delivery System" module.
8.  Configure the Google Maps API key in the Odoo settings (Settings > Delivery System Settings).

## Configuration

### .env

Create a `.env` file in the root directory of the repository with the following content, replacing the values with your actual configuration as these are the default values:

```sh
POSTGRES_USER=odoo 
POSTGRES_PASSWORD=odoo
```

This file is ignored by git, as specified in [.gitignore](.gitignore).

### odoo.conf

Create or modify your `odoo.conf` file in the `config` directory with the following content, replacing the values with your actual configuration:

```conf
[options]
db_host = db
db_port = 5432
db_user = YOUR_DB_USER
db_password = YOUR_DB_PASSWORD
admin_passwd = your_admin_password
addons_path = /mnt/extra-addons
dev=True
```

Note: Replace your_admin_password with a strong password.

This file is ignored by git, as specified in .gitignore.

## Usage
After installing the module, you can access the Delivery System menu in Odoo. From there, you can manage delivery routes, stops, parcels, and delivery personnel.

*   **Create Delivery Routes:** Go to Delivery System > Routes and create a new route. You can manually add stops or use the "Plan Route" feature to select stops from a list.
*   **Optimize Routes:** Use the "Optimize Route" button on the route form to optimize the route using the Google Maps API. This requires a valid Google Maps API key to be configured.
*   **Manage Parcels:** Go to Delivery System > Parcels and create new parcels. Assign them to routes and delivery personnel.
*   **Schedule Delivery Blocks:** Go to Delivery System > Delivery Blocks to schedule delivery blocks and manage driver registrations.

## Security
*   The module defines several user groups with different access levels: Admin, Driver, Customer, and Warehouse.
*   Record rules are defined to restrict access to delivery routes, orders, and parcels based on user roles.
*   The Google Maps API key is stored in the Odoo configuration parameters and should be protected accordingly.

## Assets
The module includes the following web assets:

*   JavaScript files for delivery route map, route planning, and map modal functionality.
*   XML templates for delivery route map and map modal views.
These assets are defined in the [__manifest__.py](addons/deliverysystem/__manifest__.py) file.