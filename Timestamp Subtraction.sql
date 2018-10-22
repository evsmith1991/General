select 
average((CAST((CAST(d.viewed_at AS DATE AT 0)- CAST(d.created_at AS DATE AT 0)) AS DECIMAL(18,6)) * 86400)
      + ((EXTRACT(  HOUR FROM d.viewed_at) - EXTRACT(  HOUR FROM d.created_at)) * 3600)
      + ((EXTRACT(MINUTE FROM d.viewed_at) - EXTRACT(MINUTE FROM d.created_at)) * 60)
      +  (EXTRACT(SECOND FROM d.viewed_at) - EXTRACT(SECOND FROM d.created_at))) as time_to_view
from sandbox.evan_push_survey_flags e
join user_gp.ugc_survey u on u.id = e.survey_id
join user_gp.ugc_dispatch d on d.survey_id = e.survey_id
where u.event_type not in ('GDT', 'VOUCHER_REDEEMED_SURVEY_GETAWAYS_TOURS', 'VOUCHER_REDEEMED_SURVEY_GOODS_INSTANT', 'VOUCHER_REDEEMED_SURVEY_GETAWAYS_INSTANT', 'VOUCHER_REDEEMED_SURVEY_OTHER_FIVE_STAR', 'VOUCHER_REDEEMED_SURVEY_OTHER', 'VOUCHER_REDEEMED_SURVEY_GETAWAYS')
and d.viewed_at is not null
and e.email_flag = 0;
