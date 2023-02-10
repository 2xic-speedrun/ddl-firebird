
CREATE TABLE LOGS (
	ID BIGINT NOT NULL,
	MESSAGE VARCHAR(500),
	CONNECT_ID INTEGER,
	CONNECT_COUNTER INTEGER,
	CONSTRAINT PK_AGENTLOGG PRIMARY KEY (ID)
);


CREATE TABLE USERS (
	ID BIGINT NOT NULL,
	MESSAGE VARCHAR(500),
	CONNECT_ID INTEGER,
	CONNECT_COUNTER INTEGER,
	CONSTRAINT PK_AGENTLOGG PRIMARY KEY (ID)
);


-- From https://firebirdsql.org/refdocs/langrefupd21-ddl-procedure.html
create procedure ismultiple (a bigposnum, b bigposnum)
  returns (res bool3)
as
  declare ratio type of bigposnum;      -- ratio is a bigint
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
    if (remainder = 0) then res = 1; else res = 0;
    execute procedure LOG(10);
  end
end;

create procedure LOG (a bigposnum)
  returns (res bool3)
as
  declare ratio type of bigposnum;      -- ratio is a bigint
  declare remainder type of bigposnum;  -- so is remainder
begin
  SELECT count(*) from LOGS;
  if (a is null or b is null) then res = null;
  else if (b = 0) then
  begin
    if (a = 0) then res = 1; else res = 0;
  end
end;

create procedure GET_COUNT ()
  returns (res bool3)
as
  declare ratio type of bigposnum;      -- ratio is a bigint
  declare remainder type of bigposnum;  -- so is remainder
begin
  SELECT COUNT(*) from USERS;
  res = 0;
end;

CREATE TRIGGER LOGG_OF_CONNECTION_ID FOR LOGS BEFORE INSERT
AS
begin
  new.logg_connect_id = current_connection;
  EXECUTE procedure GET_COUNT();
end;
