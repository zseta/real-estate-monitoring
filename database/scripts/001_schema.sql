/* Create the table which will contain real estate listings */
DROP TABLE IF EXISTS es_real_estate;
CREATE TABLE public.es_real_estate (
	url text NOT NULL,
	"time" timestamp NOT NULL,
	city text NULL,
	address text NULL,
	area int NULL,
	rooms int NULL,
	price int NULL,
	property_condition text NULL,
	build_year text NULL,
	description text NULL,
	floor int NULL,
	building_floors int NULL,
	property_type text NULL,
	area_lot int NULL,
	advertiser_agent text NULL,
	advertiser_name text NULL,
	price_eur int NULL
);

/* Create the hypertable to efficiently store the listings */
SELECT create_hypertable('es_real_estate', 'time');