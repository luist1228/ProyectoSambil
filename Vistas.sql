--------------------VIEWS-----------------------------------------
------------------------------------------------------------------
Create or replace view porcentajeConMAC as 
select (count("fkpersonamac")*100)/count(*) as conmac, 100- (count("fkpersonamac")*100)/count(*) as sinmac
from compra ;


------------------------------------------------------------------

create or replace view masVisitas as
select count (e."macadd"), s."nombre" 
from entradacc as e
inner join persona as s on s."macaddres"= e."macadd"
group by s."nombre"
limit 5;

------------------------------------------------------------------






