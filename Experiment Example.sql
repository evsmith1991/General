create table sandbox.stay_high_test as(
    select v.consumer_id, v.variant
    , count(distinct tr.id) as num_reds
    , max(case when tr.id is not null then 1 else 0 end) as red_yn
    from sandbox.stay_high_user_variants v
    join user_gp.clo_users u on u.consumer_id = v.consumer_id
    left join user_gp.clo_claims cl on cl.user_id = u.id and cl.pre_claim_reward = 0
    left join (
        select *
        from user_gp.clo_visa_transactions
        where timestamp_col between date '2018-05-30' and date '2018-06-05'
        and raw_transaction_type = 'auth'
        and is_eligible = 't'
    ) tr on tr.claim_id = cl.id
    group by 1,2
) with data primary index (consumer_id, variant);

select variant
, count(distinct consumer_id) as num_users
, average(num_reds) as avg_reds
, var_pop(num_reds) as var_reds
, average(red_yn) as avg_red_per
, var_pop(red_yn) as var_red_per
from sandbox.stay_high_test
group by 1;
