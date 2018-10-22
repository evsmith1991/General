create table grp_gdoop_bizops_db.clo_reminder_test2 as
select a.consumer_id, a.variant, a.send_date
, case when datediff(tr.auth_date, a.send_date) between 0 and 7 then 1 else 0 end as red_7d_yn 
, count(distinct case when datediff(tr.auth_date, a.send_date) <= 7 then tr.id else null end) as redemptions
, case when datediff(tr.auth_date, a.send_date) between 0 and  7 and tr.deal_uuid = a.deal_uuid then 1 else 0 end as red_7d_test_deal_yn 
, count(distinct case when datediff(tr.auth_date, a.send_date) <= 7 and tr.deal_uuid = a.deal_uuid then tr.id else null end) as redemptions_test_deal
from (
    select u.consumer_id, u.variant, u.deal_uuid, u.send_date
    from grp_gdoop_bizops_db.clo_reminder_test_users u
) a
left join (
    select u.consumer_id, o.deal_id as deal_uuid, tr.id, to_date(tr.timestamp_col) as auth_date
    from user_gp.clo_users u
    join user_gp.clo_claims cl on cl.user_id = u.id --and cl.pre_claim_reward = 0
    join user_gp.clo_offers o on o.id = cl.offer_id
    join (
        select *
        from user_gp.clo_visa_transactions
        where to_date(timestamp_col) between '2018-03-27' and '2018-04-09'
        and raw_transaction_type = 'Auth'
    ) tr on tr.claim_id = cl.id
) tr on tr.consumer_id = a.consumer_id 
group by 1,2,3,4,6;

select variant, count(distinct consumer_id) as num_users
, avg(red_7d_yn) as avg_redeemer_per
, var_pop(red_7d_yn) as var_redeemer_per
, avg(redemptions) as avg_redemptions
, var_pop(redemptions) as var_redemptions
, avg(red_7d_test_deal_yn) as avg_same_deal_redeemer_per
, var_pop(red_7d_test_deal_yn) as var_same_deal_redeemer_per
, avg(redemptions_test_deal) as avg_same_deal_redemptions
, var_pop(redemptions_test_deal) as var_same_deal_redemptions
from grp_gdoop_bizops_db.clo_reminder_test2
--where send_date between '2018-03-28' and '2018-03-29'
group by 1;
