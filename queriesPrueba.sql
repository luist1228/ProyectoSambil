
sel


select "id", "macadd"  from entradaCC as e
where date_part('day',e."registroe")=date_part('day',timestamp '2019-05-31')

select "id", "macadd" from salidap as e
where date_part('day',e."registros")=date_part('day',timestamp '2019-05-31')

select count("macadd") from salidap as e
where e."macadd"=null


select count("macadd") from salidap as e
where e."macadd" is null


select *from salidap as e
where "macadd" is null

select *from entradap as e
where "macadd" is null



15 null
46 not null




24 84

46

select e."macadd" from entradap as e
left join salidap as s on s."macadd"=e."macadd" 
where s."id" IS NULL and e."macadd" is not null

select count(e."macadd") from entradap as e
left join salidap as s on s."macadd"=e."macadd" 
where s."macadd" IS NULL and e."macadd" is null


select (s."macadd") from entradap as e
inner join salidap as s on s."macadd"=e."macadd" 

select * from entradap as e 
where "macadd"='F9:57:A2:9D:AF:B0'


select count(e."macaddres") , e."macaddres" from Persona as e
group by "macaddres"



select b."id" from beacon as b
inner join tienda as t on t."fkbeacon"=b."id"

select b."id" from beacon as b
inner join mesa as t on t."fkbeacon"=b."id"





