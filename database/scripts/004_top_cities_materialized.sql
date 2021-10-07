CREATE OR REPLACE VIEW public.es_top_cities
AS WITH top_cities AS (
         SELECT
                CASE
                    WHEN es_real_estate.city ~~ '%kerület%'::text THEN 'Budapest'::text
                    ELSE es_real_estate.city
                END AS city_normalized
           FROM es_real_estate
          GROUP BY (
                CASE
                    WHEN es_real_estate.city ~~ '%kerület%'::text THEN 'Budapest'::text
                    ELSE es_real_estate.city
                END)
         HAVING count(*) > 1000
        )
 SELECT s.city_normalized,
    s.url,
    s."time",
    s.city,
    s.address,
    s.area,
    s.rooms,
    s.price,
    s.price / 357 AS price_eur,
    s.property_condition,
    s.build_year,
    s.description,
    s.floor,
    s.building_floors,
    s.property_type,
    s.area_lot,
    s.advertiser_agent,
    s.advertiser_name
   FROM ( SELECT
                CASE
                    WHEN es_real_estate.city ~~ '%kerület%'::text THEN 'Budapest'::text
                    ELSE es_real_estate.city
                END AS city_normalized,
            es_real_estate.url,
            es_real_estate."time",
            es_real_estate.city,
            es_real_estate.address,
            es_real_estate.area,
            es_real_estate.rooms,
            es_real_estate.price,
            es_real_estate.property_condition,
            es_real_estate.build_year,
            es_real_estate.description,
            es_real_estate.floor,
            es_real_estate.building_floors,
            es_real_estate.property_type,
            es_real_estate.area_lot,
            es_real_estate.advertiser_agent,
            es_real_estate.advertiser_name
           FROM es_real_estate) s
  WHERE (s.city_normalized IN ( SELECT top_cities.city_normalized
           FROM top_cities));