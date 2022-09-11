select user_id, sum(breakfast_orders) as Break_orders, sum(other_orders) as oth_orders, sum(cash_orders) as orders_cash, sum(credit_orders) as orders_credit,
	sum(total_orders) as orders_tl, round(sum(total_spend),2) as tl_spend,	
	sum(case when city_group='Sterea Ellada' then 1 else 0 end) as StereaEllada_orders,
	sum(case when city_group='Anat Makedonia and Thraki' then 1 else 0 end) as AnatMakedoniaThraki_orders,
	sum(case when city_group='Nisia' then 1 else 0 end) as Nisia_orders,
	sum(case when city_group='Dutiki Ellada' then 1 else 0 end) as DutikiEllada_orders,
	sum(case when city_group='Dutiki Makedonia' then 1 else 0 end) as DutikiMakedonia_orders,
	sum(case when city_group='Ipeiros' then 1 else 0 end) as Ipeiros_orders,
	sum(case when city_group='Thessalia' then 1 else 0 end) as Thessalia_orders,
	sum(case when city_group='Kentriki Makedonia' then 1 else 0 end) as KentrikiMakedonia_orders,
	sum(case when city_group='Peloponnisos' then 1 else 0 end) as Peloponnisos_orders
from(
	select user_id, city,
  	sum(case when cuisine='Breakfast' then 1 else 0 end) as breakfast_orders,
  	sum(case when cuisine<>'Breakfast' then 1 else 0 end) as other_orders,
  	sum(case when paid_cash=true then 1 else 0 end) as cash_orders,
  	sum(case when paid_cash=false then 1 else 0 end) as credit_orders,
  	count(order_id) as total_orders,
  	sum(amount) as total_spend,
  	case 
  		when city in ('Θήβα', 'Λαμία', 'Λιβαδειά', 'Αράχωβα', 'Αλίαρτος', 'Ιστιαία', 'Οινόφυτα', 'Βασιλικό', 'Αίγινα') then 'Sterea Ellada'
		when city in ('Ξάνθη', 'Αλεξανδρούπολη', 'Διδυμότειχο', 'Δράμα', 'Ορεστιάδα') then 'Anat Makedonia and Thraki'
		when city in ('Ρόδος', 'Λέρος', 'Ζάκυνθος', 'Λευκάδα', 'Νάξος', 'Άνδρος', 'Μύκονος') then 'Nisia'
		when city in ('Αγρίνιο', 'Μεσολόγγι', 'Ναύπακτος', 'Αμαλιάδα') then 'Dutiki Ellada'
		when city in ('Φλώρινα', 'Γρεβενά') then 'Dutiki Makedonia'
		when city in ('Ιωάννινα', 'Άρτα', 'Ηγουμενίτσα') then 'Ipeiros'
		when city in ('Βόλος', 'Λάρισα') then 'Thessalia'
		when city in ('Βέροια', 'Έδεσσα', 'Νάουσα', 'Αλεξάνδρεια', 'Γιαννιτσά', 'Αριδαία') then 'Kentriki Makedonia'
		else 'Peloponnisos' 
  	end as city_group
	from `efood2022-361807.main_assessment.orders`
	group by user_id, city) as temp
group by user_id
