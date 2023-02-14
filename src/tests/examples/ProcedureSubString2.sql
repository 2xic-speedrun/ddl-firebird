-- From https://firebirdsql.org/refdocs/langrefupd21-ddl-procedure.html
create procedure ismultiple (a bigposnum, b bigposnum)
  returns (res bool3)
as
  declare variable tekst varchar(100);      /* 22.06.2020 Utvidet fra 45 for å kunne appende tekst fra transkode.tekst. NB Blir klipt til 60 pos ved overf. til new.transtekst! */
  declare remainder type of bigposnum;  -- so is remainder
begin
  if (a is null or b is null) then res = null;
  else if (b = 0) then
  begin
    if (a = 0) then res = 1; else res = 0;
  end
  else
  begin
    ratio = a / b;                      -- integer division!
    remainder = a - b*ratio;
    tekst =  substring(:tekst from 1 for 60);  -- 14.09.2020  Ekstra test på lengde transtekst lagt inn for å unngå exception.
    if (remainder = 0) then res = 1; else res = 0;
  end
end
