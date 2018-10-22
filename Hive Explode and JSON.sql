select place_id 
from
(
select place_id, category
from 
(
select key as place_id, get_json_object(place, '$.categories') as categories
from places_internal
where get_json_object(place, '$.writeups.short_description.text') is not null
) a
lateral view explode(split(substr(regexp_replace(a.categories, '"', ''), 2, length(regexp_replace(a.categories, '"', '')) - 2), ',')) id_list as category
) b
where b.category = 'b497d800-0dd3-44d5-abf7-b59c51c74d48';
