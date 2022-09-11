select bkf.city, sum(bkf.break_freqUser_contr_perc) as Br_FreqUs_perc, sum(tl.efood_freqUser_contr_perc) as ef_FreqUs_perc,
sum(bkf.Break_basket) as Bkt_Break, sum(tl.efood_basket) as Bsk_efood, sum(bkf.Freq_Break) as Break_frq, sum(tl.Freq_efood) as efood_frq
from (
	select a.city, (sum(b.freq_users)/sum(a.total_users)) as break_freqUser_contr_perc, sum(a.basket_break) as Break_basket, 
	sum(a.Break_freq) as Freq_Break
	from (
		select city, count(distinct(user_id)) as total_users, sum(amount)/count(order_id) as basket_break,
		count(order_id)/count(distinct (user_id)) as Break_freq,
		row_number() over(partition by city order by count(order_id) desc) as rnk
		from `efood2022-361807.main_assessment.orders` 
		where cuisine = "Breakfast"
		group by city
		having count(order_id)>=1000) as a
	left join (
		select city, count(user_id) as freq_users
		from (
			select city, user_id, count(order_id) as orders_per_user
			from `efood2022-361807.main_assessment.orders` 
			where cuisine = "Breakfast"
			group by city, user_id
			having count(order_id)>3
			)
		group by city) as b
	on a.city = b.city
	where a.rnk<=5
	group by city) as bkf
left join (
	select a.city, (sum(b.freq_users)/sum(a.total_users)) as efood_freqUser_contr_perc, sum(a.basket_efood) as efood_basket, sum(a.efood_freq) as Freq_efood 
	from (
		select city, count(distinct(user_id)) as total_users, sum(amount)/count(order_id) as basket_efood,
		count(order_id)/count(distinct (user_id)) as efood_freq,
		from `efood2022-361807.main_assessment.orders` 
		group by city
		having count(order_id)>=1000) as a
	left join (
		select city, count(user_id) as freq_users
		from (
			select city, user_id, count(order_id) as orders_per_user
			from `efood2022-361807.main_assessment.orders` 
			group by city, user_id
			having count(order_id)>3
			)
      group by city) as b
	on a.city = b.city
	group by city) as tl
on bkf.city = tl.city
group by city
