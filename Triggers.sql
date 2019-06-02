--------------------TRIGGERS--------------------------------------
------------------------------------------------------------------
CREATE OR REPLACE FUNCTION RegistroPersona()
RETURNS TRIGGER AS $$
declare
	n varchar(20);
BEGIN
		if new.macadd is not null then
			SELECT s."macaddres" into n 
			from Persona as s
			where s."macaddres"=new.macadd;
			
			if n is null then
			INSERT INTO public.persona( macaddres) VALUES (new.macadd);	
			end if;
		end if;
		return new;
END
$$ LANGUAGE plpgSQL;


CREATE TRIGGER RegistroPersonaT
BEFORE INSERT
ON EntradaCC
FOR EACH ROW
EXECUTE PROCEDURE RegistroPersona();



------------------------------------------------------------------
CREATE OR REPLACE FUNCTION CompraconMac()
RETURNS TRIGGER AS $$
declare
f timestamp ;
BEGIN
	if new.fkpersonamac is not null then
	
	select e."registroe" into f from EntradaCC as e
	where  new.fkpersonamac=e."macadd"
	ORDER BY e."registroe" DESC
	limit 1;
	
	INSERT INTO public.compraentrada( fkcompra, fechaentrada) VALUES (new.id, f);
	
	end if;
	
	return null;
	
END
$$ LANGUAGE plpgSQL;


CREATE TRIGGER CompraconMacT
AFTER INSERT
ON Compra
FOR EACH ROW
EXECUTE PROCEDURE CompraconMac();


------------------------------------------------------------------











