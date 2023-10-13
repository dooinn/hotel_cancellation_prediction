use hotel;


-- Total Hotel Count : 119k
select COUNT(*) as total_hotel from hotel_booking limit 100;



-- Hotel Count By types: Resort Hotel (40060), City Hotel (79326)
select hotel, count(hotel) as count from hotel_booking
group by hotel;



-- Cancellation: True (75166), False (44220)
select is_canceled, count(*) as count from hotel_booking
group by is_canceled;

-- Cancellation Rate per hotel
-- City Hotel : 41,72%, Resort hotel: 27.76%
select
	hotel,
    round(avg(case when is_canceled = 1 THEN 1 ELSE 0 END) * 100, 2) as CancellationRate
from hotel_booking
group by hotel
order by CancellationRate desc;


-- lead time : NUmber of days between booking and arrival
-- Resort (128 days), City (150days)


-- Ag of numerica values
-- lead time: Resort(128 days), City (150days) > City Hotel appears to longer term bettwen booking and arrival
-- Weekend nights: Resort(1.3 days), City(0.7 days) > People tened to stay in Resort hotel a bit longer during weekend
-- Week days: Resort(3.4 days), City(2.2 days) > Like weekends, Peple stay longer in Resort thant City during weekdays
-- # Adults: Resort (1.9), City (1.8) > No significant differences identified.
-- # Children: Resort (0.18), City (0.08) > Resort seems more preffered by family who has children
-- # Babies: Resort (0.0094), City(0.0019) > Although the # of babies stay in hotels is very scarece, Resort is sligihtly bigger.
-- Booking Changes: Resort(0.15), City(0.07).
-- # days waiting list: Resort(0.09), City(4.73) > City Hotel reveals the four times longer days of waiting list, we could relate this to the cause of high cancellation rate of City Hotel (41%), Although it's high demand, it also have high cancellation rate
-- # car parking spaces: Resort(0), City(0)
-- # Special Request: Resort (0.4), City(0.2) > Resort sliglhtl higher number in special request > it possible means that they have family? (e.g. special request for baby or child bed?)
select 
	hotel, 
    avg(lead_time) as avg_lead_time,
    avg(stays_in_weekend_nights) as avg_stay_weekend_nights,
    avg(stays_in_week_nights) as avg_staty_week_nights,
    avg(adults) as avg_adults,
    avg(children) as avg_children,
    avg(babies) as avg_babies,
    avg(booking_changes) as avg_booking_changes,
    avg(days_in_waiting_list) as avg_days_waiting_list,
    avg(required_car_parking_spaces) as avg_car_parking_spaces,
    avg(total_of_special_requests) as avg_special_requests,
    avg(previous_cancellations) as avg_prev_cancel,
    avg(previous_bookings_not_canceled) as avg_prev_not_cancel
from hotel_booking
	where is_canceled = 1
	group by hotel;
    

-- Repeated Guest
-- Repeated Guest (14.5%) VS Non-Repeated Guest (37.8%) > Cancellation Rate?

-- Repeated Guest Canccelation Rate(14.5%)
select
	round(avg(case when is_canceled = 1 THEN 1 ELSE 0 END) * 100, 2) as CancellationRate
from hotel_booking
	where is_repeated_guest = 1;

-- Non-Repeated Guest Cancellation Rate(37.8%)
select
	round(avg(case when is_canceled = 1 THEN 1 ELSE 0 END) * 100, 2) as CancellationRate
from hotel_booking
	where is_repeated_guest = 0;
    
    
select arrival_date_year, count(*) as count from hotel_booking
group by arrival_date_year;

select * from hotel_booking;

select name, count(*) as count from hotel_booking
group by name
order by count desc;







