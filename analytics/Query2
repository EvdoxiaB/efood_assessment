Select a.city, round((100*sum(b.top10_orders)/ sum(a.total_orders)),2) as top10_cont_perc
from 
	(select city, count(order_id) as total_orders
	from `efood2022-361807.main_assessment.orders`
	group by city) as A
left join 
	(select city, sum(orders_per_user) as top10_orders
	from (
        select city, user_id, count(order_id) as orders_per_user,
        row_number() over(partition by city order by count(order_id) desc) as rnk
			  from `efood2022-361807.main_assessment.orders`
        group by city, user_id
		) as temp
	where rnk <= 10
  group by city) as B
on A.city = B.city
group by city
